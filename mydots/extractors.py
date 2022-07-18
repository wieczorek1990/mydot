import json
import re
import sys
import typing


class Extractor:
    # .identifier | ["identifier.with.dots"] | [index_string] | anything
    SPLIT_REGEX = re.compile(
        r"\.(\w+)|\[\"([.\w]+)\"\]|\[\'([.\w]+)\'\]|\[(\d+)\]|(.+)"
    )

    def __init__(self, options: dict[str, typing.Any], args: list[str]) -> None:
        self.separator = options["separator"]
        self.raw_strings = options["raw_strings"]
        self.patterns = args
        self.data = self.load()

    def set_patterns(self, patterns: list[str]) -> None:
        self.patterns = patterns

    @staticmethod
    def load() -> dict[str, typing.Any]:
        return json.load(sys.stdin)

    def extract(self) -> list[typing.Optional[typing.Any]]:
        values = []
        string_values = []
        for value in self.extract_many():
            values.append(value)
            if value is not None:
                if self.raw_strings and isinstance(value, str):
                    string_value = value
                else:
                    string_value = json.dumps(value)
            else:
                string_value = ""
            string_values.append(string_value)
        print(*string_values, sep=self.separator)
        return values

    def extract_many(self) -> list[typing.Optional[typing.Any]]:
        return [self.extract_one(pattern) for pattern in self.patterns]

    def split(self, pattern: str) -> list[str]:
        return self.SPLIT_REGEX.findall(pattern)

    @staticmethod
    def get_dict_value(data: typing.Any, key: str) -> typing.Any:
        if not isinstance(data, dict):
            raise TypeError('Not a dict.')
        value = data[key]
        return value

    @staticmethod
    def get_list_value(data: typing.Any, index_string: str) -> typing.Any:
        if not isinstance(data, list):
            return None
        index = int(index_string)
        value = data[index]
        return value

    def extract_one(self, pattern: str) -> typing.Optional[typing.Any]:
        data = self.data.copy()
        value = data
        parts = self.split(pattern)
        try:
            for part in parts:
                if all([not group for group in part]):
                    return None
                elif key := part[0]:
                    value = self.get_dict_value(data, key)
                elif key := part[1]:
                    value = self.get_dict_value(data, key)
                elif key := part[2]:
                    value = self.get_dict_value(data, key)
                elif index_string := part[3]:
                    value = self.get_list_value(data, index_string)
                else:
                    return None
                data = value
        except (IndexError, KeyError, TypeError, ValueError):
            return None
        return value
