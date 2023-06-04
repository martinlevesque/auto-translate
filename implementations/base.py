from dataclasses import dataclass
from tenacity import retry, stop_after_attempt
import langdetect


@dataclass
class Base:
    source_language: str = "en"
    target_language: str = "en"

    def determine_language(text):
        return langdetect.detect(text) or "en"

    def translate(self, chunks):
        raise NotImplementedError()

    def resolve_all_chunks_lines(self, chunks):
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
            result_lines.append(self.resolve_chunk_line(line))

        return result_lines

    def resolve_chunk_line(self, line):
        raise NotImplementedError()
