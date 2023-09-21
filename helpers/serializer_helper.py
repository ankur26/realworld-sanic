async def serialize_output(classtype,data,key):
    # print(data)
    return {key:classtype(**data).model_dump()}

async def merge_objects(input_data,output_data):
    for key in output_data:
        if key in input_data and not output_data[key]:
            output_data[key] = input_data[key]
    return output_data
