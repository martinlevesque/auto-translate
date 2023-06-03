import os
import requests
from implementations.base import Base

CHUNK_SIZE_LIMIT = 1000
API_ENDPOINT_URL = os.environ.get(
    "LIBRETRANSLATE_URL", "https://translate.argosopentech.com/translate"
)


class Libretranslate(Base):
    def translate(self, chunks):
        return self.resolve_all_chunks_lines(chunks)

    def resolve_chunk_line(self, line):
        result = requests.post(
            API_ENDPOINT_URL,
            timeout=10,
            json={
                "q": line["original_value"],
                "source": self.source_language,
                "target": self.target_language,
            },
        )

        if not result.ok:
            raise Exception(
                f"Error while trying to translate line {line['original_value']}: {result.text}"
            )

        translated_text = result.json()["translatedText"]

        return translated_text


Klass = Libretranslate
