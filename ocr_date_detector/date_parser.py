import re
from dateutil import parser


class DateParser:
    def __init__(self, month_mapping=None, debug=False):
        self.month_mapping = month_mapping
        self.date_parser_locale = self.__get_locale(month_mapping) if month_mapping else None
        self.debug = debug
        self.DATE_FORMAT_REGEX = [
            r"[0-9]+/[0-9]+/[0-9]+",  # Example: 11/02/1998
            r"[0-9]+-[a-zA-Z]{3}-[0-9]+",  # Example: 11-Feb-1998
            r"[0-9]+\.[0-9]+\.[0-9]+",  # Example: 11.02.1998
        ]

    def parse_date(self, input):
        try:
            parsed_date = parser.parse(input, parserinfo=self.date_parser_locale)
            return parsed_date
        except ValueError:
            print("Failed to detect the date format using default mechanism: {}".format(input))
            pass

        # Likely unknown date+time format - try to parse just the date
        parsed_date = self.__parse_date_fallback(input)
        if parsed_date:
            return parsed_date

    def __get_locale(self, month_mapping):
        class LocaleParserInfo(parser.parserinfo):
            MONTHS = month_mapping

        return LocaleParserInfo()

    def __parse_date_fallback(self, text):
        if not text or not text[0].isdigit():
            return
        known_date_part = None

        for regex in self.DATE_FORMAT_REGEX:
            res = re.search(regex, text)
            if res:
                known_date_part = res.group(0)
                break

        if not known_date_part:
            return None

        if self.debug:
            print("Found known date format using fallback detection: {}".format(known_date_part))
        try:
            return parser.parse(known_date_part, parserinfo=self.date_parser_locale)
        except ValueError:
            print("ERROR: Failed to translate the date format using fallback detection: {}".format(known_date_part))
            return None
