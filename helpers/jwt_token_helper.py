from datetime import datetime, timedelta
from os import getenv

from jwt import decode, encode
from jwt.exceptions import *
from playhouse.shortcuts import model_to_dict
from sanic.log import logger

from models.user import User


async def get_token(user: dict) -> (bool, str | None):
    logger.info("get_token")
    logger.info(f"Getting token for user{user['username']}")
    key = getenv("JWT_SECRET") if getenv("JWT_SECRET") else "DevelopmentJWT"
    claims = {
        "iss": "conduit-sanic",
        "iat": datetime.now().timestamp(),
        "exp": (datetime.now() + timedelta(days=60)).timestamp(),
        "sub": user["username"],
        "aud": "user",
        "id": user["id"],
    }
    try:
        token = encode(payload=claims, key=key)
        logger.info("Generated token successfully")
        return True, token
    except Exception as e:
        logger.error(e)
        return False, None


async def invalidate_token(output, exception, error_code):
    logger.error(exception)
    output["return_status_code"] = error_code
    output["error"] = f"{exception}"
    output["valid_token"] = False
    return output


async def check_token_and_return_status(token: str):
    key = getenv("JWT_SECRET") if getenv("JWT_SECRET") else "DevelopmentJWT"
    output = {
        "valid_token": True,
        "error": None,
        "return_status_code": 200,
        "token_user": None,
    }
    try:
        claims = decode(
            jwt=token,
            key=key,
            algorithms=["HS256"],
            audience="user",
            issuer="conduit-sanic",
        )
        user_name = claims["sub"]
        user_id = claims["id"]
        user_from_id = User.get_or_none(id=user_id)
        user_from_username = User.get_or_none(username=user_name)
        if not user_from_id:
            raise ValueError("The id in the claim does not exist")
        if not user_from_username:
            raise ValueError("The user from the claim does not exist")
        # This is just a baseline token check to ensure that the token was not tampered with
        # I would say that this is not needed but it would be better to have as a measure.
        if (
            user_from_id.id == user_from_username.id
            and user_from_id.username == user_from_username.username
        ):
            output["token_user"] = model_to_dict(user_from_id, exclude=["password"])
            return output
        else:
            raise ValueError("It looks like the token claims were tampered with")
    except DecodeError as de:
        return await invalidate_token(output, de, 500)
    except InvalidIssuerError as iie:
        return await invalidate_token(output, iie, 403)
    except InvalidIssuedAtError as iiae:
        return await invalidate_token(output, iiae, 403)
    except MissingRequiredClaimError as mrce:
        return await invalidate_token(output, mrce, 403)
    except InvalidSignatureError as ise:
        return await invalidate_token(output, ise, 403)
    except ExpiredSignatureError as ese:
        return await invalidate_token(output, ese, 403)
    except InvalidAudienceError as iae:
        return await invalidate_token(output, iae, 403)
    except InvalidTokenError as ite:
        # this is just a generic base class for all exceptions/ if it
        # reaches here we don't know whether the token was tampered with
        # or whether the error came when decoding, regardless it should forbid any access
        return await invalidate_token(output, ite, 403)
    except ValueError as ve:
        # This will be for any validation errors that happen
        return await invalidate_token(output, ve, 403)
