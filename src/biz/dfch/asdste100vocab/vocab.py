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

"""Vocabulary class."""

from __future__ import annotations
import json
from pathlib import Path
from typing import Callable
from typing import Iterator

from dacite import Config, from_dict

from .word import Word
from .word_category import WordCategory
from .word_meaning import WordMeaning
from .word_note import WordNote
from .word_status import WordStatus
from .word_type import WordType
from .builtin_vocab import BuiltInVocab


class Vocab:
    """Vocabulary class."""

    _configuration: Config = Config(
        strict=True,
        type_hooks={
            WordStatus: WordStatus,
            WordType: WordType,
            WordCategory: WordCategory,
        },
        forward_references={
            Word.__name__: Word,
            WordMeaning.__name__: WordMeaning,
            WordNote.__name__: WordNote,
        },
    )

    _files: list[Path]
    _items: list[Word]
    _predicate: Callable[[Word], bool]

    def __init__(
        self,
        *,
        files: list[Path] | None = None,
        use_ste100: bool = True,
        use_ste100_technical_word: bool = False,
        predicate: Callable[[Word], bool] | None = None,
    ) -> None:
        """Instantiates a vocabulary object."""

        if files is None:
            files = []
        assert isinstance(files, list), type(files)
        assert isinstance(use_ste100, bool), type(use_ste100)
        assert isinstance(use_ste100_technical_word, bool), type(
            use_ste100_technical_word
        )
        if predicate is not None:
            assert callable(predicate), type(predicate)
            self._predicate = predicate
        else:
            self._predicate = lambda _: True

        self._items = []
        self._files = []

        data_dir = Path(__file__).parent / BuiltInVocab.DATA_DIR

        if use_ste100:
            base_vocab = data_dir / BuiltInVocab.STE100_BASE
            self._files.append(base_vocab)

        if use_ste100_technical_word:
            tn_vocab = data_dir / BuiltInVocab.STE100_TECHNICAL_WORDS
            self._files.append(tn_vocab)

        self._files.extend(files)
        for file in self._files:

            assert isinstance(file, Path), type(file)
            if not file.exists():
                raise FileNotFoundError(file)

            words = Vocab.read_jsonl_file(
                file,
                predicate=self._predicate,
            )
            self._items.extend(words)

        self.sort(key=self._default_sort_key)

    @staticmethod
    def read_jsonl_text(
        value: str,
    ) -> Word:
        """Read `Word` entries from a JSONL file."""

        assert isinstance(value, str), type(value)

        line = value.strip()
        item = json.loads(line)
        result = from_dict(
            data_class=Word,
            data=item,
            config=Vocab._configuration,
        )

        return result

    @staticmethod
    def read_jsonl_file(
        fullname: Path,
        predicate: Callable[[Word], bool] | None = None,
    ) -> list[Word]:
        """Read `Word` entries from a JSONL file."""

        assert isinstance(fullname, Path), type(fullname)
        assert fullname.exists(), fullname
        if predicate is not None:
            assert callable(predicate), type(predicate)

        result: list[Word] = []

        with open(fullname, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f, 1):
                line = line.strip()
                try:
                    word = Vocab.read_jsonl_text(line)
                    if predicate is not None and predicate(word):
                        result.append(word)
                except Exception as ex:  # pylint: disable=W0718
                    print(f"[ERROR] {fullname}[#{idx}]: '{ex}'.")

        return result

    def __len__(self) -> int:
        """Return the number of items in the vocabulary."""
        return len(self._items)

    def __iter__(self) -> Iterator[Word]:
        """Return an iterator over items in the vocabulary."""
        return iter(self._items)

    def __getitem__(self, index: int) -> Word:
        """Return a word by its index."""
        return self._items[index]

    def append(self, word: Word) -> None:
        """Add a single `Word` item to the vocabulary."""

        assert isinstance(word, Word), type(word)

        self._items.append(word)

    def extend(self, words: list[Word]) -> None:
        """Add multiple `Word` items to the vocabulary."""

        assert isinstance(words, list), type(words)

        self._items.extend(words)

    def remove(self, word: Word) -> None:
        """Remove a `Word` item from the vocabulary by object."""

        assert isinstance(word, Word), type(word)

        self._items.remove(word)

    def pop(self, index: int = -1) -> Word:
        """Remove and return a `Word` item from the vocabulary by its index."""

        return self._items.pop(index)

    def __delitem__(self, index: int) -> None:
        """Remove a `Word` item from the vocabulary by its index."""
        del self._items[index]

    @staticmethod
    def _default_sort_key(word):
        """Default sort key is case-insensitive alphabetical order."""

        return word.name.lower()

    def sort(
        self, *, key: Callable[[Word], str] | None = None, reverse=False
    ) -> None:
        """
        Sort the `Word` items in the vocabulary.

        If you do not define `key`, then the result of the sort is
        alphabetically.
        """

        if key is None:
            key = Vocab._default_sort_key
        assert callable(key), type(key)
        assert isinstance(reverse, bool)

        self._items.sort(key=key, reverse=reverse)
