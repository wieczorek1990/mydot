import io
import sys
import unittest

from mydots import extractors


class QuietTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        sys.stdout = io.StringIO()

    def tearDown(self) -> None:
        sys.stdout = sys.__stdout__

        super().tearDown()


class FullDiffTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.maxDiff = None


class ExtractorsTestCase(FullDiffTestCase, QuietTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.options = {"separator": "\n", "raw_strings": True}
        self.args = [
            "",
            "invalid",
            ".null",
            ".boolean_true",
            ".boolean_false",
            ".string",
            ".integer",
            ".floating",
            ".list_empty",
            ".list_bool",
            ".list_strings",
            ".list_integers",
            ".list_floating",
            ".list_list",
            ".list_object",
            ".object",
            '["list_bool"]',
            ".list_bool[0]",
            ".object.string",
            ".list_list[0][0]",
        ]

        with open("tests/sample.json") as file_descriptor:
            content = file_descriptor.read()
            sys.stdin = io.StringIO(content)

    def tearDown(self) -> None:
        sys.stdin = sys.__stdin__

        super().tearDown()

    def test_extractor(self) -> None:
        extractor = extractors.Extractor(self.options, self.args)
        extracted = extractor.extract()
        expected = [
            extractor.data,
            None,
            None,
            True,
            False,
            "I am alive!",
            1,
            1.0,
            [],
            [True, False],
            ["one", "two"],
            [0, 1],
            [0.0, 1.0],
            [[0, 1]],
            [{"string": "I am alive!"}],
            {"string": "I am alive!", "list_integers": [0, 1]},
            [True, False],
            True,
            "I am alive!",
            0,
        ]
        self.assertEqual(extracted, expected)
