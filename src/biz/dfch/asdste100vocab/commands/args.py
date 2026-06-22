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

"""Shared ``Annotated`` parameter definitions for CLI sub-commands.

Each name defined here is a ready-to-use type alias that can be dropped
directly into a Typer command signature::

    from .args import ArgName, OptStatus, OptDryRun

    def new(
        name: ArgName,
        status: OptStatus = WordStatus.UNKNOWN,
        dry_run: OptDryRun = False,
    ) -> None: ...
"""

from pathlib import Path
from typing import Annotated, List, Optional

import typer

from ..word_category import WordCategory
from ..word_status import WordStatus
from ..word_type import WordType

# ---------------------------------------------------------------------------
# Named option shared by all three commands
# ---------------------------------------------------------------------------

NameOpt = Annotated[
    Optional[str],
    typer.Option(
        "--word",
        "-w",
        help="The name of the wordto add.",
    ),
]

StatusOpt = Annotated[
    Optional[WordStatus],
    typer.Option(
        "--status",
        "-s",
        envvar="VOCAB_STATUS",
        help="Approval status of the entry.",
    ),
]

TypeOpt = Annotated[
    Optional[WordType],
    typer.Option(
        "--type",
        "-t",
        envvar="VOCAB_TYPE",
        help="Grammatical type of the entry.",
    ),
]

CategoryOpt = Annotated[
    Optional[WordCategory],
    typer.Option(
        "--category",
        "-cat",
        "-c",
        envvar="VOCAB_CATEGORY",
        help="Word category of the entry.",
    ),
]

SourceOpt = Annotated[
    Optional[str],
    typer.Option(
        "--source",
        "-src",
        envvar="VOCAB_SOURCE",
        help="Source reference for the entry (e.g. ``STE100:9``).",
    ),
]

MeaningOpt = Annotated[
    Optional[List[str]],
    typer.Option(
        "--meaning",
        "-m",
        help=(
            "Definition of the word. Repeat for multiple meanings,"
            " e.g. ``--meaning 'def one' --meaning 'def two'``."
        ),
    ),
]

AlternativeOpt = Annotated[
    Optional[List[str]],
    typer.Option(
        "--alternative",
        "-a",
        help=(
            "Approved alternative word name for a rejected entry."
            " Repeat for multiple alternatives,"
            " e.g. ``--alternative OPERATE --alternative WORK``."
        ),
    ),
]

NewNameOpt = Annotated[
    Optional[str],
    typer.Option(
        "--new-name",
        "-N",
        help="Rename the entry to this new word name.",
    ),
]

VocabFile = Annotated[
    Optional[Path],
    typer.Option(
        "--vocabulary",
        "-v",
        envvar="VOCAB_FILE",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=True,
        resolve_path=True,
        help=(
            "Path to an existing JSONL vocabulary file."
            " The `word` is added to this file."
        ),
    ),
]

YesNoOpt = Annotated[
    bool,
    typer.Option(
        "--yes/--no",
        "-y/-n",
        help="Confirm (--yes) or cancel (--no) the operation.",
    ),
]

DryRunOpt = Annotated[
    bool,
    typer.Option(
        "--dry-run",
        help="Print what would happen without persisting anything.",
    ),
]

InteractiveOpt = Annotated[
    bool,
    typer.Option(
        "--interactive",
        "-i",
        help="Start the interactive procedure and ask for parameters.",
    ),
]
