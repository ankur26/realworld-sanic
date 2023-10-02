from playhouse.shortcuts import model_to_dict
from sanic import Blueprint, NotFound, SanicException, json
from sanic.log import logger

from ..helpers.serializer_helper import serialize_output
from ..middleware.request_header_and_body_validator import (
    authorize,
    validate_authorization_token_exists,
)
from ..models.follower import Follower
from ..models.user import User
from ..schemas.profile_schema import ProfileSerializer

profile_bp = Blueprint("profiles", url_prefix="/profiles")


@profile_bp.get("/<username:str>", name="get_profile")
@validate_authorization_token_exists(allow_anonymous=True)
@authorize()
async def get_profile(request, username):
    logger.info("get_profile")
    curr_user = request.ctx.user
    profile_to_lookup = User.get_or_none(username=username)
    if not profile_to_lookup:
        return NotFound("Username does not exist")
    logger.info("get_profile:found profile")
    profile_to_lookup = model_to_dict(profile_to_lookup)
    if curr_user:
        logger.info("get_profile:authorized route")
        current_user_id = curr_user.get("id")
        profile_to_lookup["following"] = (
            Follower.get_or_none(
                current=current_user_id, following=profile_to_lookup["id"]
            )
            is not None
        )
    else:
        logger.info("get_profile:anonymouse route")
        profile_to_lookup["following"] = False
    return json(
        await serialize_output(ProfileSerializer, profile_to_lookup, key="profile")
    )


@profile_bp.post("/<username:str>/follow", name="follow_user")
@validate_authorization_token_exists()
@authorize()
async def follow_user(request, username):
    logger.info("follow_user")
    curr_user = request.ctx.user
    profile_to_lookup = model_to_dict(User.get_or_none(username=username))
    if not profile_to_lookup or not curr_user:
        raise NotFound({"errors": "User or profile to follow not found"}, 404)
    try:
        logger.info("follow_user:profile found, attempting follow")
        follower = Follower.get_or_none(
            current=curr_user["id"], following=profile_to_lookup["id"]
        )
        if not follower:
            Follower(current=curr_user["id"], following=profile_to_lookup["id"]).save()
        profile_to_lookup["following"] = True
        logger.info("follow_user: returning profile")
        return json(
            await serialize_output(ProfileSerializer, profile_to_lookup, key="profile")
        )
        # profile_to_lookup = model_to_dict(profile_to_lookup)
    except Exception as e:
        raise SanicException(f"Something went wrong {e}", 500)


@profile_bp.delete("/<username:str>/follow", name="unfollow_user")
@validate_authorization_token_exists()
@authorize()
async def unfollow_user(request, username):
    logger.info("unfollow_user")
    try:
        user_id = request.ctx.user["id"]
        profile_to_unfollow_id = User.get_or_none(username=username)
        if profile_to_unfollow_id:
            logger.info("unfollow_user: user profile found")
            following_id = Follower.get_or_none(
                current=user_id, following=profile_to_unfollow_id.id
            )
            if following_id:
                logger.info("unfollow_user: profile link found")
                Follower.delete_by_id(following_id)
            profile_to_lookup = model_to_dict(User.get_by_id(profile_to_unfollow_id))
            profile_to_lookup["following"] = False
            logger.info("returning updated profile")
            return json(
                await serialize_output(
                    ProfileSerializer, profile_to_lookup, key="profile"
                )
            )
    except Exception as e:
        raise SanicException("Something went wrong", 500)
