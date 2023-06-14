
# auto-translate

auto-translate takes as input a source file to be translated and using a third-party translation tool,
it translates only values contained.

## Usage

### Command line

The CLI can be used as follows:

```
<STDIN> | python translate.py [--source-lang SOURCE_LANG] [--target-lang TARGET_LANG] [--impl IMPLEMENTATION] [--format FORMAT]
```

- `SOURCE_LANG` is the source language of the input file. If not specified, it will be auto-detected.
- `TARGET_LANG` is the target language of the output file.
- `IMPLEMENTATION` is the translation implementation to use, based on the implementions in `implementions/` folder.
- `FORMAT` is the format of the input and output files. If not specified, it will be auto-detected. Available formats are based on the implementations in `translating_formats/` folder.

And so an example usage is as follows:

```
cat input.json | python translate.py --target-lang fr --impl libretranslate --format json > output.json
```

where input.json could be:

```json
{
  "hello": "Hello world!",
  "goodbye": "Goodbye world!"
}
```

the resulting output.json file could result into:

```json
{
  "hello": "Bonjour le monde!",
  "goodbye": "Au revoir le monde!"
}
```

## Features

- Automatically translate values contained in a source file into a target language.
- Auto detect the source language (using langdetect).
- Auto detect of the source file format.
- Extendable by adding new translation implementations (see `implementions/` folder) and translated file formats (see `translating_formats/` folder).
