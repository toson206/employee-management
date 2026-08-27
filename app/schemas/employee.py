
from pydantic import BaseModel, EmailStr, field_validator
import re


class EmployeeCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Tên nhân viên không được để trống")

        if not re.fullmatch(r"[A-Za-zÀ-ỹĐđ\s]+", value):
            raise ValueError(
                "Tên nhân viên chỉ được chứa chữ cái "
            )

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError(
                "Số điện thoại gồm 10 chữ số"
            )

        return value


class EmployeeResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: EmailStr

    class Config:
        from_attributes = True
