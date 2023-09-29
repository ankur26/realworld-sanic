from peewee import ForeignKeyField

from .Article import Article
from .Base import BaseModel
from .User import User


class FavoritedArticlesByUser(BaseModel):
    userid = ForeignKeyField(User, field="id")
    articleid = ForeignKeyField(Article, field="id")
