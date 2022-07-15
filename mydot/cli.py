import optparse

from mydot import extractor


parser = optparse.OptionParser()
parser.add_option(
    "-e", "--escape-strings", action="store_false", dest="raw_strings"
)
parser.add_option(
    "-r",
    "--raw_strings",
    action="store_true",
    dest="raw_strings",
    default=True,
)
parser.add_option(
    "-s", "--output-spaces", action="store_false", dest="output_newlines"
)
parser.add_option(
    "-n",
    "--output-newlines",
    action="store_true",
    dest="output_newlines",
    default=True,
)


def main():
    options, args = parser.parse_args()
    if len(args) == 0:
        print("Please provide patterns.")
        exit(1)
    extractor.Extractor(options, args).extract()
