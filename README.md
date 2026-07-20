# biz.dfch.AsdSte100Vocab

[![ASD-STE100: Issue 9](https://img.shields.io/badge/ASD--STE100-Issue%209-blue.svg)](https://www.asd-ste100.org/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)
[![Pylint and unittest](https://github.com/dfch/biz.dfch.AsdSte100Vocab/actions/workflows/ci.yml/badge.svg)](https://github.com/dfch/biz.dfch.AsdSte100Vocab/actions/workflows/ci.yml)
[![TestPyPI version](https://img.shields.io/badge/dynamic/json?url=https://test.pypi.org/pypi/biz-dfch-ste100vocab/json&label=TestPyPI&query=$.info.version&color=orange)](https://test.pypi.org/project/biz-dfch-ste100vocab/)
[![PyPI version](https://img.shields.io/badge/dynamic/json?url=https://www.pypi.org/pypi/biz-dfch-ste100vocab/json&label=PyPI&query=$.info.version&color=blue)](https://www.pypi.org/project/biz-dfch-ste100vocab/)
[![PyPI downloads](https://img.shields.io/pypi/dm/biz-dfch-ste100vocab.svg)](https://pypistats.org/packages/biz-dfch-ste100vocab)

## Introduction

This is a Python library, that implements an [ASD-STE100 Issue 9](https://www.asd-ste100.org/) compatible dictionary, that includes the Technical Nouns (TN) and Technical Verbs (TV) from the rule R1.5 and rule R1.12. A [`word`](./src/biz/dfch/asdste100vocab/word.py) has these properties:

* `name`, the name of a word item
* [`status`](./src/biz/dfch/asdste100vocab/word_status.py), is this word `APPROVED` or `REJECTED`?
* [`source`](./src/biz/dfch/asdste100vocab/word_source.py), where does this word come from?
* [`type_`](./src/biz/dfch/asdste100vocab/word_type.py), the word type (similar to "part of speech")
* [`category`](./src/biz/dfch/asdste100vocab/word_category.py), the TN or TV category or "default"
* `spellings`, all correct spellings of the `Word` item (this is not a "lemma")
* [`meanings`](./src/biz/dfch/asdste100vocab/word_meaning.py), contains one or more meanings for an `APPROVED` word item
* `alternatives`, a `list` that contains one or more alternatives for a `REJECTED` word item
* [`note`](./src/biz/dfch/asdste100vocab/word_note.py), an optional note for `Word` item
* `ste_example`, an example that shows how to use the `Word` item correctly
* `nonste_example`, an example that shows an incorrect use of the `Word` item

[biz.dfch.AsdSte100Lookup](https://github.com/dfch/biz.dfch.AsdSte100Lookup) uses this library for its word lists and the display of these words.

## Installation

[biz-dfch-ste100vocab](https://pypi.org/project/biz-dfch-ste100vocab/) is on [PyPI](https://pypi.org). Create a virtual environment and install the library with `pip`:

```
pip install biz-dfch-ste100vocab
```

Or install with `uv`:

```
uv add biz-dfch-ste100vocab
```

## Create your own vocabulary entries

When you want to create your own word entries, you install the `dev` dependencies:

```
uv sync --extra dev
# or
uv pip install -e ".[dev]"
# or
pip install -e ".[dev]"
```

Then use this command:

```
uv run vocab new
```

<img width="3804" height="1536" alt="image" src="https://github.com/user-attachments/assets/9f14c8eb-5d15-40f0-82f3-94fdebb68a14" />

You can use an `.env` file (or environment variables, see `--help`) to define recurring parameters (see example below) and you can use `--interactive` (or `-i`) for an interactive wizard. Each time you start the program, it will create a new `JSONL` entry.

The specified file must exist. The program will only **append** to an existing file, but not create a new file.

### Example `.env` file

```
cat .env
```

```
VOCAB_STATUS=approved
VOCAB_SOURCE=ARBITRARY-SOURCE
VOCAB_TYPE=TN
VOCAB_CATEGORY=TN21
VOCAB_FILE=./vocab.jsonl
```


## License

This library is licensed under the [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0). See [LICENSE](./LICENSE) for more information.

ASD-STE100 Simplified Technical English (Standard for Technical Documentation), Issue 9

Copyright 2025 [Aerospace, Security and Defence Industries Association of Europe (ASD)](https://www.asd-europe.org), https://www.asd-europe.org.

This library or the maintainer is not affiliated with ASD. ASD does not endorse this library or the maintainer.
