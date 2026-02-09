# Copyright (c) 2026 Ronald Rink, http://d-fens.ch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116

from pathlib import Path
import unittest

from src.biz.dfch.asdste100vocab.vocab import Vocab
from src.biz.dfch.asdste100vocab.word import Word
from src.biz.dfch.asdste100vocab.word_meaning import WordMeaning
from src.biz.dfch.asdste100vocab.word_note import WordNote
from src.biz.dfch.asdste100vocab.word_status import WordStatus
from src.biz.dfch.asdste100vocab.word_type import WordType

from .vocab_file import VocabFile


class TestWord(unittest.TestCase):

    def test_name_source_status_type(self):

        word_list = VocabFile.COMPLETE
        fullname = Path(__file__).parent / word_list

        expected = Word(
            name="BE",
            status=WordStatus.APPROVED,
            type_=WordType.VERB,
            source="STE100:9",
        )

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )[0]

        self.assertEqual(expected.name, sut.name)
        self.assertEqual(expected.source, sut.source)
        self.assertEqual(expected.status, sut.status)
        self.assertEqual(expected.type_, sut.type_)

    def test_note(self):

        word_list = VocabFile.COMPLETE
        fullname = Path(__file__).parent / word_list

        expected = Word(
            name="BE",
            status=WordStatus.APPROVED,
            type_=WordType.VERB,
            source="STE100:9",
            note=WordNote(
                value="No other verb forms.",
                ste_example="NOTE: This is an ste_example.",
                nonste_example="NOTE: This is a nonste_example.",
                words=[
                    Word(
                        name="OTHER_WORD0",
                    ),
                    Word(
                        name="OTHER_WORD1",
                    ),
                ],
            ),
        )
        assert expected.note is not None

        word = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )[0]

        self.assertIsNotNone(word.note)
        sut = word.note
        assert sut is not None

        self.assertEqual(expected.note.value, sut.value)
        self.assertEqual(expected.note.ste_example, sut.ste_example)
        self.assertEqual(expected.note.nonste_example, sut.nonste_example)
        self.assertIsNotNone(sut.words)
        self.assertEqual(2, len(sut.words))
        note_word = sut.words[0]
        self.assertEqual(expected.note.words[0].name, note_word.name)

    def test_example(self):

        word_list = VocabFile.COMPLETE
        fullname = Path(__file__).parent / word_list

        expected = Word(
            name="BE",
            status=WordStatus.APPROVED,
            type_=WordType.VERB,
            source="STE100:9",
            ste_example=[
                "This is ste_example 1.",
                "This is ste_example 2.",
            ],
            nonste_example=[
                "This is nonste_example 1.",
                "This is nonste_example 2.",
            ],
        )

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )[0]

        self.assertIsNotNone(sut)

        self.assertEqual(2, len(sut.ste_example))
        self.assertEqual(expected.ste_example[0], sut.ste_example[0])
        self.assertEqual(expected.ste_example[1], sut.ste_example[1])

        self.assertEqual(2, len(sut.nonste_example))
        self.assertEqual(expected.nonste_example[0], sut.nonste_example[0])
        self.assertEqual(expected.nonste_example[1], sut.nonste_example[1])

    def test_meaning(self):

        word_list = VocabFile.COMPLETE
        fullname = Path(__file__).parent / word_list

        expected = Word(
            name="BE",
            status=WordStatus.APPROVED,
            type_=WordType.VERB,
            source="STE100:9",
            meanings=[
                WordMeaning(
                    value="1. To occur, exist",
                    ste_example="IF THERE IS CORROSION ON THE PUMP VANES, REPLACE THE PUMP.",
                ),
                WordMeaning(
                    value="2. To have a property, to be equal to",
                    ste_example="ACID SOLUTIONS ARE DANGEROUS.",
                ),
            ],
        )

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )[0]

        self.assertIsNotNone(sut)

        self.assertEqual(2, len(sut.meanings))
        self.assertEqual(expected.meanings[0].value, sut.meanings[0].value)
        self.assertEqual(
            expected.meanings[0].ste_example, sut.meanings[0].ste_example
        )
        self.assertEqual(
            expected.meanings[0].nonste_example, sut.meanings[0].nonste_example
        )

        self.assertEqual(expected.meanings[1].value, sut.meanings[1].value)
        self.assertEqual(
            expected.meanings[1].ste_example, sut.meanings[1].ste_example
        )
        self.assertEqual(
            expected.meanings[1].nonste_example, sut.meanings[1].nonste_example
        )

    def test_alternative(self):

        word_list = VocabFile.COMPLETE
        fullname = Path(__file__).parent / word_list

        expected = Word(
            name="BE",
            status=WordStatus.APPROVED,
            type_=WordType.VERB,
            source="STE100:9",
            alternatives=[
                Word(
                    name="ALT0",
                    ste_example=[
                        "ALT0.1: This is ste_example 1.",
                        "ALT0.2: This is ste_example 2.",
                    ],
                    nonste_example=[
                        "ALT0.1: This is nonste_example 1.",
                        "ALT0.2: This is nonste_example 2.",
                    ],
                ),
                Word(
                    name="ALT1",
                    ste_example=[
                        "ALT1.1: This is ste_example 1.",
                        "ALT1.2: This is ste_example 2.",
                    ],
                    nonste_example=[
                        "ALT1.1: This is nonste_example 1.",
                        "ALT1.2: This is nonste_example 2.",
                    ],
                ),
            ],
        )

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )[0]

        self.assertIsNotNone(sut)

        self.assertEqual(2, len(sut.alternatives))
        self.assertEqual(
            expected.alternatives[0].name, sut.alternatives[0].name
        )
        self.assertEqual(
            expected.alternatives[0].ste_example[0],
            sut.alternatives[0].ste_example[0],
        )
        self.assertEqual(
            expected.alternatives[0].ste_example[1],
            sut.alternatives[0].ste_example[1],
        )
        self.assertEqual(
            expected.alternatives[0].nonste_example[0],
            sut.alternatives[0].nonste_example[0],
        )
        self.assertEqual(
            expected.alternatives[0].nonste_example[1],
            sut.alternatives[0].nonste_example[1],
        )

        self.assertEqual(
            expected.alternatives[1].name, sut.alternatives[1].name
        )
        self.assertEqual(
            expected.alternatives[1].ste_example[0],
            sut.alternatives[1].ste_example[0],
        )
        self.assertEqual(
            expected.alternatives[1].ste_example[1],
            sut.alternatives[1].ste_example[1],
        )
        self.assertEqual(
            expected.alternatives[1].nonste_example[0],
            sut.alternatives[1].nonste_example[0],
        )
        self.assertEqual(
            expected.alternatives[1].nonste_example[1],
            sut.alternatives[1].nonste_example[1],
        )

    def test_spelling(self):

        word_list = VocabFile.COMPLETE
        fullname = Path(__file__).parent / word_list

        expected = Word(
            name="BE",
            status=WordStatus.APPROVED,
            type_=WordType.VERB,
            source="STE100:9",
            spellings=[
                "IS",
                "WAS",
                "(ARE)",
                "(WERE)"
            ],
        )

        sut = Vocab(
            files=[fullname],
            use_ste100=False,
            use_ste100_technical_word=False,
        )[0]

        self.assertIsNotNone(sut)

        self.assertEqual(4, len(sut.spellings))
        self.assertEqual(expected.spellings[0], sut.spellings[0])
        self.assertEqual(expected.spellings[1], sut.spellings[1])
        self.assertEqual(expected.spellings[2], sut.spellings[2])
        self.assertEqual(expected.spellings[3], sut.spellings[3])
