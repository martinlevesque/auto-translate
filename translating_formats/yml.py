import yaml
import sys
from translating_formats.base import Base


class Yml(Base):
    @staticmethod
    def is_proper_format(content):
        try:
            print(f"checking yml..")
            yaml.safe_load(content)
            print(f"looks ok checking yml..")
        except yaml.error.MarkedYAMLError as e:
            print(f"Issue reading yml content: {e}", file=sys.stderr)
            return False

        return True

    def prepare_chunks(self, content, chunk_size):
        yml_data = yaml.safe_load(content)

        return self.prepare_object_chunks(yml_data, chunk_size)

    def format_final_yml(self, resulting_chunks, original_yml):

        for chunk in resulting_chunks:
            index_line = 0

            for line in chunk["lines"]:
                resolve_line = chunk["resolved_lines"][index_line]
                line["data_ref"][line["key_ref"]] = resolve_line

                index_line += 1

        return yaml.safe_dump(original_yml, allow_unicode=True)


Klass = Yml
