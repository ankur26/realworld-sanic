from peewee import CharField,TextField,ForeignKeyField
from datetime import datetime

from .Base import BaseModel
from .User import User

class Article(BaseModel):
    slug=CharField()
    title=CharField()
    description=CharField()
    body=TextField()
    author = ForeignKeyField(User,field="id")
    createdAt = CharField(default =datetime.utcnow().isoformat()[:-3]+"Z")
    updatedAt = CharField(default =datetime.utcnow().isoformat()[:-3]+"Z")
