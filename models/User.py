from models import Base
from sqlalchemy import Column, Integer, String, VARCHAR, Boolean

class User(Base):
	__tablename__ = "users"

	id = Column("id", Integer, primary_key=True, nullable=False, autoincrement=True)
	email = Column("email", VARCHAR(30), nullable=False)
	nama = Column("nama", String(50), nullable=False)
	password = Column("password", String(255), nullable=False)
	is_teacher = Column("is_teacher", Boolean, nullable=False)
	is_superadmin = Column("is_superadmin", Boolean, nullable=False)