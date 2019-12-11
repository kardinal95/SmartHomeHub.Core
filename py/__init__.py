type_map = {
    'str': str,
    'int': int
}


def convert_to_type(value, value_type):
    return type_map[value_type](value)