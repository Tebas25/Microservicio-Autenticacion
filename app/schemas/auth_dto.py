import re
from pydantic import BaseModel, EmailStr, Field, field_validator


class CreateUserDTO(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=16)
    complete_name: str = Field(min_length=25)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-!@#$%^&*(),.?\":{}|<>_]).+$"
        if not re.match(pattern, v):
            raise ValueError(
                "La contraseña debe incluir al menos una mayúscula, "
                "una minúscula, un número y un carácter especial."
            )

        return v
