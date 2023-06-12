import argparse
import sys
import os
import implementations
import pkgutil
import importlib
import translating_formats

cmd_line_parser = argparse.ArgumentParser(
    description="Translate a text file from one language to another."
)
cmd_line_parser.add_argument("--source-lang")
cmd_line_parser.add_argument("--target-lang", default="french")
cmd_line_parser.add_argument("--impl", default="libretranslate", dest="implementation")
cmd_line_parser.add_argument("--format", dest="format")

args = cmd_line_parser.parse_args()

if not os.isatty(sys.stdin.fileno()):
    stdin_content = sys.stdin.read()
else:
    # exit
    print(cmd_line_parser.format_help(), file=sys.stderr)
    sys.exit(1)



def load_submodules(main_module):
    return {
        name: importlib.import_module("." + name, main_module.__name__)
        for _, name, _ in pkgutil.iter_modules(main_module.__path__)
    }

# implementations:
# define how translation is done based on various implementions in implementations/ folder

submodules = load_submodules(implementations)

implementation_submodule = submodules[args.implementation]

# translating formats:
# supported file formats

format_submodules = load_submodules(translating_formats)

if not args.format:
    # loop over format submodules:
    for name, submodule in format_submodules.items():
        if hasattr(submodule, "Klass") and submodule.Klass.is_proper_format(
            stdin_content
        ):
            args.format = name
            break

######
# Main

translating_format = format_submodules[args.format]
format = translating_format.Klass()

chunks, original_yaml = format.prepare_chunks(
    stdin_content, implementation_submodule.CHUNK_SIZE_LIMIT
)

all_content = translating_formats.base.Base.concatenate_all_content(chunks)

if not args.source_lang:
    args.source_lang = implementations.base.Base.determine_language(all_content) or "en"

# translate:

implementation = implementation_submodule.Klass(
    target_language=args.target_lang, source_language=args.source_lang
)

resulting_chunks = implementation.translate(chunks)

print(format.format_final_yml(resulting_chunks, original_yaml))
