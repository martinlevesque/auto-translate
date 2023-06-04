import json
import sys
from translating_formats.base import Base


class Json(Base):
    @staticmethod
    def is_proper_format(content):
        try:
            json.loads(content)
        except ValueError as e:
            print(f"Issue reading json content: {e}", file=sys.stderr)
            return False

        return True

    def prepare_chunks(self, content, chunk_size):
        yml_data = json.loads(content)

        return self.prepare_object_chunks(yml_data, chunk_size)
