import optparse

from mydot import extractor


parser = optparse.OptionParser()
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


def main():
    options, args = parser.parse_args()
    if len(args) == 0:
        print("Please provide patterns.")
        exit(1)
    extractor.Extractor(options, args).extract()
