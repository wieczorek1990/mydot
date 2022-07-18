import io
import sys
import unittest

from mydots import extractors
from mydots import results


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
        self.empty = results.Empty()
        self.string = "I am alive!"
        self.test_cases = [
            # invalid
            ("invalid", self.empty),
            ("['null\"]", self.empty),
            ('[\"null\']', self.empty),
            # valid
            ("['null']", None),
            ('["null"]', None),
            (".null", None),
            (".boolean_true", True),
            (".boolean_false", False),
            (".string", self.string),
            (".integer", 1),
            (".floating", 1.0),
            (".list_empty", []),
            (".list_bool", [True, False]),
            (".list_bool[0]", True),
            (".list_strings", ["one", "two"]),
            (".list_integers", [0, 1]),
            (".list_floating", [0.0, 1.0]),
            (".list_list", [[0, 1]]),
            (".list_list[0][0]", 0),
            (".list_object", [{"string": self.string}]),
            (".object", {"string": self.string, "list_integers": [0, 1]}),
            (".object.string", self.string),
            ('["list_bool"]', [True, False]),
            ('["identifier.with.dots"]', True),
            ("['identifier.with.dots']", True),
        ]
        self.args = [test_case[0] for test_case in self.test_cases]
        self.expected = [test_case[1] for test_case in self.test_cases]

        self.paste()

    def tearDown(self) -> None:
        sys.stdin = sys.__stdin__

        super().tearDown()

    @staticmethod
    def paste():
        with open("tests/sample.json") as file_descriptor:
            content = file_descriptor.read()
            sys.stdin = io.StringIO(content)

    def test_extractor(self) -> None:
        extractor = extractors.Extractor(self.options, self.args)
        extracted = extractor.extract()
        self.assertEqual(extracted, self.expected)

    def test_extractor_copy(self):
        extractor = extractors.Extractor(self.options, [''])
        extracted = extractor.extract()
        first_extracted = extracted[0]
        extractor_data = extractor.data
        self.assertEqual(first_extracted, extractor_data)
