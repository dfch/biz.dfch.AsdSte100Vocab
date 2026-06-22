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

"""``new`` create a new vocabulary entry."""

from dataclasses import replace
from pathlib import Path
from typing import Optional, TypeVar
from enum import EnumType

import typer
from rich.console import Console
from rich.table import Table
from rich import box

from ..vocab import Vocab
from ..word import Word
from ..word_meaning import WordMeaning
from ..word_source import WordSource
from ..word_status import WordStatus
from ..word_category import WordCategory
from ..word_type import WordType
from .args import (
    AlternativeOpt,
    VocabFile,
    MeaningOpt,
    NameOpt,
    StatusOpt,
    TypeOpt,
    CategoryOpt,
    SourceOpt,
    InteractiveOpt,
    YesNoOpt,
)

T = TypeVar("T")


def _prompt_source(default: str = "") -> str:
    """Prompt the user for a source reference.

    Offers ``STE100:9`` as a numbered shortcut; any other free-text is
    accepted as-is.  Pressing Enter with no input leaves the source empty.

    Returns
    -------
    str
        The chosen or typed source string (may be empty).
    """
    typer.echo("Source:")
    typer.echo(f"  1. {WordSource.STE100_9}")
    typer.echo("  (or any free-text)")

    raw: str = typer.prompt("  Choice", default=default).strip()

    if raw == "1":
        return WordSource.STE100_9
    return raw


def _prompt_choice(prompt: str, enum_type: type[T], default: T) -> T:
    """Prompt the user to pick an enum value interactively.

    Displays each member on its own numbered row::

        1. UNKNOWN: unknown
        2. NOUN: n
        3. VERB: v

    Accepted inputs (all case-insensitive):

    * A **number** (1-based index in the displayed list).
    * An **unambiguous prefix** of any member's *name* or *value*
      (e.g. ``a``, ``app``, ``appr`` for APPROVED / ``approved``).
    * The **full name** (``APPROVED``) or **full value** (``approved``).
    * An **empty string** / Enter to accept *default*.

    Keeps prompting until the input is valid and unambiguous.
    """

    assert isinstance(enum_type, EnumType), type(enum_type)

    members = list(enum_type)
    default_label = default.name  # type: ignore

    while True:
        # Print the numbered list – one member per row.
        typer.echo(f"{prompt}:")
        for i, m in enumerate(members, 1):
            marker = " (default)" if m is default else ""
            typer.echo(f"  {i}. {m.name}: {m.value}{marker}")  # type: ignore

        raw = typer.prompt("  Choice", default=default_label).strip()

        # "" or ENTER: default.
        if not raw or raw == default_label:
            return default

        # Numeric selection.
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(members):
                return members[idx]
            typer.echo(
                typer.style(
                    f"  Number must be between 1 and {len(members)}.",
                    fg=typer.colors.RED,
                )
            )
            continue

        # Prefix / full match against member name OR value (case-insensitive).
        prefix = raw.lower()
        matches = [
            m
            for m in members
            if m.name.lower().startswith(prefix)  # type: ignore
            or m.value.lower().startswith(prefix)  # type: ignore
        ]
        # De-duplicate (a full match on name and value could add same member
        # twice if both happen to start value).
        seen: list = []
        for m in matches:
            if m not in seen:
                seen.append(m)
        matches = seen

        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            ambiguous = ", ".join(f"{m.name}: {m.value}" for m in matches)
            typer.echo(
                typer.style(
                    f"  Ambiguous: '{raw}' matches '{ambiguous}'.",
                    fg=typer.colors.RED,
                )
            )
        else:
            typer.echo(
                typer.style(
                    f"  Unknown value: '{raw}'.",
                    fg=typer.colors.RED,
                )
            )


def _collect_meanings(
    meanings: Optional[list[str]],
    is_interactive: bool,
) -> list[WordMeaning]:
    """Collect word meanings for an ``APPROVED`` word.

    Builds the list of :class:`WordMeaning` objects from the supplied
    *meanings* list and, when interactive, from user prompts for additional
    meanings and their STE / non-STE examples.

    Returns
    -------
    list[WordMeaning]
        At least one meaning.
    """
    word_meanings: list[WordMeaning] = []

    if meanings is None:
        meanings = []
    for m in meanings:
        word_meanings.append(
            WordMeaning(value=m, ste_example=[], nonste_example=[])
        )

    if is_interactive:
        # Allow the user to add meanings one by one until they stop.
        while True:
            raw = typer.prompt(
                "Add a meaning (select ENTER to complete)",
                default="",
                show_default=False,
            ).strip()
            if not raw:
                break
            word_meanings.append(
                WordMeaning(value=raw, ste_example=[], nonste_example=[])
            )

        # Collect the examples of all meanings.
        for meaning in word_meanings:
            typer.echo(f"WordMeaning: '{meaning.value}'")

            ste = typer.prompt(
                "  STE example", default="", type=str, show_default=False
            ).strip()
            if ste:
                meaning.ste_example.append(ste)

            nonste = typer.prompt(
                "  Non-STE example",
                default="",
                type=str,
                show_default=False,
            ).strip()
            if nonste:
                meaning.nonste_example.append(nonste)

    assert word_meanings, (
        f"A word with status '{WordStatus.APPROVED.name}' "
        "must have at least one meaning."
    )

    return word_meanings


def _collect_alternatives(
    meanings: Optional[list[str]],
    alternatives: Optional[list[str]],
    type_: WordType,
    category: WordCategory,
    source: str,
    is_interactive: bool,
) -> list[Word]:
    """Collect alternative words for a ``REJECTED`` word.

    Builds the list of alternative :class:`Word` objects from the supplied
    *alternatives* list and, when interactive, from user prompts for
    additional alternatives and their STE / non-STE example pairs.

    Returns
    -------
    list[Word]
        The collected alternative words (may be empty).
    """
    assert not meanings, (
        f"A word with status '{WordStatus.REJECTED.name}' "
        "must not have meanings."
    )

    word_alternatives: list[Word] = []

    if alternatives is None:
        alternatives = []

    for alt_name in alternatives:
        word_alternatives.append(
            Word(
                name=alt_name,
                status=WordStatus.APPROVED,
                type_=type_,
                category=category,
                source=source,
                ste_example=[],
                nonste_example=[],
            )
        )

    if is_interactive:
        # Allow the user to add alternative word names one by one.
        while True:
            alt_name = typer.prompt(
                "Add an alternative word name (select ENTER to complete)",
                default="",
                show_default=False,
            ).strip()
            if not alt_name:
                break
            word_alternatives.append(
                Word(
                    name=alt_name,
                    status=WordStatus.APPROVED,
                    type_=type_,
                    category=category,
                    source=source,
                    ste_example=[],
                    nonste_example=[],
                )
            )

        # For each alternative collect 1+ ste/non-ste example pairs.
        updated_alternatives: list[Word] = []
        for alt in word_alternatives:
            typer.echo(f"\nAlternative: '{alt.name}'")
            ste_examples: list[str] = []
            nonste_examples: list[str] = []
            while True:
                ste = typer.prompt(
                    "  STE example (select ENTER to complete)",
                    default="",
                    show_default=False,
                ).strip()
                if not ste:
                    if not ste_examples:
                        typer.echo(
                            typer.style(
                                "  At least one STE example is required.",
                                fg=typer.colors.RED,
                            )
                        )
                        continue
                    break
                nonste = typer.prompt(
                    "  Non-STE example for this pair",
                    default="",
                    show_default=False,
                ).strip()
                ste_examples.append(ste)
                nonste_examples.append(nonste)

            updated_alternatives.append(
                replace(
                    alt,
                    ste_example=ste_examples,
                    nonste_example=nonste_examples,
                )
            )
        word_alternatives = updated_alternatives

    return word_alternatives


def new(
    name: NameOpt,
    status: StatusOpt = None,
    type_: TypeOpt = None,
    category: CategoryOpt = None,
    source: SourceOpt = None,
    meanings: MeaningOpt = None,
    alternatives: AlternativeOpt = None,
    is_interactive: InteractiveOpt = False,
    file: VocabFile = None,
    do_not_confirm: YesNoOpt = False,
) -> None:
    """
    Create a new vocabulary entry.

    When called with `is_interactive` interactive prompt collects all
    values.
    """

    assert isinstance(name, str), name
    assert name.strip()

    assert (
        status is None
        or (status == WordStatus.APPROVED and not alternatives)
        or (status == WordStatus.REJECTED and not meanings)
    ), "Combination of WordStatus and meanings and alternatives is not correct."

    vocab = Vocab(use_ste100=False, use_ste100_technical_word=False)
    if file is not None:
        assert isinstance(file, Path), type(file)
        assert file.exists(), f"File '{file.name}' must exist."
        assert file.is_file(), f"File '{file.name}' must be a file."
        vocab = Vocab(
            use_ste100=False, use_ste100_technical_word=False, files=[file]
        )

    if is_interactive or status is None or status.strip() == "":
        status = _prompt_choice(
            "WordStatus", WordStatus, status or WordStatus.UNKNOWN
        )
    if is_interactive or type_ is None or type_.strip() == "":
        type_ = _prompt_choice("WordType", WordType, type_ or WordType.UNKNOWN)
    if is_interactive or category is None or category.strip() == "":
        category = _prompt_choice(
            "WordCategory", WordCategory, category or WordCategory.DEFAULT
        )
    if is_interactive or source is None or source.strip() == "":
        source = _prompt_source(default=source or "")

    word_meanings: list[WordMeaning] = []
    word_alternatives: list[Word] = []

    if status == WordStatus.APPROVED:
        word_meanings = _collect_meanings(
            meanings=meanings,
            is_interactive=is_interactive,
        )
    elif status == WordStatus.REJECTED:
        word_alternatives = _collect_alternatives(
            meanings=meanings,
            alternatives=alternatives,
            type_=type_,  # type: ignore
            category=category,  # type: ignore
            source=source,
            is_interactive=is_interactive,
        )

    assert isinstance(name, str), type(name)
    assert isinstance(status, WordStatus), type(status)
    assert isinstance(type_, WordType), type(type_)
    assert isinstance(category, WordCategory), type(category)
    assert isinstance(source, str), type(source)

    word = Word(
        name=name,
        status=status,
        type_=type_,
        category=category,
        source=source,
        meanings=word_meanings,
        alternatives=word_alternatives,
    )

    table = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("Field", style="bold")
    table.add_column("Value")
    table.add_row("name", word.name)
    table.add_row("status", word.status.value)
    table.add_row("type", word.type_.value)
    table.add_row("category", word.category.value)
    if status == WordStatus.APPROVED:
        table.add_row("meanings", "\n".join(m.value for m in word.meanings))
    elif status == WordStatus.REJECTED:
        alt_summary = (
            "\n".join(
                f"{a.name}  STE: {a.ste_example}  non-STE: {a.nonste_example}"
                for a in word.alternatives
            )
            or "(none)"
        )
        table.add_row("alternatives", alt_summary)
    table.add_row("source", word.source or "(none)")
    console = Console()
    console.print(table)

    v = Vocab(use_ste100=False, use_ste100_technical_word=False)
    v.append(word)
    jsonl_text = v.write_jsonl_text()
    assert isinstance(jsonl_text, list), type(jsonl_text)
    assert 1 == len(jsonl_text)
    result = jsonl_text[0]
    console.print_json(result)

    if file is None:
        typer.echo(result)
        return

    if not do_not_confirm:
        do_not_confirm = typer.confirm(
            f"Do you want to write word '{word.name}' to vocabulary '{file}'?",
            default=False,
        )
    if not do_not_confirm:
        return

    typer.echo(f"Write word '{word.name}' to vocabulary '{file}' ...")
    vocab.append(word)
    vocab.sort()
    vocab.write_jsonl_file(file, overwrite=True)
    typer.echo(f"Write word '{word.name}' to vocabulary '{file}' OK.")
