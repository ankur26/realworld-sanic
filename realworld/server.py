from os import getcwd, path

from peewee import SqliteDatabase
from sanic import Blueprint, Sanic, text
from sanic.log import logger

from .helpers.serializer_helper import serialize_error
from .models import article, articletag, comment, follower, tag, user, userfavorite
from .services.article_comment_service import article_bp
from .services.auth_service import auth_bp, user_bp
from .services.profile_service import profile_bp
from .services.tag_service import tag_bp


async def hello(request):
    return text("Welcome to app")


def create_app(test=False):
    # Initialize the app
    db_models = [
        user.User,
        follower.Follower,
        article.Article,
        comment.Comment,
        userfavorite.FavoritedArticlesByUser,
        tag.Tag,
        articletag.TagToArticle,
    ]
    app = Sanic("conduit")
    logger.info("Created app!")
    logger.info("Adding exception serializer")
    app.error_handler.add(Exception, serialize_error)

    logger.info("Adding Baseline route just to test a ping")
    app.add_route(hello, "/")

    logger.info(" Initialize the database in {}".format(getcwd()))
    db = (
        SqliteDatabase(path.join(getcwd(), "conduit.db"))
        if not test
        else SqliteDatabase(":memory:")
    )
    logger.info("Binding models to database")
    db.bind(db_models)
    logger.info("Database created in {}".format("conduit.db" if not test else "memory"))
    if test:
        logger.info("Dropping previous context for tests")
        db.drop_tables(db_models)
    logger.info("Creating tables / database structure if it does not exist")
    db.create_tables(models=db_models)
    logger.info("Make the api blueprint here")
    api = Blueprint.group(
        auth_bp, profile_bp, article_bp, tag_bp, user_bp, url_prefix="/api"
    )
    app.blueprint(api)
    logger.info("Sucessfully initialized app, ready to go!")
    return app
