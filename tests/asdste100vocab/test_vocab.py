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
# pylint: disable=R0904

from pathlib import Path
import unittest

from src.biz.dfch.asdste100vocab.vocab import Vocab
from src.biz.dfch.asdste100vocab.word import Word
from src.biz.dfch.asdste100vocab.word_status import WordStatus
from src.biz.dfch.asdste100vocab.word_type import WordType

from .vocab_file import VocabFile


class TestVocab(unittest.TestCase):

    def test_load_all(self):

        expected = 2979

        sut = Vocab(
            use_ste100=True,
            use_ste100_technical_word=True,
        )
        self.assertIsNotNone(sut)
        result = len(sut)

        self.assertEqual(expected, result)

    def test_load_all_filter_all(self):

        def predicate(_: Word) -> bool:
            return False

        expected = 0

        sut = Vocab(
            use_ste100=True,
            use_ste100_technical_word=True,
            predicate=predicate,
        )
        self.assertIsNotNone(sut)
        result = len(sut)

        self.assertEqual(expected, result)

    def test_load_nothing(self):

        expected = 0

        sut = Vocab(
            use_ste100=False,
            use_ste100_technical_word=False,
        )
        self.assertIsNotNone(sut)
        result = len(sut)

        self.assertEqual(expected, result)

    def test_ste100_only(self):

        expected = 2200

        sut = Vocab(
            use_ste100=True,
            use_ste100_technical_word=False,
        )
        self.assertIsNotNone(sut)
        result = len(sut)

        self.assertEqual(expected, result)

    def test_technical_words_only(self):

        expected = 779

        sut = Vocab(
            use_ste100=False,
            use_ste100_technical_word=True,
        )
        self.assertIsNotNone(sut)
        result = len(sut)

        self.assertEqual(expected, result)

    def test_load_technical_noun_only(self):

        def predicate(word: Word) -> bool:
            return word.type_ == WordType.TECHNICAL_NOUN

        expected = 616

        sut = Vocab(
            use_ste100=True,
            use_ste100_technical_word=True,
            predicate=predicate,
        )
        self.assertIsNotNone(sut)
        result = len(sut)

        self.assertEqual(expected, result)

    def test_load_technical_verb_only(self):

        def predicate(word: Word) -> bool:
            return word.type_ == WordType.TECHNICAL_VERB

        expected = 163

        sut = Vocab(
            use_ste100=True,
            use_ste100_technical_word=True,
            predicate=predicate,
        )
        self.assertIsNotNone(sut)
        result = len(sut)

        self.assertEqual(expected, result)

    def test_default_params(self):
        """Initialize `Vocab` with default parameters."""

        expected = 2200

        sut = Vocab()
        self.assertIsNotNone(sut)
        result = len(sut)

        self.assertEqual(expected, result)

    def test_load_custom_word_list(self):

        word_list = VocabFile.ONE_ITEM
        fullname = Path(__file__).parent / word_list

        expected = 1

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
        )
        self.assertIsNotNone(sut)
        result = len(sut)

        self.assertEqual(expected, result)

    def test_load_non_existent_word_list_throws(self):

        word_list = VocabFile.NON_EXISTENT_FILE
        fullname = Path(__file__).parent / word_list

        with self.assertRaises(FileNotFoundError) as ex:
            _ = Vocab(
                files=[fullname],
            )
        self.assertIsNotNone(ex)
        self.assertIsNotNone(ex.exception)
        self.assertTrue(word_list in str(ex.exception), str(ex.exception))

    def test_load_multiple_word_lists(self):

        word_list1 = VocabFile.ONE_ITEM
        fullname1 = Path(__file__).parent / word_list1
        word_list2 = VocabFile.TWO_ITEMS
        fullname2 = Path(__file__).parent / word_list2

        expected = 3

        sut = Vocab(
            files=[fullname1, fullname2],
            use_ste100=False,
        )
        self.assertIsNotNone(sut)
        result = len(sut)

        self.assertEqual(expected, result)

    def test_load_all_and_multiple_word_lists(self):

        word_list1 = VocabFile.ONE_ITEM
        fullname1 = Path(__file__).parent / word_list1
        word_list2 = VocabFile.TWO_ITEMS
        fullname2 = Path(__file__).parent / word_list2

        expected = 2982

        sut = Vocab(
            files=[fullname1, fullname2],
            use_ste100=True,
            use_ste100_technical_word=True,
        )
        self.assertIsNotNone(sut)
        result = len(sut)

        self.assertEqual(expected, result)

    def test_iterate(self):

        word_list1 = VocabFile.ONE_ITEM
        fullname1 = Path(__file__).parent / word_list1
        word_list2 = VocabFile.TWO_ITEMS
        fullname2 = Path(__file__).parent / word_list2

        expected = 3

        sut = Vocab(
            files=[fullname1, fullname2],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = len(sut)
        self.assertEqual(expected, result)

        idx = 0
        for idx, word in enumerate(sut):
            self.assertTrue(word.name.lower().startswith("a"))

        self.assertEqual(expected - 1, idx)

    def test_pop(self):

        word_list = VocabFile.ONE_ITEM
        fullname = Path(__file__).parent / word_list

        expected = 0

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        item = sut.pop()
        self.assertIsNotNone(item)
        self.assertEqual("a", item.name.lower())

        result = len(sut)
        self.assertEqual(expected, result)

    def test_pop_empty_throws(self):

        expected = 0

        sut = Vocab(
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = len(sut)
        self.assertEqual(expected, result)

        with self.assertRaises(IndexError):
            _ = sut.pop()

    def test_del(self):

        word_list = VocabFile.ONE_ITEM
        fullname = Path(__file__).parent / word_list

        expected = 0

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = len(sut)
        self.assertNotEqual(expected, result)

        del sut[0]

        result = len(sut)
        self.assertEqual(expected, result)

    def test_del_throws(self):

        word_list = VocabFile.ONE_ITEM
        fullname = Path(__file__).parent / word_list

        expected = 1

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = len(sut)
        self.assertEqual(expected, result)

        with self.assertRaises(IndexError):
            del sut[42]

        result = len(sut)
        self.assertEqual(expected, result)

    def test_pop_first(self):

        word_list = VocabFile.TWO_ITEMS
        fullname = Path(__file__).parent / word_list

        expected = 1

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        item = sut.pop(0)
        self.assertIsNotNone(item)
        self.assertEqual("abaft", item.name.lower())

        result = len(sut)
        self.assertEqual(expected, result)

    def test_index(self):

        word_list = VocabFile.TWO_ITEMS
        fullname = Path(__file__).parent / word_list

        expected = 2

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = len(sut)
        self.assertEqual(expected, result)

        item = sut[0]
        self.assertIsNotNone(item)
        self.assertEqual("abaft", item.name.lower())

        item = sut[1]
        self.assertIsNotNone(item)
        self.assertEqual("abandon", item.name.lower())

    def test_index_raises(self):

        word_list = VocabFile.TWO_ITEMS
        fullname = Path(__file__).parent / word_list

        expected = 2

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = len(sut)
        self.assertEqual(expected, result)

        with self.assertRaises(IndexError):
            _ = sut[42]

    def test_append(self):

        word_list = VocabFile.ONE_ITEM
        fullname = Path(__file__).parent / word_list

        expected = 1

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = len(sut)
        self.assertEqual(expected, result)

        item = sut.pop()
        self.assertIsNotNone(item)
        self.assertEqual("a", item.name.lower())

        result = len(sut)
        self.assertEqual(expected - 1, result)

        sut.append(item)

        result = len(sut)
        self.assertEqual(expected, result)

    def test_append_throws(self):

        word_list = VocabFile.ONE_ITEM
        fullname = Path(__file__).parent / word_list

        expected = 1

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = len(sut)
        self.assertEqual(expected, result)

        with self.assertRaises(AssertionError):
            sut.append(None)  # type: ignore

    def test_extend(self):

        word_list = VocabFile.ONE_ITEM
        fullname = Path(__file__).parent / word_list

        expected = 1

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = len(sut)
        self.assertEqual(expected, result)

        item0 = sut[0]
        self.assertIsNotNone(item0)
        self.assertEqual("a", item0.name.lower())

        item1 = sut[0]
        self.assertIsNotNone(item1)
        self.assertEqual("a", item1.name.lower())

        sut.extend([item0, item1])
        result = len(sut)
        self.assertEqual(expected + 2, result)

    def test_remove(self):

        word_list = VocabFile.ONE_ITEM
        fullname = Path(__file__).parent / word_list

        expected = 1

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = len(sut)
        self.assertEqual(expected, result)

        item = sut[0]
        self.assertIsNotNone(item)
        self.assertEqual("a", item.name.lower())

        sut.extend([item])
        result = len(sut)
        self.assertEqual(expected + 1, result)

        sut.remove(item)

        result = len(sut)
        self.assertEqual(expected, result)

    def test_read_jsonl_text(self):

        # pylint: disable=C0301
        jsonl = r"""{"status":"approved","name":"A","type_":"art","meanings":[{"value":"Function word: indefinite article","ste_example":"A FUEL PUMP IS INSTALLED IN ZONE 10.","nonste_example":"","note":null}],"spellings":[],"alternatives":[],"source":"STE100:9","category":"0","ste_example":[],"nonste_example":[],"note":{"value":"","words":[],"ste_example":null,"nonste_example":null}}"""

        result = Vocab.read_jsonl_text(jsonl)

        self.assertIsNotNone(result)
        self.assertEqual(Word, type(result))
        self.assertTrue(result.name.lower().startswith("a"))

    def test_sort_reverse(self):

        word_list = VocabFile.TWO_ITEMS
        fullname = Path(__file__).parent / word_list

        expected = 2

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = len(sut)
        self.assertEqual(expected, result)

        item = sut[0]
        self.assertIsNotNone(item)
        self.assertEqual("abaft", item.name.lower())

        sut.sort(reverse=True)

        item = sut[-1]
        self.assertIsNotNone(item)
        self.assertEqual("abaft", item.name.lower())

    def test_sort_custom_key(self):

        word_list = VocabFile.THREE_ITEMS
        fullname = Path(__file__).parent / word_list

        expected = 3

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = len(sut)
        self.assertEqual(expected, result)

        item = sut[0]
        self.assertIsNotNone(item)
        self.assertEqual("a", item.name.lower())

        item = sut[-1]
        self.assertIsNotNone(item)
        self.assertEqual("you", item.name.lower())

        sut.sort(key=lambda w: w.status)

        item = sut[-1]
        self.assertIsNotNone(item)
        self.assertEqual("abaft", item.name.lower())
        self.assertEqual(WordStatus.REJECTED, item.status)
