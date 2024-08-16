from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginSuccessResponse(BaseModel):
    id: str
    email: str
    token: str


class MeSuccessResponse(BaseModel):
    class Jabatan(BaseModel):
        id: str
        nama_jabatan: str

    id: str
    email: str
    nama: str
    jabatan: Jabatan


class LogoutSuccessResponse(BaseModel):
    id: str
    email: str
    token: str


class RefreshTokenSuccessResponse(BaseModel):
    refreshed_token: str


class RevokeTokenRequest(BaseModel):
    token: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
