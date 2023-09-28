async def serialize_output(classtype,data,key):
    # print(data)
    return {key:classtype(**data).model_dump()}

async def merge_objects(input_data,output_data):
    for key in input_data:
        if key not in  output_data or  input_data[key]:
            output_data[key] = input_data[key]
    return output_data

async def serialize_multiple(classtype,multidata,key,include_counts=False):
    data = [(await serialize_output(classtype,data,key))[key] for data in multidata] if multidata else []
    if include_counts:
        return {"{}s".format(key):data, "{}sCount".format(key):len(data)} 
    return {"{}s".format(key):[(await serialize_output(classtype,data,key))[key] for data in multidata] if multidata else []} 

async def get_query_items(query_args):
    return {key:int(value) if key in ['limit','offset'] else value for key,value in query_args}