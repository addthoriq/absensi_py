from models import Base
from sqlalchemy import Column, Integer, String, VARCHAR

class User(Base):
	__tablename__ = "users"

	id = Column("id", Integer, primary_key=True, nullable=False, autoincrement=True)
	email = Column("email", VARCHAR(30), nullable=False)
	nama = Column("nama", String(50), nullable=False)
	password = Column("password", String(255), nullable=False)