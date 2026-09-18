from datetime import datetime
from typing import Optional
import re
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("Tên phòng ban không được để trống")
        return value


class DepartmentMemberItem(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    assigned_at: Optional[datetime] = None


class DepartmentResponse(DepartmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None
    members_count: int = 0
    members: list[DepartmentMemberItem] = []



class EmployeeDepartmentItem(BaseModel):
    id: int
    name: str
    assigned_at: Optional[datetime] = None


class EmployeeCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr
    department_ids: list[int] = []
    username: Optional[str] = None
    password: Optional[str] = None

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
    departments: list[EmployeeDepartmentItem] = []



class UserRegister(BaseModel):
    full_name: str
    phone: str
    email: EmailStr
    username: str
    password: str

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("Họ và tên không được để trống")
        if not re.fullmatch(r"[A-Za-zÀ-ỹĐđ\s]+", value):
            raise ValueError("Họ và tên chỉ được chứa chữ cái và khoảng trắng")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str):
        value = value.strip()
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Số điện thoại phải gồm đúng 10 chữ số")
        return value

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


class UserRoleUpdate(BaseModel):
    role: str  # "admin" hoặc "employee"


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: str = "employee"
    employee_id: Optional[int] = None
    created_at: Optional[datetime] = None
    employee_profile: Optional[EmployeeResponse] = None


class LoginResponse(BaseModel):
    message: str
    user: UserResponse