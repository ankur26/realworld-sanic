from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, computed_field
from slugify import slugify

from .profile_schema import ProfileSerializer


class ArticleCreateType(BaseModel):
    title: str
    description: str
    body: str
    tagList: Optional[List[str]] = []

    @computed_field
    def slug(self) -> str:
        return slugify(self.title)


class ArticleOutputType(BaseModel):
    @computed_field
    def slug(self) -> str:
        return slugify(self.title)

    title: str
    description: str
    body: str
    tagList: Optional[List[str]] = []
    createdAt: str
    updatedAt: str
    author: ProfileSerializer
    favorited: Optional[bool] = False
    favoritesCount: Optional[int] = 0


class ArticleUpdateType(BaseModel):
    @computed_field
    def slug(self) -> str:
        return slugify(self.title)

    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None
    tagList: Optional[List[str]] = []
    updatedAt: Optional[str] = datetime.utcnow().isoformat()[:-3] + "Z"


class CommentCreateType(BaseModel):
    body: str


class CommentOutputType(BaseModel):
    id: int
    createdAt: str
    updatedAt: str
    body: str
    author: ProfileSerializer
