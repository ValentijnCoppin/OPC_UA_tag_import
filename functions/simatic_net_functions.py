import re
import shared_functions
import math

def generate_header(cu_number):
    header = f"""TagType;Level;ShortName;RTName;DataType;AccessRights;102;103\n\
B;1;CU{cu_number};;;\n\
B;2;meteor;;;\n\
B;3;header;;;\n\
B;4;sections;;;\n\
B;5;Stargate;;;\n\
B;3;sections;;;\n\
B;4;Stargate;;;\n\
B;5;Stargate1;;;
"""    

    return header

def create_tag(name, data_type, cu_number, db_number, current_index):
    data_type = data_type.lower().strip()
    name = name.lower()
    data_type_index = {
        "string": 8, 
        "bool": "B", 
        "int": 2, 
        "dint": 3, 
        "word": 12, 
        "dword": 13, 
        "array": 20, 
        "byte": 6, 
        "real": 5}

    if "spare" in name:
        return None, current_index
    
    if "string" in data_type:
        current_index = math.ceil(current_index)
        length_of_string = data_type[data_type.index('[') + 1 : data_type.index(']')]
        data_type = data_type[: data_type.index('[')].strip()
        output_string = f"""L;6;{name};S7:[{cu_number}]DB{db_number},string{current_index}.{length_of_string};{data_type_index[data_type]};RW;0;0"""    
        new_index = int(current_index) + int(length_of_string) + 2
    elif "bool" in data_type:
        output_string = f"""L;6;{name};S7:[{cu_number}]DB{db_number},X{current_index};{data_type_index[data_type]};RW;0;0"""
        new_index = shared_functions.calculate_new_position(data_type, 1, current_index)
    elif "array" in data_type:
        length = re.search(r'\[\s*(\d+)\s*\.\.\s*(\d+)\s*\]', data_type).group(2)
        data_type = data_type.split(' ')[-1].strip()
        current_index = math.ceil(current_index) if data_type != "bool" else current_index
        output_string = f"""L;6;{name};S7:[{cu_number}]DB{db_number},{data_type}{current_index},{length};{data_type_index["array"]}{data_type_index[data_type]};RW;0;0\n"""
        new_index = shared_functions.calculate_new_position(data_type, length, current_index)
        for i in range(int(length)):
            sub_tag, new_index = create_tag(f"{name}[{i}]", data_type, cu_number, db_number, new_index)
            output_string = output_string + sub_tag
        output_string = output_string[:-1] # remove the unwanted newline at the end of the last subtag
    else:
        current_index = math.ceil(current_index)
        if current_index % 2 != 0 and data_type != "byte": current_index +=1
        output_string = f"""L;6;{name};S7:[{cu_number}]DB{db_number},{data_type}{current_index};{data_type_index[data_type]};RW;0;0"""
        new_index = shared_functions.calculate_new_position(data_type, 1, current_index)
    return output_string + "\n", new_index
