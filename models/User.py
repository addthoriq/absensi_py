from . import Base
from sqlalchemy import Column, Integer, String, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column("id", Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column("email", VARCHAR(30), nullable=False)
    nama = Column("nama", String(50), nullable=False)
    password = Column("password", String(255), nullable=False)
    role_id = Column("role_id", ForeignKey("role.id"))
    user_role = relationship(
        "UserRole", backref="user_role_id", foreign_keys=[role_id]
	)