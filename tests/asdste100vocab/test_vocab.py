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

    def test_write_jsonl_text_returns_list_of_strings(self):

        word_list = VocabFile.TWO_ITEMS
        fullname = Path(__file__).parent / word_list

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = sut.write_jsonl_text()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertEqual(2, len(result))
        for line in result:
            self.assertIsInstance(line, str)

    def test_write_jsonl_text_each_line_is_valid_json(self):

        import json

        word_list = VocabFile.TWO_ITEMS
        fullname = Path(__file__).parent / word_list

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = sut.write_jsonl_text()

        for line in result:
            parsed = json.loads(line)
            self.assertIsInstance(parsed, dict)
            self.assertIn("name", parsed)

    def test_write_jsonl_text_contains_word_name(self):

        import json

        word_list = VocabFile.TWO_ITEMS
        fullname = Path(__file__).parent / word_list

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = sut.write_jsonl_text()

        self.assertEqual(2, len(result))
        print(result[0])
        self.assertEqual("abaft", json.loads(result[0])["name"])
        print(result[1])
        self.assertEqual("abandon", json.loads(result[1])["name"])

    def test_write_jsonl_text_is_sorted_by_default(self):

        word_list = VocabFile.TWO_ITEMS
        fullname = Path(__file__).parent / word_list

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = sut.write_jsonl_text()

        import json

        names = [json.loads(line)["name"].lower() for line in result]
        self.assertEqual(sorted(names), names)

    def test_write_jsonl_text_roundtrip(self):

        word_list = VocabFile.TWO_ITEMS
        fullname = Path(__file__).parent / word_list

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        lines = sut.write_jsonl_text()

        self.assertEqual(len(sut), len(lines))

        for idx, line in enumerate(lines):
            original = sut[idx]
            result = Vocab.read_jsonl_text(line)

            self.assertIsNotNone(result)
            self.assertEqual(Word, type(result))
            self.assertEqual(original, result)

    def test_write_jsonl_text_empty_vocab_returns_empty_list(self):

        sut = Vocab(
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = sut.write_jsonl_text()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertEqual(0, len(result))

    def test_write_jsonl_text_no_trailing_newlines(self):

        word_list = VocabFile.ONE_ITEM
        fullname = Path(__file__).parent / word_list

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = sut.write_jsonl_text()

        for line in result:
            self.assertFalse(line.endswith("\n"), repr(line))

    def test_replace_succeeds(self):

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

        existing = sut[0]
        self.assertIsNotNone(existing)
        self.assertEqual("abaft", existing.name.lower())

        replacement = sut[1]
        self.assertIsNotNone(replacement)
        self.assertEqual("abandon", replacement.name.lower())

        sut.replace(existing, replacement)

        result = len(sut)
        self.assertEqual(expected, result)

        item = sut[0]
        self.assertEqual("abandon", item.name.lower())

    def test_replace_preserves_length(self):

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

        existing = sut[0]
        replacement = sut[1]

        sut.replace(existing, replacement)

        result = len(sut)
        self.assertEqual(expected, result)

    def test_replace_preserves_position(self):

        word_list = VocabFile.TWO_ITEMS
        fullname = Path(__file__).parent / word_list

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        existing = sut[1]
        self.assertEqual("abandon", existing.name.lower())

        replacement = sut[0]
        self.assertEqual("abaft", replacement.name.lower())

        sut.replace(existing, replacement)

        item = sut[1]
        self.assertEqual("abaft", item.name.lower())

    def test_replace_not_found_throws(self):

        word_list = VocabFile.TWO_ITEMS
        fullname = Path(__file__).parent / word_list

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        not_in_vocab = Vocab.read_jsonl_text(
            r'{"status":"approved","name":"ZZZZ","type_":"n","meanings":[],"spellings":[],"alternatives":[],"source":"STE100:9","category":"0","ste_example":[],"nonste_example":[],"note":null}'
        )
        replacement = sut[0]

        with self.assertRaises(ValueError):
            sut.replace(not_in_vocab, replacement)

    def test_replace_existing_with_none_throws(self):

        word_list = VocabFile.ONE_ITEM
        fullname = Path(__file__).parent / word_list

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        existing = sut[0]

        with self.assertRaises(AssertionError):
            sut.replace(existing, None)  # type: ignore

    def test_replace_none_existing_throws(self):

        word_list = VocabFile.ONE_ITEM
        fullname = Path(__file__).parent / word_list

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        replacement = sut[0]

        with self.assertRaises(AssertionError):
            sut.replace(None, replacement)  # type: ignore

    def test_replace_both_none_throws(self):

        sut = Vocab(
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        with self.assertRaises(AssertionError):
            sut.replace(None, None)  # type: ignore

    def test_replace_with_same_word_is_idempotent(self):

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

        existing = sut[0]
        self.assertEqual("a", existing.name.lower())

        sut.replace(existing, existing)

        result = len(sut)
        self.assertEqual(expected, result)

        item = sut[0]
        self.assertEqual(existing, item)

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

    def test_find_with_one_result(self):
        word_list = VocabFile.TWO_ITEMS
        fullname = Path(__file__).parent / word_list

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = sut.find("abaft")
        self.assertEqual(1, len(result))
        self.assertEqual("abaft", result[0].name.lower())

    def test_find_with_two_results(self):
        word_list = VocabFile.SAME_WORD_TWICE
        fullname = Path(__file__).parent / word_list

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        # Both 'abaft' and 'abandon' contain 'aba'
        result = sut.find("test")
        self.assertEqual(2, len(result))

    def test_find_with_zero_results(self):
        word_list = VocabFile.TWO_ITEMS
        fullname = Path(__file__).parent / word_list

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = sut.find("non-existent-word")
        self.assertEqual(0, len(result))

    def test_find_is_case_insensitive(self):
        word_list = VocabFile.TWO_ITEMS
        fullname = Path(__file__).parent / word_list

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result_upper = sut.find("ABAFT")
        result_lower = sut.find("abaft")

        self.assertEqual(1, len(result_upper))
        self.assertEqual(result_upper, result_lower)

    def test_filter(self):
        word_list = VocabFile.TWO_ITEMS
        fullname = Path(__file__).parent / word_list

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        # Filter for words that have a name with length 5
        result = sut.filter(lambda w: len(w.name) == 5)
        self.assertEqual(1, len(result))
        self.assertEqual("abaft", result[0].name.lower())

    def test_match_with_regex_anchor(self):
        word_list = VocabFile.TWO_ITEMS
        fullname = Path(__file__).parent / word_list

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        # '^aba' matches both 'abaft' and 'abandon'
        result = sut.match("^aba")
        self.assertEqual(2, len(result))

    def test_match_with_zero_results(self):
        word_list = VocabFile.TWO_ITEMS
        fullname = Path(__file__).parent / word_list

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        # Regex that won't match any names
        result = sut.match("[0-9]")
        self.assertEqual(0, len(result))

    def test_match_with_one_result(self):
        word_list = VocabFile.TWO_ITEMS
        fullname = Path(__file__).parent / word_list

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        # End of string anchor
        result = sut.match("t$")
        self.assertEqual(1, len(result))
        self.assertEqual("abaft", result[0].name.lower())
