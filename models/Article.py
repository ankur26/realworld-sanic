from peewee import CharField,TextField,ForeignKeyField,DateTimeField
from datetime import datetime

from .Base import BaseModel
from .User import User

class Article(BaseModel):
    title=CharField()
    description=CharField()
    body=TextField()
    author = ForeignKeyField(User,field="id")
    createdAt = DateTimeField(default = datetime.now)
    updatedAt = DateTimeField(default = datetime.now)
