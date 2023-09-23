from peewee import ForeignKeyField
from .Base import BaseModel
from .Tags import Tags
from .Article import Article

class TagToArticle(BaseModel):
    articleid = ForeignKeyField(Article,field="id")
    tagid = ForeignKeyField(Tags,field="id")
