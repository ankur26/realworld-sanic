from pydantic import BaseModel,computed_field
from typing import List,Optional
from slugify import slugify
from .ProfileSerializationSchemas import ProfileSerializer

class ArticleCreateType(BaseModel):
    title:str
    description:str
    body:str
    tagList:Optional[List[str]] = []


class ArticleOutputType(BaseModel):
    @computed_field
    def slug(self)->str:
        return slugify(self.title)
    title:str
    description:str
    body:str
    tagList:Optional[List[str]] = []
    createdAt:str
    updatedAt:str
    author:ProfileSerializer
    