# biz.dfch.AsdSte100Vocab

[![ASD-STE100: Issue 9](https://img.shields.io/badge/ASD--STE100-Issue%209-blue.svg)](https://www.asd-ste100.org/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)
[![Pylint and unittest](https://github.com/dfch/biz.dfch.AsdSte100Vocab/actions/workflows/ci.yml/badge.svg)](https://github.com/dfch/biz.dfch.AsdSte100Vocab/actions/workflows/ci.yml)

## Introduction

This is a Python library, that implements an [ASD-STE100 Issue 9](https://www.asd-ste100.org/) compatible dictionary, that includes the Technical Nouns (TN) and Technical Verbs (TV) from the rule R1.5 and rule R1.12. It has these properties:

* `name`, the name of a word item
* `status`, is this word `APPROVED` or `REJECTED`?
* `source`, where does this word come from?
* `type_`, the word type (similar to "part of speech")
* `spellings`, all correct spellings of the `Word` item (this is not a "lemma")
* `meanings`, contains one or more meanings for an `APPROVED` word item
* `alternatives`, contains one or more alternatives for a `REJECTED` word item
* `note`, an optional note for `Word` item
* `ste_example`, an example that shows how to use the `Word` item correctly
* `nonste_example`, an example that shows an incorrect use of the `Word` item

[biz.dfch.AsdSte100Lookup](https://github.com/dfch/biz.dfch.AsdSte100Lookup) uses this library for its word lists and the display of these words.

## Installation

[biz-dfch-ste100vocab](https://pypi.org/project/biz-dfch-ste100vocab/) is on [PyPI](https://pypi.org). Create a virtual environment and install the library with `pip`:

```
pip install biz-dfch-ste100vocab
```

## License

This library is licensed under the [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0). See [LICENSE](./LICENSE) for more information.

ASD-STE100 Simplified Technical English (Standard for Technical Documentation), Issue 9

Copyright 2025 [Aerospace, Security and Defence Industries Association of Europe (ASD)](https://www.asd-europe.org), https://www.asd-europe.org.

This library or the maintainer is not affiliated with ASD. ASD does not endorse this library or the maintainer.
