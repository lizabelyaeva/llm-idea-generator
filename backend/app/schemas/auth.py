from pydantic import BaseModel, Field, field_validator


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(min_length=6, max_length=200)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        email = value.strip().lower()
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Некорректный email")
        return email


class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=1, max_length=200)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return value.strip().lower()


class UserResponse(BaseModel):
    id: int
    email: str


class AuthResponse(BaseModel):
    access_token: str
    user: UserResponse
