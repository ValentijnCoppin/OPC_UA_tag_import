import math

def tag_export_to_dict(file_path):
    # Define a dictionary to store the data
    data_block = {}
    # Open the text file
    with open(file_path, 'r') as file:
        key_list = []
        structured_data = {}
        for line in file:
            line = line.split("//")[0].strip()  # split("//")[0] removes all the comments, strip() removes all the leading and trailing spaces
            line = line.split(":=")[0].strip()
            if "DATA_BLOCK" in line.upper() and not "END" in line.upper():
                db = line.split(" ")[-1]
            if not line:
                continue
            if "STRUCT" in line.upper():
                if line.upper() == "STRUCT":
                    key_list.append("main_key")
                    structured_data[key_list[-1]] = {}

                elif line.upper().startswith("END_STRUCT"):
                    key_list.pop()
                    
                else:
                    key_list.append(line.split(':')[0].strip())
                    set_nested_value(source_dict=structured_data,
                                     key_list=key_list,
                                     value={key_list[-1]: {}})

            elif key_list: # add tags to the current struct if a struct exists
                if len(key_list) == 1:
                    key, value = line.split(':')
                    structured_data[key_list[-1]].update({key.strip(): value.replace(";", "").strip()})
                elif len(key_list) == 2:
                    key, value = line.split(':')
                    structured_data[key_list[-2]][key_list[-1]].update({key.strip(): value.replace(";", "").strip()})
                elif len(key_list) == 3:
                    key, value = line.split(':')
                    structured_data[key_list[-3]][key_list[-2]][key_list[-1]].update({key.strip(): value.replace(";", "").strip()})
    return structured_data, db

def calculate_new_position(datatype, amount, index):
        data_type_bits = {
            'bool': 1,
            'byte': 8,
            'int': 16,
            'word': 16,
            'dint': 32,
            'dword': 32,
            'real': 32,
            'sint': 8,
        }
        if datatype not in data_type_bits:
            raise ValueError(f"Invalid data type: {datatype}")
        rest_amount_of_bits = round((index % 1) * 10)
        total_bits_to_add = (rest_amount_of_bits + (int(amount) * int(data_type_bits[datatype])))
        bytes_to_add = total_bits_to_add // 8
        bits_to_add = total_bits_to_add % 8
        new_position = math.floor(index) + bytes_to_add + (bits_to_add / 10)
        return round(new_position, 1)

def yield_key_value_from_nested_dict(tag_dict):
    for key, value in tag_dict.items():
        if isinstance(value, dict):
            yield from yield_key_value_from_nested_dict(value)
        else:
            yield key, value

def round_up_to_next_even(number):
    if number % 2 == 0:
        return math.ceil(number)
    else:
        return math.ceil(number / 2) * 2


def set_nested_value(source_dict, key_list, value):
    def _set_value(d, keys, v):
        if len(keys) == 1:
            d[keys[0]] = v
        else:
            if keys[0] not in d:
                d[keys[0]] = {}
            _set_value(d[keys[0]], keys[1:], v)

    result_dict = source_dict.copy()
    _set_value(result_dict, key_list, value)
    return result_dict

