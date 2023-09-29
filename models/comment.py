from datetime import datetime

from peewee import CharField, ForeignKeyField

from .article import Article
from .base import BaseModel
from .user import User


class Comment(BaseModel):
    createdAt = CharField(default=datetime.utcnow().isoformat()[:-3] + "Z")
    updatedAt = CharField(default=datetime.utcnow().isoformat()[:-3] + "Z")
    body = CharField()
    userid = ForeignKeyField(User, field="id")
    articleid = ForeignKeyField(Article, field="id")
