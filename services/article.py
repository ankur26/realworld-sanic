from sanic import Blueprint,SanicException,json
from models.Followers import Followers
from models.Article import Article
from models.Tags import Tags
from models.User import User
from models.TagToArticle import TagToArticle
from models.FavoritedArticlesByUser import FavoritedArticlesByUser
from helpers.serializer_helper import serialize_output
from middleware.requestcontentvalidator import validate_data
from middleware.requestvalidator import validate_request_body_exists,validate_request_object_exists_in_body,validate_authorization_token_exists,authorize
from schemas.ArticleValidationAndSerializationSchema import ArticleCreateType,ArticleOutputType
from playhouse.shortcuts import dict_to_model, model_to_dict
from peewee import IntegrityError


article_bp = Blueprint("article",url_prefix="/articles")



@article_bp.post("/",name="create_article")
@validate_request_body_exists
@validate_request_object_exists_in_body("article")
@validate_authorization_token_exists()
@authorize()
@validate_data(ArticleCreateType,"article")
async def create_article(request,validated_data:ArticleCreateType):
    current_user = request.ctx.user
    validated_data = validated_data.model_dump()
    validated_data["author"] = current_user["id"]
    article_cursor = dict_to_model(Article,validated_data,ignore_unknown=True)
    print("Reached the created cursor point as wel")
    try:
        #We need to create and article first, the tags then can be associated with 
        #Whose ID can be then be passed for us to create tags.
        article_id = article_cursor.save()
        if article_id:
            # print(article_id,article_cursor.id)
            taglist = validated_data["tagList"]
            for t in taglist:
                tag_cursor = Tags.get_or_none(tag=t)
                if not tag_cursor:
                    #We will create a tag here and get it's ID
                    tag_cursor = Tags(tag=t).save()
                #We now have the article ID and the tag ID at this point, now just add this entry to the tagToarticletable
                tag_to_article_id = TagToArticle(articleid=article_id,tagid=tag_cursor).save()
                if not tag_to_article_id:
                    print("Some error happened")
                #We now have a tag list, we now have a article entry
            article_output = model_to_dict(article_cursor)
            article_output["tagList"] = taglist
            article_output["author"] = current_user
            article_output["author"]["following"] = False
            print("Reacehed till this point")
            # print(article_output)
            return json(await serialize_output(ArticleOutputType,article_output,"article"))
    except IntegrityError as e:
        print (e)
        raise SanicException("The data had an error while being created",500)
    except Exception as e:
        print(e)
        raise SanicException("There is some unexpected error",500)


@article_bp.get("/<slug:str>",name="get_single_article")
@validate_authorization_token_exists(allow_anonymous=True)
@authorize()
async def get_article(request,slug):
    user = request.ctx.user
    try:

        article = model_to_dict(Article.get(Article.slug == slug))
        print(article)
        if article:
            # article_output = model_to_dict(article)
            article["favorited"] = FavoritedArticlesByUser.get_or_none(userid=user["id"],articleid=article['id']) is not None if user else False
            article["favoritesCount"] = FavoritedArticlesByUser.select(FavoritedArticlesByUser.articleid== article["id"]).count()
            # tag_predicate= TagToArticle.select(TagToArticle.articleid == article["id"] )
            tags = TagToArticle.select().join(
                Tags,on=(Tags.id==TagToArticle.tagid)).join(
                    Article, on=(Article.id==TagToArticle.articleid)).where(
                        Article.id==article["id"])
            article["tagList"] = [tag.tagid.tag for tag in tags]
            article["author"]["following"] = False if not user else Followers.get_or_none(userid=user.id,following=article["author"]["id"]) is not None
            return json(await serialize_output(ArticleOutputType,article,"article"))
    except IntegrityError as ie:
        print(ie)
        raise SanicException("There has been an an internal server error",500)
    except Exception as e:
        print(e)
        raise SanicException("Non database issue",500)

@article_bp.get("/",name="get_articles")
async def get_articles(request):
    return json(["Get articles soon here."])

@article_bp.get("/feed",name="get_feed")
@validate_authorization_token_exists()
@authorize()
async def get_feed(request):
    return json(["Get feed"])

