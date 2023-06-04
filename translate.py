import argparse
import sys
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

stdin_content = sys.stdin.read()


# implementations:

submodules = {
    name: importlib.import_module("." + name, implementations.__name__)
    for _, name, _ in pkgutil.iter_modules(implementations.__path__)
}

implementation_submodule = submodules[args.implementation]

# translating formats:

format_submodules = {
    name: importlib.import_module("." + name, translating_formats.__name__)
    for _, name, _ in pkgutil.iter_modules(translating_formats.__path__)
}

if not args.format:
    # loop over format submodules:
    for name, submodule in format_submodules.items():
        if hasattr(submodule, "Klass") and submodule.Klass.is_proper_format(
            stdin_content
        ):
            args.format = name
            break


translating_format = format_submodules[args.format]
format = translating_format.Klass()

chunks, original_yaml = format.prepare_chunks(
    stdin_content, implementation_submodule.CHUNK_SIZE_LIMIT
)

all_content = translating_formats.base.Base.concatenate_all_content(chunks)

print(f"about source.")
if not args.source_lang:
    print("inn")
    args.source_lang = implementations.base.Base.determine_language(all_content) or "en"
    print(f"source language: {args.source_lang}")

# translate:

implementation = implementation_submodule.Klass(
    target_language=args.target_lang, source_language=args.source_lang
)

resulting_chunks = implementation.translate(chunks)

print(format.format_final_yml(resulting_chunks, original_yaml))
