from typing import Optional

from pydantic import AnyHttpUrl, BaseModel, EmailStr


class UserRegistration(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserLogin(BaseModel):
    email: str
    password: str


class UserOutput(BaseModel):
    id: int
    username: str
    email: str
    bio: Optional[str]
    image: Optional[AnyHttpUrl]
    token: str


class UserUpdate(BaseModel):
    id: Optional[
        int
    ] = None  # While this is optional, we definitely need to set it with the help of the user context which will be sent in the request.
    username: Optional[str] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[AnyHttpUrl] = None
    email: Optional[EmailStr] = None
