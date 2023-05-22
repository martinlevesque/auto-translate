from translating_formats import yml
import copy
import yaml

SIMPLE_SAMPLE_YML_INPUT = """
key1: value1
alist:
    - value2
    - value3
deep_list:
    key4:
        - kk: value4
          jj: value5
"""


def test_translating_formats_yml_prepare_chunks_happy_path():
    chunks, yml_loaded = yml.prepare_chunks(SIMPLE_SAMPLE_YML_INPUT, 10)

    assert chunks == [
        {
            "content": "-=-=-\nvalue1\n-=-=-\n",
            "lines": [
                {
                    "path": ["key1"],
                    "ref_type": "dict",
                    "data_ref": {
                        "key1": "value1",
                        "alist": ["value2", "value3"],
                        "deep_list": {"key4": [{"kk": "value4", "jj": "value5"}]},
                    },
                    "key_ref": "key1",
                    "str_path": "key1",
                    "original_value": "value1",
                }
            ],
        },
        {
            "content": "-=-=-\nvalue2\n-=-=-\n",
            "lines": [
                {
                    "path": ["alist", "index:0"],
                    "ref_type": "list",
                    "data_ref": ["value2", "value3"],
                    "key_ref": 0,
                    "str_path": "alist->index:0",
                    "original_value": "value2",
                }
            ],
        },
        {
            "content": "-=-=-\nvalue3\n-=-=-\n",
            "lines": [
                {
                    "path": ["alist", "index:1"],
                    "ref_type": "list",
                    "data_ref": ["value2", "value3"],
                    "key_ref": 1,
                    "str_path": "alist->index:1",
                    "original_value": "value3",
                }
            ],
        },
        {
            "content": "-=-=-\nvalue4\n-=-=-\n",
            "lines": [
                {
                    "path": ["deep_list", "key4", "index:0", "kk"],
                    "ref_type": "dict",
                    "data_ref": {"kk": "value4", "jj": "value5"},
                    "key_ref": "kk",
                    "str_path": "deep_list->key4->index:0->kk",
                    "original_value": "value4",
                }
            ],
        },
        {
            "content": "-=-=-\nvalue5\n-=-=-\n",
            "lines": [
                {
                    "path": ["deep_list", "key4", "index:0", "jj"],
                    "ref_type": "dict",
                    "data_ref": {"kk": "value4", "jj": "value5"},
                    "key_ref": "jj",
                    "str_path": "deep_list->key4->index:0->jj",
                    "original_value": "value5",
                }
            ],
        },
    ]


def test_translating_formats_yml_format_final_yml():
    resulting_chunks, yml_loaded = yml.prepare_chunks(SIMPLE_SAMPLE_YML_INPUT, 10)
    original_yaml = copy.deepcopy(yml_loaded)
    resulting_chunks[0]['resolved_lines'] = ['frvalue1']
    resulting_chunks[1]['resolved_lines'] = ['frvalue2']
    resulting_chunks[2]['resolved_lines'] = ['frvalue3']
    resulting_chunks[3]['resolved_lines'] = ['frvalue4']
    resulting_chunks[4]['resolved_lines'] = ['frvalue5']

    result_yml = yml.format_final_yml(resulting_chunks, yml_loaded)

    original_yaml['alist'][0] = 'frvalue2'
    original_yaml['alist'][1] = 'frvalue3'
    original_yaml['deep_list']['key4'][0]['kk'] = 'frvalue4'
    original_yaml['deep_list']['key4'][0]['jj'] = 'frvalue5'
    original_yaml['key1'] = 'frvalue1'

    assert result_yml == yaml.dump(original_yaml, allow_unicode=True)
