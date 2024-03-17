import shared_functions
import re
import math

def generate_header(db_number):
    return str(f'''Tag Name,Address,Data Type,Respect Data Type,Client Access,Scan Rate,Scaling,Raw Low,Raw High,Scaled Low,Scaled High,Scaled Data Type,Clamp Low,Clamp High,Eng Units,Description,Negate Value
"Meteor.header.contexts.Stargate.placeholder",DB{db_number}.DBX0.0,Boolean,1,R,100,,,,,,,,,,,\n''')

def create_tag(name, data_type, db_number, current_index):
    prefix = '"Meteor.contexts.Stargate.Stargate1.'
    postfix = ',1,R/W,1000,,,,,,,,,,"",'
    data_type_abbriviation = {
        "dword": "DI",
        "dint": "DINT",
        "bool": "X",
        "int": "INT",
        "real": "D",
        "word": "W",
        "string": "STRING",
        "byte": "B"
    }
    name = name.lower()
    data_type = data_type.lower()
    if "spare" in name:
        return None, current_index
    
    if "array" in data_type:
        length = re.search(r'\[\s*(\d+)\s*\.\.\s*(\d+)\s*\]', data_type.replace(" ", "")).group(2)
        data_type = data_type.strip().split(' ')[-1].lower()
        current_index = math.ceil(current_index)
        output_string = f'{prefix}{name}",DB{db_number}.{data_type_abbriviation[data_type]}{current_index}[{length}],{data_type} Array{postfix}'
        new_index = shared_functions.calculate_new_position(data_type, length, current_index)
    
    elif "string" in data_type:
        current_index = math.ceil(current_index)
        length_of_string = data_type[data_type.index('[') + 1 : data_type.index(']')].strip()
        data_type = str(data_type[: data_type.index('[')]).strip().lower()
        output_string = f'{prefix}{name}",DB{db_number}.{data_type_abbriviation[data_type]}{current_index}.{length_of_string},{data_type}{postfix}'
        new_index = int(current_index) + int(length_of_string) + 2
    
    elif "byte" in data_type:
        data_type = data_type.strip().lower()
        current_index = math.ceil(current_index)
        output_string = f'{prefix}{name}",DB{db_number}.{data_type_abbriviation[data_type]}{current_index},{data_type}{postfix}'
        new_index = shared_functions.calculate_new_position(data_type, 1, current_index)
    
    elif "bool" in data_type:
        data_type = data_type.strip().lower()
        output_string = f'{prefix}{name}",DB{db_number}.{data_type_abbriviation[data_type]}{current_index},{data_type}{postfix}'
        new_index = shared_functions.calculate_new_position(data_type, 1, current_index)

    else:
        data_type = data_type.strip().lower()
        current_index = math.ceil(current_index)
        if current_index % 2 != 0: current_index +=1
        output_string = f'{prefix}{name}",DB{db_number}.{data_type_abbriviation[data_type]}{current_index},{data_type}{postfix}'
        new_index = shared_functions.calculate_new_position(data_type, 1, current_index)
    return output_string + "\n", new_index
