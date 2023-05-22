import re
import yaml
import copy
from translating_formats.constants import TERMS_SEPARATOR


# var -> val

def iterate_recursive_ordered(data, path=None, result=[]):
    if path is None:
        path = []

    if isinstance(data, dict):
        for key, value in data.items():
            new_path = path + [key]
            if isinstance(value, (dict, list)):
                iterate_recursive_ordered(value, path=new_path, result=result)
            else:
                result.append({
                    "path": copy.deepcopy(new_path),
                    "str_path": '->'.join(new_path),
                    "original_value": value
                })
    elif isinstance(data, list):
        for index, value in enumerate(data):
            new_path = path + [f"index:{str(index)}"]

            if isinstance(value, (dict, list)):
                iterate_recursive_ordered(value, path=new_path, result=result)
            else:
                result.append({
                    "path": copy.deepcopy(new_path),
                    "str_path": '->'.join(new_path),
                    "original_value": value
                })
    else:
        raise Exception(f"Unknown type iterate_recursive_ordered: {type(data)}")


def prepare_chunks(content, chunk_size):
    yml_data = yaml.safe_load(content)
    result = []
    iterate_recursive_ordered(yml_data, result=result)
    print(f"result = {result}")

    chunks = []
    current_chunk = {
        "content": "",
        "lines": []
    }

    for line in result:
        current_value = line['original_value']
        if current_value.strip() == "":
            continue

        new_content = f"{TERMS_SEPARATOR}\n{current_value}\n{TERMS_SEPARATOR}\n"

        if len(current_chunk['content']) + len(new_content) > chunk_size:
            chunks.append(current_chunk)
            current_chunk = {
                "content": "",
                "lines": []
            }

        current_chunk['content'] += new_content
        current_chunk['content'] = current_chunk['content'].replace(
            f"{TERMS_SEPARATOR}\n{TERMS_SEPARATOR}", TERMS_SEPARATOR
        )
        current_chunk['lines'].append(copy.deepcopy(line))

    if current_chunk['content'] != "":
        chunks.append(current_chunk)

    return chunks


def format_final_yml(resulting_chunks):
    dict_result = {}

    for chunk in resulting_chunks:
        index_line = 0

        for line in chunk['lines']:

            current_path_dict_part = dict_result

            index_path = 0

            for path_part in line['path']:
                if path_part not in current_path_dict_part:
                    current_path_dict_part[path_part] = {}

                if index_path == len(line['path']) - 1:
                    resolve_line = chunk['resolved_lines'][index_line]
                    current_path_dict_part[path_part] = resolve_line
                else:
                    current_path_dict_part = current_path_dict_part[path_part]

                index_path += 1

            index_line += 1

    return yaml.dump(dict_result, allow_unicode=True)
