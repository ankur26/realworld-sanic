from peewee import ForeignKeyField

from .article import Article
from .base import BaseModel
from .tag import Tag


class TagToArticle(BaseModel):
    articleid = ForeignKeyField(Article, field="id")
    tagid = ForeignKeyField(Tag, field="id")
