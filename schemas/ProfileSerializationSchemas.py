from typing import Optional

from pydantic import AnyHttpUrl, BaseModel


class ProfileSerializer(BaseModel):
    username: str
    bio: Optional[str] = None
    image: Optional[AnyHttpUrl] = None
    following: Optional[bool] = False
