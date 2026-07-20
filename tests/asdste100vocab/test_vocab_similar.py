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

from pathlib import Path
import unittest

from src.biz.dfch.asdste100vocab.vocab import Vocab
from src.biz.dfch.asdste100vocab.word import Word

from .vocab_file import VocabFile


class TestVocabSimilar(unittest.TestCase):
    def _make_sut(self, vocab_file: VocabFile) -> Vocab:
        fullname = Path(__file__).parent / vocab_file
        return Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

    # ------------------------------------------------------------------
    # Return type
    # ------------------------------------------------------------------

    def test_similar_returns_list(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        result = sut.similar("abaft")

        self.assertIsInstance(result, list)

    def test_similar_returns_list_of_words(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        result = sut.similar("abaft")

        for item in result:
            self.assertIsInstance(item, Word)

    # ------------------------------------------------------------------
    # Exact match
    # ------------------------------------------------------------------

    def test_similar_exact_match_returns_word(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        result = sut.similar("abaft")

        self.assertEqual(1, len(result))
        self.assertEqual("abaft", result[0].name)

    # ------------------------------------------------------------------
    # Typo / near match
    # ------------------------------------------------------------------

    def test_similar_typo_returns_close_match(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        # "abaaft" is a plausible typo for "abaft"
        result = sut.similar("abaaft")

        self.assertEqual(1, len(result))
        self.assertEqual("abaft", result[0].name)

    def test_similar_with_full_vocab_typo_returns_result(self):
        sut = Vocab(use_ste100=True, use_ste100_technical_word=False)

        # "reinstalation" is close enough to "reinstallation" for difflib
        result = sut.similar("reinstalation")

        self.assertGreater(len(result), 0)
        names = [w.name.lower() for w in result]
        self.assertIn("reinstallation", names)

    # ------------------------------------------------------------------
    # No match
    # ------------------------------------------------------------------

    def test_similar_no_match_returns_empty_list(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        result = sut.similar("zzzzzzzzz")

        self.assertEqual(0, len(result))

    # ------------------------------------------------------------------
    # n parameter
    # ------------------------------------------------------------------

    def test_similar_n_limits_results(self):
        sut = Vocab(use_ste100=True, use_ste100_technical_word=True)

        result = sut.similar("instal", n=2, cutoff=0.5)

        self.assertLessEqual(len(result), 2)

    def test_similar_n_default_is_three(self):
        sut = Vocab(use_ste100=True, use_ste100_technical_word=True)

        result = sut.similar("instal", n=3, cutoff=0.5)

        self.assertLessEqual(len(result), 3)

    # ------------------------------------------------------------------
    # cutoff parameter
    # ------------------------------------------------------------------

    def test_similar_high_cutoff_returns_fewer_results(self):
        sut = Vocab(use_ste100=True, use_ste100_technical_word=True)

        result_low = sut.similar("instal", n=10, cutoff=0.5)
        result_high = sut.similar("instal", n=10, cutoff=0.9)

        self.assertGreaterEqual(len(result_low), len(result_high))

    def test_similar_cutoff_zero_returns_results(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        result = sut.similar("abaft", cutoff=0.0)

        self.assertGreater(len(result), 0)

    def test_similar_cutoff_one_exact_match_only(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        result = sut.similar("abaft", cutoff=1.0)

        self.assertEqual(1, len(result))
        self.assertEqual("abaft", result[0].name)

    def test_similar_cutoff_one_no_match_returns_empty(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        # "abaaft" will not score 1.0 against any word
        result = sut.similar("abaaft", cutoff=1.0)

        self.assertEqual(0, len(result))

    # ------------------------------------------------------------------
    # Empty vocabulary
    # ------------------------------------------------------------------

    def test_similar_empty_vocab_returns_empty_list(self):
        sut = Vocab(
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = sut.similar("abaft")

        self.assertEqual(0, len(result))

    # ------------------------------------------------------------------
    # Guard assertions
    # ------------------------------------------------------------------

    def test_similar_none_value_throws(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        with self.assertRaises(AssertionError):
            sut.similar(None)  # type: ignore

    def test_similar_invalid_n_zero_throws(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        with self.assertRaises(AssertionError):
            sut.similar("abaft", n=0)

    def test_similar_invalid_n_negative_throws(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        with self.assertRaises(AssertionError):
            sut.similar("abaft", n=-1)

    def test_similar_invalid_cutoff_below_zero_throws(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        with self.assertRaises(AssertionError):
            sut.similar("abaft", cutoff=-0.1)

    def test_similar_invalid_cutoff_above_one_throws(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        with self.assertRaises(AssertionError):
            sut.similar("abaft", cutoff=1.1)
