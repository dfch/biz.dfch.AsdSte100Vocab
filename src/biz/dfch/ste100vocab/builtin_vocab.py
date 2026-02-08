# Copyright (c) 2026 Ronald Rink, http://d-fens.ch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""BuiltInVocab enumeration."""

from enum import StrEnum


class BuiltInVocab(StrEnum):
    """ASD STE100 builtin vocabulary."""

    DATA_DIR = "data"
    STE100_BASE = "asdste100_issue9_base.jsonl"
    STE100_TECHNICAL_WORDS = "asdste100_issue9_technical_words.jsonl"
