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


class TestVocabExamine(unittest.TestCase):
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

    def test_examine_returns_list(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        result = sut.examine("abaft")

        self.assertIsInstance(result, list)

    def test_examine_returns_list_of_words(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        result = sut.examine("abaft")

        for item in result:
            self.assertIsInstance(item, Word)

    # ------------------------------------------------------------------
    # Exact match
    # ------------------------------------------------------------------

    def test_examine_exact_match_returns_word(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        result = sut.examine("abaft")

        names = [w.name for w in result]
        self.assertIn("abaft", names)

    # ------------------------------------------------------------------
    # Partial / substring match
    # ------------------------------------------------------------------

    def test_examine_substring_is_included(self):
        sut = Vocab(use_ste100=True, use_ste100_technical_word=True)

        # "install" is a substring of:
        # * "reinstall"
        # * "installation"
        # * "reinstallation"
        result = sut.examine("install")

        names = [w.name.lower() for w in result]
        self.assertIn("install", names)
        self.assertIn("reinstall", names)
        self.assertIn("reinstallation", names)
        self.assertIn("installation", names)

    def test_examine_prefix_is_included(self):
        sut = Vocab(use_ste100=True, use_ste100_technical_word=True)

        result = sut.examine("install")

        names = [w.name.lower() for w in result]
        # "instead" contains "inst" but not "install" — should NOT appear
        # via partial; verify at least one prefix match is present
        self.assertTrue(any("install" in n for n in names))

    # ------------------------------------------------------------------
    # Fuzzy match
    # ------------------------------------------------------------------

    def test_examine_typo_is_included(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        # "abaaft" is a typo for "abaft" — found via fuzzy
        result = sut.examine("abaaft")

        names = [w.name for w in result]
        self.assertIn("abaft", names)

    # ------------------------------------------------------------------
    # Deduplication
    # ------------------------------------------------------------------

    def test_examine_no_duplicates(self):
        sut = Vocab(use_ste100=True, use_ste100_technical_word=True)

        # "abaft" would be found by both fuzzy and partial
        result = sut.examine("abaft")

        names = [w.name for w in result]
        self.assertEqual(len(names), len(set(names)))

    def test_examine_no_duplicate_objects(self):
        sut = Vocab(use_ste100=True, use_ste100_technical_word=True)

        result = sut.examine("abaft")

        ids = [id(w) for w in result]
        self.assertEqual(len(ids), len(set(ids)))

    # ------------------------------------------------------------------
    # Sorted output
    # ------------------------------------------------------------------

    def test_examine_result_is_sorted(self):
        sut = Vocab(use_ste100=True, use_ste100_technical_word=True)

        result = sut.examine("install")

        names = [w.name.lower() for w in result]
        self.assertEqual(sorted(names), names)

    # ------------------------------------------------------------------
    # No match
    # ------------------------------------------------------------------

    def test_examine_no_match_returns_empty_list(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        result = sut.examine("zzzzzzzzz")

        self.assertEqual(0, len(result))

    # ------------------------------------------------------------------
    # Empty vocabulary
    # ------------------------------------------------------------------

    def test_examine_empty_vocab_returns_empty_list(self):
        sut = Vocab(
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = sut.examine("abaft")

        self.assertEqual(0, len(result))

    # ------------------------------------------------------------------
    # cutoff parameter
    # ------------------------------------------------------------------

    def test_examine_high_cutoff_returns_fewer_fuzzy(self):
        sut = Vocab(use_ste100=True, use_ste100_technical_word=True)

        result_low = sut.examine("install", cutoff=0.3)
        result_high = sut.examine("install", cutoff=0.9)

        self.assertGreaterEqual(len(result_low), len(result_high))

    def test_examine_cutoff_one_still_returns_partial_matches(self):
        sut = Vocab(use_ste100=True, use_ste100_technical_word=True)

        # cutoff=1.0 suppresses all fuzzy results except exact,
        # but partial (regex) matches are always included
        result = sut.examine("install", cutoff=1.0)

        names = [w.name.lower() for w in result]
        self.assertIn("reinstall", names)

    # ------------------------------------------------------------------
    # Guard assertions
    # ------------------------------------------------------------------

    def test_examine_none_value_throws(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        with self.assertRaises(AssertionError):
            sut.examine(None)  # type: ignore

    def test_examine_invalid_cutoff_below_zero_throws(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        with self.assertRaises(AssertionError):
            sut.examine("abaft", cutoff=-0.1)

    def test_examine_invalid_cutoff_above_one_throws(self):
        sut = self._make_sut(VocabFile.TWO_ITEMS)

        with self.assertRaises(AssertionError):
            sut.examine("abaft", cutoff=1.1)
