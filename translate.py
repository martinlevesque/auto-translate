import argparse
import sys
import implementations
import pkgutil
import importlib
from translating_formats import yml as yml_module

translating_formats = {
    "yml": yml_module,
}

cmd_line_parser = argparse.ArgumentParser(
    description="Translate a text file from one language to another."
)
cmd_line_parser.add_argument("--lang", default="french")
cmd_line_parser.add_argument("--impl", default="libretranslate", dest="implementation")

args = cmd_line_parser.parse_args()

submodules = {
    name: importlib.import_module("." + name, implementations.__name__)
    for _, name, _ in pkgutil.iter_modules(implementations.__path__)
}


submodule = submodules[args.implementation]
implementation = submodule.Klass(target_language=args.lang)

stdin_content = sys.stdin.read()

chunks, original_yaml = translating_formats["yml"].prepare_chunks(
    stdin_content, submodule.CHUNK_SIZE_LIMIT
)

resulting_chunks = implementation.translate(chunks)

print(translating_formats["yml"].format_final_yml(resulting_chunks, original_yaml))
