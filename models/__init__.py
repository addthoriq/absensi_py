from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from settings import (
	DB_PORT,
	DB_HOST,
	DB_USER,
	DB_NAME,
	DB_PASSWORD
)

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
	f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}",
	pool_size=100,
	max_overflow=0,
	pool_timeout=300
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
	f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"
)
Async_Session = sessionmaker(async_engine, class_=AsyncSession)

# base for model
Base = declarative_base()

# for alembic automigrations
from models.User import User