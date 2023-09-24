from peewee import CharField,TextField,ForeignKeyField
from datetime import datetime

from .Base import BaseModel
from .User import User

class Article(BaseModel):
    title=CharField()
    description=CharField()
    body=TextField()
    author = ForeignKeyField(User,field="id")
    createdAt = CharField(default = datetime.now().isoformat())
    updatedAt = CharField(default = datetime.now().isoformat())
