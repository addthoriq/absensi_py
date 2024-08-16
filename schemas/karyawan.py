from typing import List, Annotated
from pydantic import BaseModel, StringConstraints, field_validator
from models import factory_session
from models.User import User


class PaginateKaryawanResponse(BaseModel):
    counts: int
    page_count: int
    page_size: int
    page: int

    class DetailKaryawanResponse(BaseModel):
        id: int
        email: str
        nama_karyawan: str

    result: List[DetailKaryawanResponse]


class DetailKaryawanResponse(BaseModel):
    id: int
    email: str
    nama_karyawan: str


class CreateKaryawanRequest(BaseModel):
    nama_karyawan: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    email: Annotated[str, StringConstraints(min_length=1, max_length=30)]
    password: Annotated[str, StringConstraints(min_length=1, max_length=50)]

    @field_validator("email")
    def validate_email_unique(cls, email):
        with factory_session() as session:
            existing_name = session.query(User).filter_by(email=email).first()
            if existing_name:
                raise ValueError("This email already exist!")
        return email


class CreateKaryawanResponse(BaseModel):
    id: str
    nama_karyawan: str
    email: str


class UpdateKaryawanRequest(BaseModel):
    nama_karyawan: str
    email: str


class UpdateKaryawanValidation(BaseModel):
    id: str
    email: Annotated[str, StringConstraints(min_length=1, max_length=30)]
    nama_karyawan: Annotated[str, StringConstraints(min_length=1, max_length=50)]

    @field_validator("email")
    def validate_email_unique(cls, email, value):
        current_id = value.data.get("id")
        if email is not None:
            with factory_session() as session:
                existing_user = (
                    session.query(User)
                    .filter(User.email == email, User.id is not current_id)
                    .first()
                )
                if existing_user:
                    raise ValueError("This email already exists!")
        return email


class UpdateKaryawanResponse(BaseModel):
    id: int
    nama_karyawan: str
    email: str


class ChangePasswordRequest(BaseModel):
    password: Annotated[str, StringConstraints(min_length=1, max_length=50)]
