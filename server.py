from peewee import SqliteDatabase
from sanic import Blueprint, Sanic, text
from sanic.log import logger

from helpers.serializer_helper import serialize_error
from models import *
from services.articleandcomment import article_bp
from services.auth import auth_bp, user_bp
from services.profile import profile_bp
from services.tag import tag_bp


async def hello(request):
    return text("Welcome to app")


def create_app():
    # Initialize the app
    app = Sanic("conduit")
    logger.info("Created app!")
    logger.info("Adding exception serializer")
    app.error_handler.add(Exception, serialize_error)

    logger.info("Adding Baseline route just to test a ping")
    app.add_route(hello, "/")

    logger.info(" Initialize the database")
    db = SqliteDatabase("conduit.db")
    logger.info("Creating tables / database structure if it does not exist")
    db.create_tables(
        models=[
            User.User,
            Followers.Followers,
            Article.Article,
            Comments.Comments,
            FavoritedArticlesByUser.FavoritedArticlesByUser,
            Tags.Tags,
            TagToArticle.TagToArticle,
        ]
    )
    logger.info("Make the api blueprint here")
    api = Blueprint.group(
        auth_bp, profile_bp, article_bp, tag_bp, user_bp, url_prefix="/api"
    )
    app.blueprint(api)
    logger.info("Sucessfully initialized app, ready to go!")
    return app
