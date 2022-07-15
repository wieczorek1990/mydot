import json
import re
import sys
import typing


class Extractor:
    SPLIT_REGEX = re.compile(r"\.?(\w+)|\[(\d+)\]|.+")

    def __init__(self, options: dict[str, typing.Any], args: list[str]) -> None:
        options_dict = vars(options)
        self.separator = options_dict["separator"]
        self.raw_strings = options_dict["raw_strings"]
        self.patterns: list[str] = args
        self.post_init()

    def post_init(self) -> None:
        self.data = json.load(sys.stdin)

    def extract(self) -> None:
        self.extract_many()

    def extract_many(self) -> None:
        values = [self.extract_one(pattern) for pattern in self.patterns]
        filtered_values = [value for value in values if value is not None]
        values_string = self.separator.join(filtered_values)
        print(values_string)

    def split(self, pattern: str) -> list[str]:
        return self.SPLIT_REGEX.findall(pattern)

    def extract_one(self, pattern: str) -> typing.Optional[str]:
        data = self.data.copy()
        value = data
        try:
            parts = self.split(pattern)
            for part in parts:
                if all([not group for group in part]):
                    return None
                elif part[0]:
                    if not isinstance(data, dict):
                        return None
                    key = part[0]
                    value = data[key]
                elif part[1]:
                    if not isinstance(data, list):
                        return None
                    index_string = part[1]
                    index = int(index_string)
                    value = data[index]
                else:
                    return None
                data = value
        except (IndexError, KeyError, TypeError, ValueError):
            return None
        if self.raw_strings and isinstance(value, str):
            return value
        return json.dumps(value)
