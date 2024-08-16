from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
    declarative_base,
    Session as SqlalchemySession,
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from settings import DB_PORT, DB_HOST, DB_USER, DB_NAME, DB_PASSWORD

# Create SQLAlchemySession
user = DB_USER
password = DB_PASSWORD
host = DB_HOST
port = DB_PORT
database = DB_NAME

# To use session for query, insert, update and delete see:
# https://docs.sqlalchemy.org/en/14/orm/session_basics.html#using-a-sessionmaker
# Create sync session
engine = create_engine(
    f"postgresql+psycopg2cffi://{user}:{password}@{host}:{port}/{database}",
    pool_size=100,
    max_overflow=0,
    pool_timeout=300,
)
Session = sessionmaker(engine, future=True)
factory_session = scoped_session(Session)


def get_db_sync():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# how to use async session on orm see:
# https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#synopsis-orm
# asyncpg currently not working on PyPy
# Create async session
async_engine = create_async_engine(
    f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
)
Async_Session = sessionmaker(async_engine, class_=AsyncSession)

# base for model
Base = declarative_base()

# for alembic automigrations
from .User import User  # NoQA
from .Role import Role  # NoQA
from .Shift import Shift  # NoQA
from .Kehadiran import Kehadiran  # NoQA
from .Absensi import Absensi  # NoQA


def clear_all_data_on_database(db: SqlalchemySession):
    stmt = select(Absensi)
    all_data = db.execute(stmt).scalars().all()
    for val in all_data:
        db.delete(val)
    stmt = select(Kehadiran)
    all_data = db.execute(stmt).scalars().all()
    for val in all_data:
        db.delete(val)
    stmt = select(Shift)
    all_data = db.execute(stmt).scalars().all()
    for val in all_data:
        db.delete(val)
    stmt = select(Role)
    all_data = db.execute(stmt).scalars().all()
    for val in all_data:
        db.delete(val)
    db.commit()
    db.execute(text("DELETE FROM public.user"))
    db.commit()
