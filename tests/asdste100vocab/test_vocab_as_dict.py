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

from .vocab_file import VocabFile


class TestVocabAsDict(unittest.TestCase):

    def test_as_dict_returns_empty_list(self):

        sut = Vocab(
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = sut.as_dict()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertEqual(0, len(result))

    def test_as_dict_returns_single_item(self):

        fullname = Path(__file__).parent / VocabFile.ONE_ITEM

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = sut.as_dict()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))
        self.assertIsInstance(result[0], dict)
        self.assertEqual("A", result[0]["name"])

    def test_as_dict_returns_two_items(self):

        fullname = Path(__file__).parent / VocabFile.TWO_ITEMS

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )

        result = sut.as_dict()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertEqual(2, len(result))
        self.assertIsInstance(result[0], dict)
        self.assertIsInstance(result[1], dict)
        self.assertEqual("abaft", result[0]["name"])
        self.assertEqual("abandon", result[1]["name"])


if __name__ == "__main__":
    unittest.main()