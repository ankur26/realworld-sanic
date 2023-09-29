from datetime import datetime

from peewee import CharField, ForeignKeyField

from .Article import Article
from .Base import BaseModel
from .User import User


class Comments(BaseModel):
    createdAt = CharField(default=datetime.utcnow().isoformat()[:-3] + "Z")
    updatedAt = CharField(default=datetime.utcnow().isoformat()[:-3] + "Z")
    body = CharField()
    userid = ForeignKeyField(User, field="id")
    articleid = ForeignKeyField(Article, field="id")
