from datetime import datetime

from peewee import CharField, ForeignKeyField, TextField

from .base import BaseModel
from .user import User


class Article(BaseModel):
    slug = CharField()
    title = CharField()
    description = CharField()
    body = TextField()
    author = ForeignKeyField(User, field="id")
    createdAt = CharField(default=datetime.utcnow().isoformat()[:-3] + "Z")
    updatedAt = CharField(default=datetime.utcnow().isoformat()[:-3] + "Z")
