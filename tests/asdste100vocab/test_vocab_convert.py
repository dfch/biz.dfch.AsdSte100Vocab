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

import json
from pathlib import Path
import unittest

from .vocab_file import VocabFile


class TestVocabConvert(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fullname = Path(__file__).parent / VocabFile.EXCEPT
        cls.JSONL_EXCEPT = fullname.read_text(encoding="utf-8").strip()

    def test_json_loads_returns_dict(self):
        result = json.loads(self.JSONL_EXCEPT)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_json_loads_name_is_except(self):
        result = json.loads(self.JSONL_EXCEPT)

        self.assertEqual("except", result["name"])

    def test_json_loads_status_is_rejected(self):
        result = json.loads(self.JSONL_EXCEPT)

        self.assertEqual("rejected", result["status"])

    def test_json_loads_type_is_prep(self):
        result = json.loads(self.JSONL_EXCEPT)

        self.assertEqual("prep", result["type_"])

    def test_json_loads_meanings_is_empty(self):
        result = json.loads(self.JSONL_EXCEPT)

        self.assertIsInstance(result["meanings"], list)
        self.assertEqual(0, len(result["meanings"]))

    def test_json_loads_alternatives_is_empty(self):
        result = json.loads(self.JSONL_EXCEPT)

        self.assertIsInstance(result["alternatives"], list)
        self.assertEqual(0, len(result["alternatives"]))

    def test_json_loads_ste_example_has_two_entries(self):
        result = json.loads(self.JSONL_EXCEPT)

        self.assertIsInstance(result["ste_example"], list)
        self.assertEqual(2, len(result["ste_example"]))

    def test_json_loads_nonste_example_has_two_entries(self):
        result = json.loads(self.JSONL_EXCEPT)

        self.assertIsInstance(result["nonste_example"], list)
        self.assertEqual(2, len(result["nonste_example"]))

    def test_json_loads_note_is_present(self):
        result = json.loads(self.JSONL_EXCEPT)

        self.assertIsNotNone(result["note"])
        self.assertIsInstance(result["note"], dict)

    def test_json_loads_note_value_is_non_empty(self):
        result = json.loads(self.JSONL_EXCEPT)

        self.assertIsInstance(result["note"]["value"], str)
        self.assertNotEqual("", result["note"]["value"].strip())


if __name__ == "__main__":
    unittest.main()
