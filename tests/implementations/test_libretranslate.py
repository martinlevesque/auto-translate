from implementations import libretranslate


def test_implementations_libretranslate_happy_path(requests_mock):
    requests_mock.post(
        libretranslate.API_ENDPOINT_URL,
        json={
            "translatedText": "Bonjour le monde",
        },
    )

    implementation = libretranslate.Klass(target_language="french")

    chunks = [
        {
            "lines": [
                {
                    "original_value": "Hello world",
                },
                {
                    "original_value": "My test",
                },
            ],
        }
    ]

    resulting_chunks = implementation.translate(chunks)

    assert resulting_chunks == [
        {
            "lines": [{"original_value": "Hello world"}, {"original_value": "My test"}],
            "resolved_lines": ["Bonjour le monde", "Bonjour le monde"],
        }
    ]
