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

# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116

import unittest

from src.biz.dfch.asdste100vocab.vocab import Vocab
from src.biz.dfch.asdste100vocab.word import Word
from src.biz.dfch.asdste100vocab.word_note import WordNote


class TestVocabFindExcept(unittest.TestCase):
    WORD_NAME = "except"

    @classmethod
    def setUpClass(cls):
        cls.sut = Vocab(
            use_ste100=True,
            use_ste100_technical_word=False,
        )
        cls.results = cls.sut.find(cls.WORD_NAME)
        cls.word = cls.results[0] if cls.results else None

    def test_find_returns_exactly_one_result(self):
        self.assertEqual(1, len(self.results))

    def test_word_name_is_except(self):
        self.assertIsNotNone(self.word)
        assert isinstance(self.word, Word), type(self.word)
        self.assertEqual(self.WORD_NAME, self.word.name.lower())

    def test_word_has_no_meanings(self):
        self.assertIsNotNone(self.word)
        assert isinstance(self.word, Word), type(self.word)
        self.assertEqual(0, len(self.word.meanings))

    def test_word_has_no_alternatives(self):
        self.assertIsNotNone(self.word)
        assert isinstance(self.word, Word), type(self.word)
        self.assertEqual(0, len(self.word.alternatives))

    def test_word_has_exactly_two_ste_examples(self):
        self.assertIsNotNone(self.word)
        assert isinstance(self.word, Word), type(self.word)
        self.assertEqual(2, len(self.word.ste_example))

    def test_word_has_exactly_two_non_ste_examples(self):
        self.assertIsNotNone(self.word)
        assert isinstance(self.word, Word), type(self.word)
        self.assertEqual(2, len(self.word.nonste_example))

    def test_word_has_a_note(self):
        self.assertIsNotNone(self.word)
        assert isinstance(self.word, Word), type(self.word)
        self.assertIsNotNone(self.word.note)

    def test_word_note_is_word_note_instance(self):
        self.assertIsNotNone(self.word)
        assert isinstance(self.word, Word), type(self.word)
        self.assertIsInstance(self.word.note, WordNote)

    def test_word_note_value_is_non_empty(self):
        self.assertIsNotNone(self.word)
        assert isinstance(self.word, Word), type(self.word)
        self.assertIsNotNone(self.word.note)
        assert isinstance(self.word.note, WordNote), type(self.word.note)
        self.assertIsNotNone(self.word.note)
        self.assertIsNotNone(self.word.note.value)
        assert isinstance(self.word.note.value, str), type(self.word.note.value)
        self.assertNotEqual("", self.word.note.value.strip())


if __name__ == "__main__":
    unittest.main()
