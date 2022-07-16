import optparse
import typing

from mydots import extractors


class OptionParser(optparse.OptionParser):
    def parse_args_and_values(
        self, args=None, values=None
    ) -> tuple[dict[str, typing.Any], list[str]]:
        options, args = super().parse_args(args=args, values=values)
        return vars(options), args


parser = OptionParser()
parser.add_option(
    "-s",
    "--separator",
    action="store",
    dest="separator",
    default="\n",
)
parser.add_option(
    "-e",
    "--escape-strings",
    action="store_false",
    dest="raw_strings",
    default=True,
)


def main() -> None:
    options, args = parser.parse_args_and_values()
    if len(args) == 0:
        print("Please provide patterns.")
        exit(1)
    extractor = extractors.Extractor(options, args)
    extractor.extract()
