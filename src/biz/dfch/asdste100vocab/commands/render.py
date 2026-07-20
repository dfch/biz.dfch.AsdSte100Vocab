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

"""Shared rendering helpers for CLI commands."""

from rich.console import Console
from rich.table import Table
from rich import box

from ..word import Word
from ..word_status import WordStatus


def _word_name_styled(word: Word) -> str:
    """Return the word name styled by its approval status."""
    if word.status == WordStatus.APPROVED:
        return f"[green]{word.name}[/green]"
    if word.status == WordStatus.REJECTED:
        return f"[red]{word.name}[/red]"
    return word.name


def print_word_table(results: list[Word]) -> None:
    """Render a list of `Word` objects as a Rich table and print it.

    Parameters
    ----------
    results:
        The list of `Word` objects to display.
    """

    assert isinstance(results, list), type(results)

    table = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("Word")
    table.add_column("Status")
    table.add_column("Type")
    table.add_column("Category")
    table.add_column("Source")

    for word in results:
        table.add_row(
            _word_name_styled(word),
            word.status.value,
            word.type_.value,
            word.category.value,
            word.source or "",
        )

    console = Console()
    console.print(table)
