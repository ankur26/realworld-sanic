from peewee import ForeignKeyField

from .Article import Article
from .Base import BaseModel
from .Tags import Tags


class TagToArticle(BaseModel):
    articleid = ForeignKeyField(Article, field="id")
    tagid = ForeignKeyField(Tags, field="id")
