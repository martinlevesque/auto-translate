import argparse
import sys
import json
from ai_implementations import phind
from translating_formats import yml as yml_module

## TODO
# please translate the following text into french (make sure to keep the four dashes), put the translation in a code snippet block in containing raw format with the translation only:----

implementations = {
    "phind": phind,
}
translating_formats = {
    "yml": yml_module,
}

cmd_line_parser = argparse.ArgumentParser(
    description="Translate a text file from one language to another."
)
cmd_line_parser.add_argument("--lang", default="french")
cmd_line_parser.add_argument("--impl", default="phind", dest="implementation")

args = cmd_line_parser.parse_args()

implementation = implementations[args.implementation]

stdin_content = sys.stdin.read()

chunks, original_yaml = translating_formats["yml"].prepare_chunks(
    stdin_content, implementation.CHUNK_SIZE_LIMIT
)

print(f"chunks = {json.dumps(chunks, indent=4)}")

# resulting_chunks = implementation.translate(chunks, target_language=args.lang)

# print(translating_formats['yml'].format_final_yml(resulting_chunks))
