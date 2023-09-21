from pydantic import BaseModel,AnyHttpUrl
from typing import Optional

class ProfileSerializer(BaseModel):
    username:str
    bio:Optional[str] = None
    image:Optional[AnyHttpUrl] = None
    following:Optional[bool] = False
