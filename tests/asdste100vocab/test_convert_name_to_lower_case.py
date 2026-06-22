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

"""
Convert all 'name' fields to lower case in a JSONL word file.

This test module serves a dual purpose:
  1. Unit tests that verify the name-lowercasing transformation function
     against a small JSONL fixture.
  2. An executable script that, when run directly, applies the transformation
     to the production data file and writes the result to a new file.

Usage as a script:
    python -m tests.asdste100vocab.test_convert_name_to_lower_case

The script reads:
    src/biz/dfch/asdste100vocab/data/asdste100_issue9_base.jsonl

And writes to:
    src/biz/dfch/asdste100vocab/data/asdste100_issue9_base_names_lower.jsonl
"""

import json
import unittest
from pathlib import Path

# ---------------------------------------------------------------------------
# Transformation helpers
# ---------------------------------------------------------------------------


def _lower_note_words(words: list) -> list:
    """Recursively lower-case the 'name' field of all words in a note."""
    result = []
    for word in words:
        result.append(_lower_word_name(word))
    return result


def _lower_word_name(word: dict) -> dict:
    """
    Return a copy of *word* with the 'name' field converted to lower case.

    The transformation is applied recursively to:
      - ``alternatives[].name``
      - ``note.words[].name``
    """
    word = dict(word)

    if "name" in word and isinstance(word["name"], str):
        word["name"] = word["name"].lower()

    if "alternatives" in word and isinstance(word["alternatives"], list):
        word["alternatives"] = [
            _lower_word_name(alt) for alt in word["alternatives"]
        ]

    if (
        "note" in word
        and isinstance(word["note"], dict)
        and "words" in word["note"]
        and isinstance(word["note"]["words"], list)
    ):
        note = dict(word["note"])
        note["words"] = _lower_note_words(note["words"])
        word["note"] = note

    return word


def convert_names_to_lower_case(input_path: Path, output_path: Path) -> int:
    """
    Read *input_path* line by line, lower-case every 'name' field
    (top-level, inside alternatives, and inside note.words), and write
    the result to *output_path*.

    Returns the number of lines successfully converted.
    """
    count = 0

    with (
        input_path.open(encoding="utf-8") as fh_in,
        output_path.open("w", encoding="utf-8") as fh_out,
    ):
        for lineno, raw_line in enumerate(fh_in, start=1):
            raw_line = raw_line.rstrip("\n")
            if not raw_line.strip():
                continue

            try:
                word = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"JSON decode error on line {lineno}: {exc}"
                ) from exc

            converted = _lower_word_name(word)
            fh_out.write(json.dumps(converted, ensure_ascii=False) + "\n")
            count += 1

    return count


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------


class TestConvertNameToLowerCase(unittest.TestCase):

    FIXTURE = Path(__file__).parent / "test_convert_name_to_lower_case.jsonl"

    def _load_fixture(self) -> list[dict]:
        words = []
        with self.FIXTURE.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    words.append(json.loads(line))
        return words

    # ------------------------------------------------------------------
    # _lower_word_name unit tests
    # ------------------------------------------------------------------

    def test_top_level_name_is_lowercased(self):
        word = {"name": "ABSORB", "alternatives": [], "note": None}
        result = _lower_word_name(word)
        self.assertEqual("absorb", result["name"])

    def test_already_lower_name_is_unchanged(self):
        word = {"name": "abaft", "alternatives": [], "note": None}
        result = _lower_word_name(word)
        self.assertEqual("abaft", result["name"])

    def test_mixed_case_name_is_lowercased(self):
        word = {"name": "AbSoRb", "alternatives": [], "note": None}
        result = _lower_word_name(word)
        self.assertEqual("absorb", result["name"])

    def test_alternative_name_is_lowercased(self):
        word = {
            "name": "abaft",
            "alternatives": [
                {"name": "AFT OF", "alternatives": [], "note": None}
            ],
            "note": None,
        }
        result = _lower_word_name(word)
        self.assertEqual("aft of", result["alternatives"][0]["name"])

    def test_multiple_alternative_names_are_lowercased(self):
        word = {
            "name": "abandon",
            "alternatives": [
                {"name": "GO", "alternatives": [], "note": None},
                {"name": "STOP", "alternatives": [], "note": None},
            ],
            "note": None,
        }
        result = _lower_word_name(word)
        self.assertEqual("go", result["alternatives"][0]["name"])
        self.assertEqual("stop", result["alternatives"][1]["name"])

    def test_note_word_name_is_lowercased(self):
        word = {
            "name": "BE",
            "alternatives": [],
            "note": {
                "value": "No other verb forms.",
                "words": [
                    {"name": "OTHER_WORD0"},
                    {"name": "OTHER_WORD1"},
                ],
                "ste_example": None,
                "nonste_example": None,
            },
        }
        result = _lower_word_name(word)
        assert result["note"] is not None
        self.assertEqual("other_word0", result["note"]["words"][0]["name"])
        self.assertEqual("other_word1", result["note"]["words"][1]["name"])

    def test_none_note_is_preserved(self):
        word = {"name": "ABSORB", "alternatives": [], "note": None}
        result = _lower_word_name(word)
        self.assertIsNone(result["note"])

    def test_original_dict_is_not_mutated(self):
        word = {"name": "ABSORB", "alternatives": [], "note": None}
        _ = _lower_word_name(word)
        self.assertEqual("ABSORB", word["name"])

    # ------------------------------------------------------------------
    # convert_names_to_lower_case integration tests (using fixture file)
    # ------------------------------------------------------------------

    def test_fixture_file_exists(self):
        self.assertTrue(
            self.FIXTURE.exists(),
            f"Fixture file not found: {self.FIXTURE}",
        )

    def test_fixture_line_count(self):
        words = self._load_fixture()
        self.assertEqual(4, len(words))

    def test_convert_produces_output_file(self, tmp_path=None):
        if tmp_path is None:
            import tempfile  # pylint: disable=C0415

            tmp_path = Path(tempfile.mkdtemp())

        output = tmp_path / "out.jsonl"
        count = convert_names_to_lower_case(self.FIXTURE, output)

        self.assertTrue(output.exists())
        self.assertEqual(4, count)

    def test_convert_top_level_name_lowercased(self, tmp_path=None):
        if tmp_path is None:
            import tempfile  # pylint: disable=C0415

            tmp_path = Path(tempfile.mkdtemp())

        output = tmp_path / "out.jsonl"
        convert_names_to_lower_case(self.FIXTURE, output)

        words = []
        with output.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    words.append(json.loads(line))

        self.assertEqual("absorb", words[0]["name"])
        self.assertEqual("abaft", words[1]["name"])
        self.assertEqual("abandon", words[2]["name"])
        self.assertEqual("be", words[3]["name"])

    def test_convert_alternative_names_lowercased(self, tmp_path=None):
        if tmp_path is None:
            import tempfile

            tmp_path = Path(tempfile.mkdtemp())

        output = tmp_path / "out.jsonl"
        convert_names_to_lower_case(self.FIXTURE, output)

        words = []
        with output.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    words.append(json.loads(line))

        # line 2: abaft -> alternatives[0].name == "AFT OF" -> "aft of"
        self.assertEqual("aft of", words[1]["alternatives"][0]["name"])

        # line 3: abandon -> alternatives[0].name == "GO", [1].name == "STOP"
        self.assertEqual("go", words[2]["alternatives"][0]["name"])
        self.assertEqual("stop", words[2]["alternatives"][1]["name"])

    def test_convert_note_word_names_lowercased(self, tmp_path=None):
        if tmp_path is None:
            import tempfile

            tmp_path = Path(tempfile.mkdtemp())

        output = tmp_path / "out.jsonl"
        convert_names_to_lower_case(self.FIXTURE, output)

        words = []
        with output.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    words.append(json.loads(line))

        # line 4: BE -> note.words[0].name == "OTHER_WORD0" -> "other_word0"
        note = words[3]["note"]
        self.assertIsNotNone(note)
        self.assertEqual("other_word0", note["words"][0]["name"])
        self.assertEqual("other_word1", note["words"][1]["name"])

    def test_convert_non_name_fields_are_unchanged(self, tmp_path=None):
        if tmp_path is None:
            import tempfile

            tmp_path = Path(tempfile.mkdtemp())

        output = tmp_path / "out.jsonl"
        convert_names_to_lower_case(self.FIXTURE, output)

        words = []
        with output.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    words.append(json.loads(line))

        # status, type_, source, category must be untouched
        self.assertEqual("approved", words[0]["status"])
        self.assertEqual("v", words[0]["type_"])
        self.assertEqual("STE100:9", words[0]["source"])
        self.assertEqual("0", words[0]["category"])


# ---------------------------------------------------------------------------
# Script entry-point: apply transformation to production data file
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    PROJECT_ROOT = Path(__file__).parents[2]
    DATA_DIR = PROJECT_ROOT / "src" / "biz" / "dfch" / "asdste100vocab" / "data"

    input_file = DATA_DIR / "asdste100_issue9_base.jsonl"
    output_file = DATA_DIR / "asdste100_issue9_base_names_lower.jsonl"

    if not input_file.exists():
        print(f"ERROR: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    print(f"Input : {input_file}")
    print(f"Output: {output_file}")
    print("Converting ...")

    total = convert_names_to_lower_case(input_file, output_file)

    print(f"Done. {total} lines written to {output_file}")
