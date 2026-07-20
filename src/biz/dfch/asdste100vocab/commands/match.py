# Copyright (C) 2026 Ronald Rink, d-fens GmbH, http://d-fens.ch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""``match`` find vocabulary entries matching a regular expression pattern."""

from pathlib import Path

import typer
from rich.console import Console

from ..vocab import Vocab
from ..word import Word
from .args import (
    PhraseArg,
    UseSte100Opt,
    UseSte100TechnicalWordOpt,
    VocabFiles,
)
from .render import print_word_table


def match(
    pattern: PhraseArg,
    use_ste100: UseSte100Opt = True,
    use_ste100_technical_word: UseSte100TechnicalWordOpt = False,
    files: VocabFiles = None,
) -> None:
    """
    Find vocabulary entries matching a regular expression pattern.

    Searches the built-in STE100 vocabulary and any additional JSONL
    vocabulary files supplied via ``--vocabulary`` for words whose names
    match *pattern* (case-insensitive regex substring search).
    """

    assert isinstance(pattern, str) and pattern.strip(), pattern

    extra_files: list[Path] = files if files is not None else []

    vocab = Vocab(
        use_ste100=use_ste100,
        use_ste100_technical_word=use_ste100_technical_word,
        files=extra_files,
    )

    results: list[Word] = vocab.match(pattern)

    console = Console()

    if not results:
        console.print(
            typer.style(
                f"No matching words found for '{pattern}'.",
                fg=typer.colors.YELLOW,
            )
        )
        raise typer.Exit(code=0)

    print_word_table(results)
