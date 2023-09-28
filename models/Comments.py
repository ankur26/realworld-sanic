from .Base import BaseModel
from .User import User
from .Article import Article
from peewee import ForeignKeyField,CharField
from datetime import datetime


class Comments(BaseModel):
    createdAt=CharField(default=datetime.utcnow().isoformat()[:-3]+"Z")
    updatedAt=CharField(default=datetime.utcnow().isoformat()[:-3]+"Z")
    body=CharField()
    userid=ForeignKeyField(User,field="id")
    articleid=ForeignKeyField(Article,field="id")