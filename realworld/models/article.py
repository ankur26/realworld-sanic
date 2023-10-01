from datetime import datetime

from peewee import CharField, ForeignKeyField, Model, TextField

from .user import User


class Article(Model):
    slug = CharField()
    title = CharField()
    description = CharField()
    body = TextField()
    author = ForeignKeyField(User, field="id")
    createdAt = CharField(default=datetime.utcnow().isoformat()[:-3] + "Z")
    updatedAt = CharField(default=datetime.utcnow().isoformat()[:-3] + "Z")
