from functools import wraps

from sanic import BadRequest, SanicException, Unauthorized
from sanic.log import logger

from helpers.jwt_token_helper import check_token_and_return_status


def validate_request_body_exists(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        logger.info("validate_request_body_exists: checking body")
        if not request.body:
            raise BadRequest({"body": "Cannot be empty"}, 422)
        return await func(request, *args, **kwargs)

    return wrapper


def validate_request_object_exists_in_body(key):
    # def validate_request_user_exists_in_body():
    def decorator(func):
        @wraps(func)
        async def wrapper(request, *args, **kwargs):
            logger.info(
                "validate_request_object_exists_in_body: checking body for {key} object"
            )
            if not request.json.get(key, None):
                raise BadRequest({"body": f"{key} cannot be empty"}, 422)
            res = await func(request, *args, **kwargs)
            return res

        return wrapper

    return decorator


def validate_authorization_token_exists(allow_anonymous=False):
    def dec(func):
        @wraps(func)
        async def wrapper(request, *args, **kwargs):
            logger.info("validate_authorization_token_exists: checking token exists")
            auth_header = request.headers.get("Authorization", None)

            if auth_header:
                if not auth_header.startswith("Bearer ") and not auth_header.startswith(
                    "Token "
                ):
                    raise BadRequest(
                        {"header": "Authorization missing bearer or token prefix"},
                        401,
                    )
                logger.info(
                    "validate_authorization_token_exists: going to next method with auth header"
                )
                res = await func(request, *args, **kwargs)
            else:
                if allow_anonymous:
                    logger.info(
                        "validate_authorization_token_exists: allowed anonymous route"
                    )
                    res = await func(request, *args, **kwargs)
                else:
                    raise Unauthorized({"headers": "Missing Bearer token"}, 403)

            return res

        return wrapper

    return dec


def authorize():
    def decorator(func):
        @wraps(func)
        async def wrapper(request, *args, **kwargs):
            logger.info("authorize:getting bearer token")
            bearer_token = request.headers.get("Authorization", None)
            if bearer_token:
                bearer_token = bearer_token.replace("Bearer ", "").replace("Token ", "")
                token_check_output = await check_token_and_return_status(bearer_token)
                if token_check_output["valid_token"]:
                    user = token_check_output["token_user"]
                    user["token"] = bearer_token
                    request.ctx.user = user
                else:
                    raise SanicException(
                        token_check_output["error"],
                        status_code=token_check_output["return_status_code"],
                    )
            elif not bearer_token:
                request.ctx.user = None
            logger.info("authorize: moving to next function")
            res = await func(request, *args, **kwargs)
            return res

        return wrapper

    return decorator
