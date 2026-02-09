# Copyright (C) 2025-2026 Ronald Rink, d-fens GmbH, http://d-fens.ch
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

"""Word class."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .word_category import WordCategory
from .word_status import WordStatus
from .word_type import WordType
from .word_source import WordSource

if TYPE_CHECKING:
    from .word_meaning import WordMeaning
    from .word_note import WordNote


@dataclass(frozen=True)
class Word:
    """
    Represents either an approved or rejected word from the ASD-STE100 standard.
    """

    name: str
    status: WordStatus = WordStatus.UNKNOWN
    type_: WordType = WordType.UNKNOWN
    meanings: list[WordMeaning] = field(default_factory=list)
    spellings: list[str] = field(default_factory=list)
    alternatives: list[Word] = field(default_factory=list)
    source: str = WordSource.UNKNOWN
    category: WordCategory = WordCategory.DEFAULT
    ste_example: list[str] = field(default_factory=list)
    nonste_example: list[str] = field(default_factory=list)
    note: WordNote | None = None
