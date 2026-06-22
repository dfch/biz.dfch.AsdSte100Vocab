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
import dataclasses
import enum
import json
from pathlib import Path
import re
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

        if use_ste100:
            base_vocab = BuiltInVocab.STE100_BASE.value
            self._files.append(base_vocab)

        if use_ste100_technical_word:
            tn_vocab = BuiltInVocab.STE100_TECHNICAL_WORDS.value
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

    def replace(self, existing: Word, replacement: Word) -> None:
        """Replace an existing `Word` item with a new `Word` item.

        Parameters
        ----------
        existing:
            The `Word` object currently in the vocabulary to be replaced.
            Lookup is done by equality (``==``).
        replacement:
            The new `Word` object to put in its place.

        Raises
        ------
        ValueError
            If *existing* is not found in the vocabulary.
        """

        assert isinstance(existing, Word), type(existing)
        assert isinstance(replacement, Word), type(replacement)

        index = self._items.index(existing)
        self._items[index] = replacement

    def pop(self, index: int = -1) -> Word:
        """Remove and return a `Word` item from the vocabulary by its index."""

        return self._items.pop(index)

    def find(self, value: str) -> list[Word]:
        """
        Search for words in the vocabulary by name.

        The search is case-insensitive and returns all words whose name
        exactly matches the specified string.

        Parameters
        ----------
        value:
            The string to search for within the word names.

        Returns
        -------
        list[Word]
            A list of matching `Word` objects.
        """

        assert isinstance(value, str), type(value)

        search_term = value.lower()
        return [
            item for item in self._items if search_term == item.name.lower()
        ]

    def match(self, pattern: str) -> list[Word]:
        """
        Search for words in the vocabulary using a regular expression.

        Parameters
        ----------
        pattern:
            The regular expression pattern to match against word names.

        Returns
        -------
        list[Word]
            A list of matching `Word` objects.
        """

        assert isinstance(pattern, str), type(pattern)

        regex = re.compile(pattern)
        return [item for item in self._items if regex.search(item.name)]

    def filter(self, predicate: Callable[[Word], bool]) -> list[Word]:
        """
        Search for words in the vocabulary using a predicate function.

        Parameters
        ----------
        predicate:
            A function that takes a `Word` and returns `True` if it should
            be included in the result.

        Returns
        -------
        list[Word]
            A list of `Word` objects for which the predicate returned `True`.
        """

        assert callable(predicate), type(predicate)

        return [item for item in self._items if predicate(item)]

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

    @staticmethod
    def _word_to_dict(word: Word) -> dict[str, object]:
        """
        Change a `Word` dataclass to a dict that you can convert to JSON.
        """

        def _convert(obj: object) -> object:
            if isinstance(obj, enum.Enum):
                return obj.value
            if isinstance(obj, dict):
                return {k: _convert(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [_convert(i) for i in obj]
            return obj

        raw: dict[str, object] = dataclasses.asdict(word)
        result = _convert(raw)
        assert isinstance(result, dict)
        return result

    def write_jsonl_text(
        self,
    ) -> list[str]:
        """
        Serialise the vocabulary to a list of JSONL lines.

        Each element in the returned list is a single JSON-encoded string
        representing one `Word`, without a trailing newline.

        Parameters
        ----------

        Returns
        -------
        list[str]
            One JSON string per `Word`.
        """

        return [
            json.dumps(Vocab._word_to_dict(word), ensure_ascii=False)
            for word in self._items
        ]

    def write_jsonl_file(
        self,
        path: Path,
        *,
        overwrite: bool = False,
        encoding: str = "utf-8",
        create_parents: bool = False,
    ) -> int:
        """
        Write the vocabulary to a JSONL file.

        Each `Word` is serialised as a single JSON line by delegating to
        :meth:`write_jsonl_text`.

        Parameters
        ----------
        path:
            Destination file path.
        overwrite:
            When ``False`` (default) raise ``FileExistsError`` if *path*
            already exists.
        encoding:
            File encoding (default ``"utf-8"``).
        create_parents:
            When ``True`` create any missing parent directories.

        Returns
        -------
        int
            Number of words written.
        """

        assert isinstance(path, Path), type(path)
        assert isinstance(overwrite, bool), type(overwrite)
        assert isinstance(encoding, str), type(encoding)
        assert isinstance(create_parents, bool), type(create_parents)

        if path.exists() and not overwrite:
            raise FileExistsError(path)

        if create_parents:
            path.parent.mkdir(parents=True, exist_ok=True)

        lines = self.write_jsonl_text()
        with open(path, "w", encoding=encoding) as f:
            f.writelines(line + "\n" for line in lines)

        return len(lines)
