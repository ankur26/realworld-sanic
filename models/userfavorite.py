from peewee import ForeignKeyField

from .article import Article
from .base import BaseModel
from .user import User


class FavoritedArticlesByUser(BaseModel):
    userid = ForeignKeyField(User, field="id")
    articleid = ForeignKeyField(Article, field="id")
