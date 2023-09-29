
from sanic import Request, json
from sanic.log import logger


async def serialize_output(classtype, data, key):
    logger.info(f"Serialzing f{classtype}")
    return {key: classtype(**data).model_dump()}


async def merge_objects(input_data, output_data):
    logger.info(f"Merging objects")
    for key in input_data:
        if key not in output_data or input_data[key]:
            output_data[key] = input_data[key]
    return output_data


async def serialize_multiple(classtype, multidata, key, include_counts=False):
    logger.info(f"Serializing multiple of {classtype} ")
    data = (
        [(await serialize_output(classtype, data, key))[key] for data in multidata]
        if multidata
        else []
    )
    if include_counts:
        logger.info(f"Including counts for {classtype}")
        return {"{}s".format(key): data, "{}sCount".format(key): len(data)}
    return {
        "{}s".format(key): [
            (await serialize_output(classtype, data, key))[key] for data in multidata
        ]
        if multidata
        else []
    }


async def get_query_items(query_args):
    logger.info("Parsing query arguments")
    return {
        key: int(value) if key in ["limit", "offset"] else value
        for key, value in query_args
    }



async def serialize_error(request: Request, exception: Exception = None):
        logger.info(request)
        logger.error(exception)
        message = getattr(exception, "message", "Some error happened")
        status_code = getattr(exception, "status_code", 500)
        return json({
             "errors":{
                  "message":f"{message if message else exception}",
                  "exception":f"{exception}"
             }
        },status_code)
