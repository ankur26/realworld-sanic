from peewee import ForeignKeyField
from .Base import BaseModel
from .User import User
from .Article import Article



class FavoritedArticlesByUser(BaseModel):
    userid = ForeignKeyField(User,field="id")
    articleid = ForeignKeyField(Article,field="id")