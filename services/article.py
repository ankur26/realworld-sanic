from sanic import Blueprint,SanicException,json
from models.Followers import Followers
from models.Article import Article
from models.Tags import Tags
from models.TagToArticle import TagToArticle
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

