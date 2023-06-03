from tenacity import retry, stop_after_attempt
from implementations.base import Base
import requests

CHUNK_SIZE_LIMIT = 1000
API_ENDPOINT_URL = "https://translate.argosopentech.com/translate"

class Libretranslate(Base):

    def translate(self, chunks):
        resulting_chunks = []

        for chunk in chunks:
            resolved_lines = self.resolve_chunk(chunk)
            translated_chunk = chunk
            translated_chunk["resolved_lines"] = resolved_lines
            resulting_chunks.append(translated_chunk)

        return resulting_chunks

    @retry(stop=stop_after_attempt(3))
    def resolve_chunk(self, chunk):
        result_lines = []

        for line in chunk["lines"]:
            result = requests.post(API_ENDPOINT_URL, timeout=10, json={
                "q": line['original_value'],
                "source": "auto",
                "target": self.target_language
            })

            translated_text = result.json()['translatedText']
            result_lines.append(translated_text)

        return result_lines

Klass = Libretranslate