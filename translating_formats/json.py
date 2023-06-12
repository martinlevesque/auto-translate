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

    def format_final_yml(self, resulting_chunks, original_yml):

        for chunk in resulting_chunks:
            index_line = 0

            for line in chunk["lines"]:
                resolve_line = chunk["resolved_lines"][index_line]
                line["data_ref"][line["key_ref"]] = resolve_line

                index_line += 1

        return json.dumps(original_yml, indent=2, sort_keys=True, ensure_ascii=False)


Klass = Json
