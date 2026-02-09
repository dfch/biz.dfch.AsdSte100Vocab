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

from enum import StrEnum


class VocabFile(StrEnum):
    """Definitions for test vocabulary files."""

    NON_EXISTENT_FILE = "this-word-list-does-not-exist.jsonl"
    ONE_ITEM = "test_vocab_word_list1.jsonl"
    TWO_ITEMS = "test_vocab_word_list2.jsonl"
    THREE_ITEMS = "test_vocab_word_list3.jsonl"
    SPELLING = "test_word_spelling.jsonl"
