from translating_formats import json as translating_json
import json


SIMPLE_SAMPLE_JSON_INPUT = json.dumps(
    {
        "key1": "value1",
        "alist": ["value2", "value3"],
        "deeplist": {"key4": [{"kk": "value4", "jj": "value5"}]},
    }
)


def test_translating_formats_json_prepare_chunks_happy_path():
    chunks, yml_loaded = translating_json.Json().prepare_chunks(
        SIMPLE_SAMPLE_JSON_INPUT, 10
    )

    assert chunks == [
        {
            "content": "value1 ",
            "lines": [
                {
                    "path": ["key1"],
                    "ref_type": "dict",
                    "data_ref": {
                        "key1": "value1",
                        "alist": ["value2", "value3"],
                        "deeplist": {"key4": [{"kk": "value4", "jj": "value5"}]},
                    },
                    "key_ref": "key1",
                    "str_path": "key1",
                    "original_value": "value1",
                }
            ],
        },
        {
            "content": "value2 ",
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
            "content": "value3 ",
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
            "content": "value4 ",
            "lines": [
                {
                    "path": ["deeplist", "key4", "index:0", "kk"],
                    "ref_type": "dict",
                    "data_ref": {"kk": "value4", "jj": "value5"},
                    "key_ref": "kk",
                    "str_path": "deeplist->key4->index:0->kk",
                    "original_value": "value4",
                }
            ],
        },
        {
            "content": "value5 ",
            "lines": [
                {
                    "path": ["deeplist", "key4", "index:0", "jj"],
                    "ref_type": "dict",
                    "data_ref": {"kk": "value4", "jj": "value5"},
                    "key_ref": "jj",
                    "str_path": "deeplist->key4->index:0->jj",
                    "original_value": "value5",
                }
            ],
        },
    ]


def test_translating_formats_json_is_proper_format_happy_path():
    assert translating_json.Json.is_proper_format(SIMPLE_SAMPLE_JSON_INPUT)


def test_translating_formats_json_is_proper_format_with_invalid_content():
    assert not translating_json.Json.is_proper_format('{ "asd: asdf }')
