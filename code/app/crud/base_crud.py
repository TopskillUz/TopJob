import re
from io import BytesIO
from typing import Optional, Type, TypeVar, Union, Dict, Any
from uuid import UUID

from fastapi import HTTPException
from fastapi_sqlalchemy import db
from psycopg2.errorcodes import UNIQUE_VIOLATION, NOT_NULL_VIOLATION, FOREIGN_KEY_VIOLATION
from pydantic import BaseModel
from sqlalchemy import exc, select, and_, or_
from sqlalchemy.orm import Query, InstrumentedAttribute
from sqlalchemy.orm import Session
from core.babel_config import _
from exceptions import IdOrSlugNotFoundException
from models import Media
from utils.minio_client import MinioClient

ModelType = TypeVar("ModelType")
TranslationModelType = TypeVar("TranslationModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
T = TypeVar("T")


class BaseCrud:
    def __init__(self, model: Type[ModelType], i18n_model: Type[TranslationModelType] = None):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `i18n_model`: A SQLAlchemy model class
        """
        self.model = model
        self.i18n_model = i18n_model

    def base_query(self,
                   order_by: str,
                   desc: bool,
                   where: Optional[dict] = None,
                   query: Optional[Query] = None,
                   q: Optional[str] = None,
                   search_fields: Optional[list] = None,
                   i18n_search_fields: Optional[list] = None):
        try:
            search_fields = search_fields or []
            i18n_search_fields = i18n_search_fields or []
            # create select with where (if where)
            if query is None:
                if where:
                    query = select(self.model).where(and_(k == v for k, v in where.items()))
                else:
                    query = select(self.model)
            query = query.filter(self.model.deleted_at.is_(None))
            # get order by
            order_field = getattr(self.model, order_by)
            query = query.order_by(order_field.desc() if desc else order_field.asc())

            # get extra query
            extra_query = [getattr(getattr(self.model, field), 'ilike')(f"%{q}%") for field in
                           search_fields if q and search_fields]
            # append i18n model to query
            if i18n_search_fields and q:
                query = query.join(self.i18n_model)
            # get i18n extra query
            i18n_extra_query = [getattr(getattr(self.i18n_model, field), 'ilike')(f"%{q}%") for field in
                                i18n_search_fields if q and i18n_search_fields]
            query = query.filter(or_(*extra_query, *i18n_extra_query))
            return query
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e),
            )

    def get(
            self, where: Optional[dict] = {},
            query: Optional[Query] = None,
            db_session: Optional[Session] = None
    ) -> Optional[ModelType]:
        db_session = db_session or db.session
        if query is not None:
            statement = query
        else:
            statement = select(self.model).where(and_(k == v for k, v in where.items())).filter(
                self.model.deleted_at.is_(None))
        objs = db_session.execute(statement)
        return objs.scalar_one_or_none()

    def get_obj(self, where: Optional[dict] = {},
                query: Optional[Query] = None,
                db_session: Optional[Session] = None) -> ModelType:
        obj = self.get(where=where, query=query, db_session=db_session)
        if not obj:
            raise IdOrSlugNotFoundException(self.model)
        return obj

    def create(
            self,
            create_data: Union[CreateSchemaType, dict],
            created_by_id: Optional[Union[UUID, str]] = None,
            db_session: Optional[Session] = None
    ) -> ModelType:
        db_session = db_session or db.session
        if not isinstance(create_data, dict):
            create_data = create_data.model_dump(exclude_unset=True, exclude_none=True)
        if self.i18n_model:
            if 'translations' in create_data and create_data['translations']:
                translations = [self.i18n_model(**translation) for translation in create_data['translations']]
            else:
                translations = []
            del create_data['translations']
            db_obj = self.model(**create_data, translations=translations)
        else:
            db_obj = self.model(**create_data)

        if created_by_id:
            db_obj.created_by_id = created_by_id

        try:
            db_session.add(db_obj)
            db_session.commit()
        except exc.SQLAlchemyError as e:
            err_code, err_text = self.error_handling(e)
            db_session.rollback()
            raise HTTPException(
                status_code=err_code,
                detail=str(err_text),
            )
        db_session.refresh(db_obj)
        return db_obj

    @classmethod
    def error_handling(cls, e: exc.SQLAlchemyError):
        orig = getattr(e, 'orig', None)
        if orig:
            if orig.pgcode == UNIQUE_VIOLATION:
                regex = r'Key\s+\((?P<key>.*)\)=\((?P<value>.*)\)\s+already\s+exists.*$'
                groups = re.search(regex, orig.args[0]).groups()
                if len(groups) == 2:
                    return 409, _("'{field_name}' already exists in database").format(field_name=groups[1])
            elif orig.pgcode == NOT_NULL_VIOLATION:
                regex = r'in\scolumn\s"(?P<text>.*?)".*?"(?P<table>.*?)"'
                groups = re.search(regex, orig.args[0]).groups()
                if len(groups) == 2:
                    return 400, _("'{field_name}' field required in table '{table_name}'").format(field_name=groups[0],
                                                                                                  table_name=groups[1])
            elif orig.pgcode == FOREIGN_KEY_VIOLATION:
                regex = r'Key\s+\((?P<key>.*?)\).*?"(?P<table>.*)"'
                groups = re.search(regex, orig.args[0].replace("\\", '')).groups()
                if len(groups) == 2:
                    return 400, _("Key '{field_name}' doesn't exists in the table '{table_name}'").format(
                        field_name=groups[0],
                        table_name=groups[1])
            return 400, orig
        print(157, e)
        return 400, e

    def update(
            self,
            obj_key: Union[UUID, str, int],
            update_data: Union[UpdateSchemaType, Dict[str, Any]],
            attr_key: InstrumentedAttribute = None,
            db_session: Optional[Session] = None
    ) -> ModelType:
        try:
            db_session = db_session or db.session
            if not attr_key:
                attr_key = self.model.id
            obj = self.get(where={attr_key: obj_key}, db_session=db_session)
            if not obj:
                raise IdOrSlugNotFoundException(self.model, obj_key)

            if not isinstance(update_data, dict):
                update_data = update_data.model_dump(exclude_unset=True)
            # obj_data = jsonable_encoder(obj)

            # for field in obj_data:
            #    if field in update_data:
            for field in update_data:
                if field == 'translations':
                    for db_translation in obj.translations:
                        db_session.delete(db_translation)

                        try:
                            db_session.commit()
                        except exc.SQLAlchemyError as e:
                            err_code, err_text = self.error_handling(e)
                            db_session.rollback()
                            raise HTTPException(
                                status_code=err_code,
                                detail=str(err_text),
                            )

                    updated_data = [self.i18n_model(**translation) for translation in update_data[field]]
                else:
                    updated_data = update_data[field]
                setattr(obj, field, updated_data)

            db_session.commit()
        except exc.SQLAlchemyError as e:
            err_code, err_text = self.error_handling(e)
            db_session.rollback()
            raise HTTPException(
                status_code=err_code,
                detail=str(err_text),
            )
        db_session.refresh(obj)
        return obj

    def get_list(self,
                 order_by: str = 'id',
                 desc: bool = False,
                 where: Optional[dict] = {},
                 query: Optional[Query] = None,
                 q: Optional[str] = None,
                 search_fields: Optional[list] = None,
                 i18n_search_fields: Optional[list] = None,
                 db_session: Optional[Session] = None):
        try:
            db_session = db_session or db.session
            # create query
            query = self.base_query(order_by=order_by, desc=desc, where=where, query=query, q=q,
                                    search_fields=search_fields,
                                    i18n_search_fields=i18n_search_fields)
            # execute query
            response = db_session.execute(query)
            # return response
            return response.scalars().unique().all()
        except exc.SQLAlchemyError as e:
            err_code, err_text = self.error_handling(e)
            raise HTTPException(
                status_code=err_code,
                detail=str(err_text),
            )

    def get_paginated_list(self,
                           page_number,
                           page_size,
                           order_by,
                           desc,
                           where: Optional[dict] = {},
                           query: Optional[Query] = None,
                           q: Optional[str] = None,
                           search_fields: Optional[list] = None,
                           i18n_search_fields: Optional[list] = None,
                           db_session: Optional[Session] = None):
        try:
            db_session = db_session or db.session
            # create base query
            query = self.base_query(order_by=order_by, desc=desc, where=where, query=query, q=q,
                                    search_fields=search_fields,
                                    i18n_search_fields=i18n_search_fields)
            # apply pagination
            query, pagination = apply_pagination(table=self.model, query=query, page_number=page_number,
                                                 page_size=page_size)

            # execute query
            response = db_session.execute(query)

            # return response
            return response.scalars().unique().all(), pagination
        except exc.SQLAlchemyError as e:
            err_code, err_text = self.error_handling(e)
            raise HTTPException(
                status_code=err_code,
                detail=str(err_text),
            )

    def delete(
            self, obj_key: Union[UUID, str, int],
            attr_key: InstrumentedAttribute = None,
            db_session: Optional[Session] = None
    ):
        db_session = db_session or db.session
        if not attr_key:
            attr_key = self.model.id
        obj = self.get_obj(where={attr_key: obj_key}, db_session=db_session)
        db_session.delete(obj)

        try:
            db_session.commit()
        except exc.SQLAlchemyError as e:
            err_code, err_text = self.error_handling(e)
            raise HTTPException(
                status_code=err_code,
                detail=str(err_text),
            )

    def upsert_media(self,
                     obj: ModelType,
                     field_name: str,
                     file_data: BytesIO,
                     minio_client: MinioClient,
                     file_path: str,
                     filename: str,
                     size: int,
                     content_type: str,
                     created_by_id: Optional[UUID] = None,
                     db_session: Optional[Session] = None):
        db_session = db_session or db.session
        from . import media as media_crud
        # save file to minio server
        data_file = minio_client.put_object(
            file_path=file_path,
            file_data=file_data,
            content_type=content_type,
        )
        media_id = getattr(obj, field_name, None)

        if media_id:
            # update
            media = media_crud.get(where={Media.id: media_id}, db_session=db_session)
            # remove old image from minio
            minio_client.remove_object(media.path)

            # update media
            media.file_format = content_type
            media.size = size
            media.filename = filename
            media.path = data_file.file_name

            db_session.add(media)
        else:
            # create
            media_data = media_schema.AMediaCreateSchema(filename=filename,
                                                         size=size,
                                                         path=data_file.file_name,
                                                         file_format=content_type,
                                                         created_by_id=created_by_id)
            media = media_crud.create(data=media_data, db_session=db_session)

            setattr(obj, field_name, media.id)
        try:
            db_session.commit()
        except exc.SQLAlchemyError as e:
            err_code, err_text = self.error_handling(e)
            db_session.rollback()
            raise HTTPException(
                status_code=err_code,
                detail=str(err_text),
            )
        db_session.refresh(obj)
        return obj
