from typing import List, Annotated, Optional
from pydantic import BaseModel, StringConstraints, field_validator
from models import factory_session
from models.User import User


class PaginateUserResponse(BaseModel):
    count: int
    page_count: int
    page_size: int
    page: int

    class DetailUserResponse(BaseModel):
        id: int
        email: str
        nama_user: str

        class DetailJabatan(BaseModel):
            id: int
            nama_jabatan: str

        jabatan: Optional[DetailJabatan]

    results: List[DetailUserResponse]


class DetailUserResponse(BaseModel):
    id: int
    email: str
    nama_user: str

    class DetailJabatan(BaseModel):
        id: int
        nama_jabatan: str

    jabatan: Optional[DetailJabatan]


class CreateUserRequest(BaseModel):
    nama_user: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    email: Annotated[str, StringConstraints(min_length=1, max_length=30)]
    password: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    jabatan: int

    @field_validator("email")
    def validate_email_unique(cls, email):
        with factory_session() as session:
            existing_name = session.query(User).filter_by(email=email).first()
            if existing_name:
                raise ValueError("This email already exist!")
        return email


class CreateUserResponse(BaseModel):
    id: str
    nama_user: str
    email: str

    class DetailJabatan(BaseModel):
        id: int
        nama_jabatan: str

    jabatan: Optional[DetailJabatan]


class UpdateUserRequest(BaseModel):
    nama_user: str
    email: str
    jabatan: int


class UpdateUserValidation(BaseModel):
    id: str
    email: Annotated[str, StringConstraints(min_length=1, max_length=30)]
    nama_user: Annotated[str, StringConstraints(min_length=1, max_length=50)]

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


class UpdateUserResponse(BaseModel):
    id: int
    nama_user: str
    email: str

    class DetailJabatan(BaseModel):
        id: int
        nama_jabatan: str

    jabatan: Optional[DetailJabatan]


class ChangePasswordRequest(BaseModel):
    password: Annotated[str, StringConstraints(min_length=1, max_length=50)]


class PaginateJabatanResponse(BaseModel):
    counts: int
    page_count: int
    page_size: int
    page: int

    class DetailJabatan(BaseModel):
        id: int
        nama_jabatan: str

    jabatan: Optional[DetailJabatan]
