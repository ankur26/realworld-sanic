from .Base import BaseModel
from .User import User
from .Article import Article
from peewee import ForeignKeyField,DateTimeField,CharField
from datetime import datetime


class Comments(BaseModel):
    createdAt=DateTimeField(default=datetime.now())
    updatedAt=DateTimeField(default=datetime.now())
    body=CharField()
    userid=ForeignKeyField(User,field="id")
    articleid=ForeignKeyField(Article,field="id")