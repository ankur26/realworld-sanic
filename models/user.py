from peewee import BlobField, CharField

from .base import BaseModel


class User(BaseModel):
    username = CharField(unique=True)
    password = BlobField()
    email = CharField(unique=True)
    bio = CharField(null=True)
    image = CharField(null=True)
