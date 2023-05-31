import re
import yaml
import copy
from translating_formats.constants import TERMS_SEPARATOR


def iterate_recursive_ordered(data, path=None, result=[], variable_id=None):
    if path is None:
        path = []

    if isinstance(data, dict):
        for key, value in data.items():
            new_path = path + [key]
            if isinstance(value, (dict, list)):
                iterate_recursive_ordered(value, path=new_path, result=result)
            else:
                result.append(
                    {
                        "path": copy.deepcopy(new_path),
                        "ref_type": "dict",
                        "data_ref": data,
                        "key_ref": key,
                        "str_path": "->".join(new_path),
                        "original_value": value,
                    }
                )
    elif isinstance(data, list):
        for index, value in enumerate(data):
            new_path = path + [f"index:{str(index)}"]

            if isinstance(value, (dict, list)):
                iterate_recursive_ordered(value, path=new_path, result=result)
            else:
                result.append(
                    {
                        "path": copy.deepcopy(new_path),
                        "ref_type": "list",
                        "data_ref": data,
                        "key_ref": index,
                        "str_path": "->".join(new_path),
                        "original_value": value,
                    }
                )
    else:
        raise Exception(f"Unknown type iterate_recursive_ordered: {type(data)}")


def prepare_chunks(content, chunk_size):
    yml_data = yaml.safe_load(content)
    result = []
    variable_id = 1
    iterate_recursive_ordered(yml_data, result=result, variable_id=variable_id)

    chunks = []
    current_chunk = {"content": "", "lines": []}

    for line in result:
        current_value = line["original_value"]
        if current_value.strip() == "":
            continue

        new_content = f"{TERMS_SEPARATOR}\n{current_value}\n{TERMS_SEPARATOR}\n"

        if (
            len(current_chunk["content"]) + len(new_content) > chunk_size
            and current_chunk["content"] != ""
        ):
            chunks.append(current_chunk)
            current_chunk = {"content": "", "lines": []}

        current_chunk["content"] += new_content
        current_chunk["content"] = current_chunk["content"].replace(
            f"{TERMS_SEPARATOR}\n{TERMS_SEPARATOR}", TERMS_SEPARATOR
        )
        current_chunk["lines"].append(line)

    if current_chunk["content"] != "":
        chunks.append(current_chunk)

    return chunks, yml_data


def format_final_yml(resulting_chunks, original_yml):

    for chunk in resulting_chunks:
        index_line = 0

        for line in chunk["lines"]:
            resolve_line = chunk["resolved_lines"][index_line]
            line["data_ref"][line["key_ref"]] = resolve_line

            index_line += 1

    return yaml.safe_dump(original_yml, allow_unicode=True)
