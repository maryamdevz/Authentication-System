from pydantic import BaseModel, EmailStr, SecretStr, Field, ConfigDict, field_validator
import re 

class RegisterationSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    first_name: str = Field(min_length=2, max_length=30)
    last_name: str = Field(min_length=2, max_length=30)
    email: EmailStr 
    username: str = Field(min_length=2, max_length=30)
    password: SecretStr # use get_secret_value() before hashing
    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        password = value.get_secret_value()
    
        if len(password) < 8:
            raise ValueError("Password must contain at least 8 characters")
    
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain an uppercase letter")
    
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain a lowercase letter")
    
        if not re.search(r"[0-9]", password):
            raise ValueError("Password must contain a number")

        return value


class RegistrationResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    username: str

class LoginSchema(BaseModel):
    identifier: str 
    password: SecretStr

class LoginResponseSchema(BaseModel):
    token: str