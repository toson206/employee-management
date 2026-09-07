from datetime import datetime
from typing import Optional
import re
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class EmployeeCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("Tên nhân viên không được để trống")
        if not re.fullmatch(r"[A-Za-zÀ-ỹĐđ\s]+", value):
            raise ValueError("Tên nhân viên chỉ được chứa chữ cái và khoảng trắng")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str):
        value = value.strip()
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Số điện thoại phải gồm đúng 10 chữ số")
        return value


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str
    email: EmailStr
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserRegister(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("Username không được để trống")
        if len(value) < 3:
            raise ValueError("Username phải có ít nhất 3 ký tự")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if len(value) < 6:
            raise ValueError("Mật khẩu phải có ít nhất 6 ký tự")
        return value


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    created_at: Optional[datetime] = None


class LoginResponse(BaseModel):
    message: str
    user: UserResponse