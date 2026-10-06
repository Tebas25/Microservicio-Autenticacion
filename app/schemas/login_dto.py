import re
from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel, EmailStr, Field, field_validator


class LoginDTO(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        try:
            result = validate_email(v, check_deliverability=False)
            return result.normalized
        except EmailNotValidError as e:
            raise ValueError(f"El correo electrónico no es válido: {str(e)}")
