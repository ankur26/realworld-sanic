from .Base import BaseModel
from .User import User
from .Article import Article
from peewee import ForeignKeyField,CharField
from datetime import datetime


class Comments(BaseModel):
    createdAt=CharField(default=datetime.now().isoformat())
    updatedAt=CharField(default=datetime.now().isoformat())
    body=CharField()
    userid=ForeignKeyField(User,field="id")
    articleid=ForeignKeyField(Article,field="id")