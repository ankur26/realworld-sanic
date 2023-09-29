from functools import wraps

from pydantic import ValidationError
from sanic import BadRequest,SanicException
from sanic.log import logger


def validate_data(validator_class, object_entry: str):
    # This is a generic attempt to try and validate as many requests we can in one class
    def decorator(f):
        @wraps(f)
        # Just a little bit of defensive programming
        async def wrapper(request, *args, **kwargs):
            logger.info("validate_data: validating {} object entry with {} class schema".format(object_entry,validator_class))
            if not request.json.get(object_entry, None):
                return BadRequest(
                    {
                        f"{object_entry}": "This key did not exist in the request body, make sure to add this"
                    }
                    ,
                    422,
                )
            else: # this is the main thing we're checking here
                try:
                    logger.info("validate_data: data check")
                    validated_data = validator_class(**request.json.get(object_entry))
                    logger.info("validate_data: going to next method")
                    res = await f(request, validated_data, *args, **kwargs)
                    return res
                except ValidationError as ve:
                    raise BadRequest(
                          "\n".join(
                                [
                                    f"{v['type']}-{v['loc'][0]}-{v['msg']}"
                                    for v in ve.errors()
                                ]
                            )
                        ,
                        422,
                    )
                except Exception as e:
                    raise SanicException(f"{e}", 500)

        return wrapper

    return decorator
