from sqlalchemy import NullPool, create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings


engine = create_engine(
    settings.SYNC_DATABASE_URI,
    echo=False,
    future=True,
    # pool_size=settings.POOL_SIZE,
    # max_overflow=64,
    poolclass=NullPool
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)
