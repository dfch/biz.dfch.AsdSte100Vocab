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


class TestVocabClear(unittest.TestCase):
    def test_clear_returns_self(self):
        sut = Vocab()

        result = sut.clear()

        self.assertIs(sut, result)

    def test_clear_returns_vocab_instance(self):
        sut = Vocab()

        result = sut.clear()

        self.assertIsInstance(result, Vocab)

    def test_clear_empties_vocab(self):
        sut = Vocab()
        self.assertGreater(len(sut), 0)

        sut.clear()

        self.assertEqual(0, len(sut))

    def test_clear_already_empty_vocab_stays_empty(self):
        sut = Vocab(
            use_ste100=False,
            use_ste100_technical_word=False,
        )
        self.assertEqual(0, len(sut))

        sut.clear()

        self.assertEqual(0, len(sut))

    def test_clear_twice_stays_empty(self):
        sut = Vocab()

        sut.clear()
        self.assertEqual(0, len(sut))

        sut.clear()
        self.assertEqual(0, len(sut))
