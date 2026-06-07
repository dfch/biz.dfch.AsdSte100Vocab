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
from src.biz.dfch.asdste100vocab.word_meaning import WordMeaning
from src.biz.dfch.asdste100vocab.word_status import WordStatus


class TestWordMeaning(unittest.TestCase):

    def test_meaning(self) -> None:
        """Temporary test that creates an updated word file."""

        sut = Vocab(
            use_ste100=True,
            use_ste100_technical_word=False,
        )

        for w in list(sut):
            if WordStatus.REJECTED == w.status:
                continue
            if 1 >= len(w.meanings):
                continue

            meaning: WordMeaning | None = None
            artifacts: list[WordMeaning] = []

            for m in w.meanings:
                has_zwsp = "\u200b" in m.value

                print(f"{w.name} [{w.type_.name}]")
                if not has_zwsp and m.value.strip():
                    meaning = m
                    continue

                assert meaning
                meaning.ste_example.extend(m.ste_example)
                meaning.nonste_example.extend(m.nonste_example)
                artifacts.append(m)

            for artifact in artifacts:
                w.meanings.remove(artifact)

        sut.write_jsonl_file(
            Path(
                "./src/biz/dfch/asdste100vocab/data/asdste100_issue9_base.jsonl"
            ),
            overwrite=True,
        )
