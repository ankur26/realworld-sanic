from datetime import datetime

from peewee import CharField, ForeignKeyField, Model

from .article import Article
from .user import User


class Comment(Model):
    createdAt = CharField(default=datetime.utcnow().isoformat()[:-3] + "Z")
    updatedAt = CharField(default=datetime.utcnow().isoformat()[:-3] + "Z")
    body = CharField()
    userid = ForeignKeyField(User, field="id")
    articleid = ForeignKeyField(Article, field="id")
