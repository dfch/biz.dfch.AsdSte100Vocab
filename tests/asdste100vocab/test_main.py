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

import src.biz.dfch.asdste100vocab as vocab


class TestMain(unittest.TestCase):
    def test_import(self):
        self.assertEqual("Word", vocab.Word.__name__)
        self.assertEqual("Word", vocab.Word.__qualname__)

        self.assertEqual("WordCategory", vocab.WordCategory.__name__)
        self.assertEqual("WordCategory", vocab.WordCategory.__qualname__)

        self.assertEqual("WordMeaning", vocab.WordMeaning.__name__)
        self.assertEqual("WordMeaning", vocab.WordMeaning.__qualname__)

        self.assertEqual("WordNote", vocab.WordNote.__name__)
        self.assertEqual("WordNote", vocab.WordNote.__qualname__)

        self.assertEqual("WordSource", vocab.WordSource.__name__)
        self.assertEqual("WordSource", vocab.WordSource.__qualname__)

        self.assertEqual("WordStatus", vocab.WordStatus.__name__)
        self.assertEqual("WordStatus", vocab.WordStatus.__qualname__)

        self.assertEqual("WordType", vocab.WordType.__name__)
        self.assertEqual("WordType", vocab.WordType.__qualname__)
