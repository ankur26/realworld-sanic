from sanic import Blueprint,json,text
from models.User import User
from models.Followers import Followers
from playhouse.shortcuts import model_to_dict,dict_to_model
from helpers.serializer_helper import serialize_output
from middleware.requestvalidator import validate_authorization_token_exists,authorize
from schemas.ProfileSerializationSchemas import ProfileSerializer
profile_bp = Blueprint("profiles",url_prefix="/profiles")

@profile_bp.get("/<username:str>")
@validate_authorization_token_exists(allow_anonymous_context=True)
@authorize(allow_anonymous_context=True)
async def get_profile(request,username):
    curr_user = request.ctx.user
    # current_user = User.get_or_none(current_user_id)
    profile_to_lookup=  User.get_or_none(username=username)
    if not profile_to_lookup:
        return json({
            "error":"Username does not exist"
        },422)
    profile_to_lookup = model_to_dict(profile_to_lookup)
    if curr_user:
        current_user_id = curr_user.get("id")
        profile_to_lookup["following"] = Followers.get_or_none(current = current_user_id ,following=profile_to_lookup.id ) == None
    return  json(await serialize_output(ProfileSerializer,profile_to_lookup,key="profile"))    
    # return text("You are at the profiles route.")

        
        