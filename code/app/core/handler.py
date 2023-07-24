from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from core.babel_config import _


def add_handlers(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(request: Request, exc: RequestValidationError):
        translated_errors = []
        for pydantic_error in exc.errors():
            msg = _(pydantic_error.get("msg", _('Error message not detected')))
            pydantic_error['msg'] = msg
            translated_errors.append(pydantic_error)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(
                {"detail": translated_errors}
            )
        )

    # @app.exception_handler(RequestValidationError)
    # def fastapi_error_handler(request, exc: RequestValidationError):
    #     error_wrapper = exc.raw_errors[0]
    #     validation_error = error_wrapper.exc
    #     from pydantic import error_wrappers as ew
    #     new_errors = []
    #     if isinstance(validation_error, ew.ValidationError):
    #         errors = validation_error.errors()
    #
    #         for error in errors:
    #             if error.get('msg', None) and error.get('loc', None):
    #                 loc = error['loc'][0]
    #                 msg = _(error.get("msg"))
    #                 new_errors.append({loc: msg})
    #             else:
    #                 logging.warn(error)
    #                 new_errors.append({"detail": _("Error type not detected!")})
    #     return JSONResponse(status_code=422, content=jsonable_encoder(new_errors))

    # @app.exception_handler(RequestValidationError)
    # def custom_form_validation_error(request, exc):
    #     # reformatted_message = defaultdict(list)
    #     reformatted_message = []
    #     print(exc.errors())
    #     for pydantic_error in exc.errors():
    #         loc, msg = pydantic_error["loc"], pydantic_error["msg"]
    #         filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
    #
    #         field_string = ".".join(filtered_loc)  # nested fields with dot-notation
    #         reformatted_message.append(
    #             {field_string: [msg]}
    #         )
    #         # reformatted_message[field_string].append(msg)
    #
    #     return JSONResponse(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         content=jsonable_encoder(
    #             {"detail": "Invalid request", "errors": reformatted_message}
    #         ),
    #     )
