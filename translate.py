import argparse
import sys
from ai_implementations import phind
from translating_formats import yml as yml_module

implementations = {
    'phind': phind,
}
translating_formats = {
    'yml': yml_module,
}

cmd_line_parser = argparse.ArgumentParser(description='Translate a text file from one language to another.')
cmd_line_parser.add_argument('--lang', default="french")
cmd_line_parser.add_argument('--impl', default="phind", dest="implementation")

args = cmd_line_parser.parse_args()

implementation = implementations[args.implementation]

stdin_content = sys.stdin.read()

chunks = translating_formats['yml'].prepare_chunks(stdin_content, implementation.CHUNK_SIZE_LIMIT)

implementation.translate(chunks, target_language=args.lang)
