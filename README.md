# DEPRECATED: This is the old `biz-dfch-ste100vocab` package

**This repository and package are deprecated. Use the new package instead:**

```bash
uv add biz-dfch-asdste100vocab
```

(or with `pip`)

```bash
pip install biz-dfch-asdste100vocab
```

All software documentation below continue to work (the repo name is unchanged), but for all projects, install from **biz-dfch-asdste100vocab** on PyPI.

# biz.dfch.AsdSte100Vocab

[![ASD-STE100: Issue 9](https://img.shields.io/badge/ASD--STE100-Issue%209-blue.svg)](https://www.asd-ste100.org/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)
[![Pylint and unittest](https://github.com/dfch/biz.dfch.AsdSte100Vocab/actions/workflows/ci.yml/badge.svg)](https://github.com/dfch/biz.dfch.AsdSte100Vocab/actions/workflows/ci.yml)
[![TestPyPI version](https://img.shields.io/badge/dynamic/json?url=https://test.pypi.org/pypi/biz-dfch-asdste100vocab/json&label=TestPyPI&query=$.info.version&color=orange)](https://test.pypi.org/project/biz-dfch-asdste100vocab/)
[![PyPI version](https://img.shields.io/badge/dynamic/json?url=https://www.pypi.org/pypi/biz-dfch-asdste100vocab/json&label=PyPI&query=$.info.version&color=blue)](https://www.pypi.org/project/biz-dfch-asdste100vocab/)
[![PyPI downloads](https://img.shields.io/pypi/dm/biz-dfch-asdste100vocab.svg)](https://pypistats.org/packages/biz-dfch-asdste100vocab)

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

**This package is deprecated.** Use the new package on [PyPI](https://pypi.org):

```
pip install biz-dfch-asdste100vocab
```

Or install with `uv`:

```
uv add biz-dfch-asdste100vocab
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

## Make a Release

### 1. Make sure that all tests pass

Before releasing, make sure the CI pipeline is green on the `dev` branch:

```
uv run --frozen ruff format --check
uv run --frozen ruff check
uv run --frozen pylint $(git ls-files '*.py') || true
uv run --frozen python -m unittest discover -v -s tests -t . -p "test_*.py"
```

### 2. Increase the version

Update the version in `pyproject.toml`:
```toml
version = "x.y.z"
```

### 3. Commit and push to `dev`

```
git add pyproject.toml
git commit -m "chore: bump version to vx.y.z"
git push origin dev
```

### 4. Merge `dev` into `main`

```
git checkout main
git merge dev
git push origin main
```

### 5. Create and push a version tag

This will create a binary artifact of the application and add it to the `release`.

```
export VERSION=x.y.z
git tag v${VERSION}
git push origin v${VERSION}
```

Then, select the `dev` branch to continue your work.

```
git checkout dev
```

Pushing the tag automatically triggers the `publish.yml` workflow, which will:
* build the executable with `pyinstaller` for Linux x86_64
    (**this step creates the artifact**)
* rename it to `AsdSte100Lookup-v<version>-linux-x86_64`
* create a GitHub Release with auto-generated release notes
* upload the binary as a release artifact
    (**this step adds the artifact to the release**)


## License

This library is licensed under the [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0). See [LICENSE](./LICENSE) for more information.

ASD-STE100 Simplified Technical English (Standard for Technical Documentation), Issue 9

Copyright 2025 [Aerospace, Security and Defence Industries Association of Europe (ASD)](https://www.asd-europe.org), https://www.asd-europe.org.

This library or the maintainer is not affiliated with ASD. ASD does not endorse this library or the maintainer.
