from datetime import datetime

from ocr_date_detector.date_parser import DateParser


def get_date(date, format="%d-%m-%Y"):
    return datetime.strptime(date, format)


def test_date_formats():
    parser = DateParser()
    assert parser.parse_date("25-12-2038") == get_date("25-12-2038")
    assert parser.parse_date("25-12-2038") == get_date("25-12-2038")
    assert parser.parse_date("25/12/2038") == get_date("25-12-2038")
    assert parser.parse_date("25.12.38") == get_date("25-12-2038")
    assert parser.parse_date("08.06.01") == get_date("06-08-2001")
    assert parser.parse_date("Jun 13 2001") == get_date("13-06-2001")
    assert parser.parse_date("13 Jun 2001") == get_date("13-06-2001")
    assert parser.parse_date("13 jun 2001") == get_date("13-06-2001")
    assert parser.parse_date("13 Jun 01") == get_date("13-06-2001")
    assert parser.parse_date("13-Jun-2001") == get_date("13-06-2001")
    assert parser.parse_date("13-Jun-01") == get_date("13-06-2001")
    assert parser.parse_date("13/Jun/2001") == get_date("13-06-2001")
    assert parser.parse_date("13/Jun/01") == get_date("13-06-2001")


def test_date_with_time_formats():
    parser = DateParser()
    # Supported time formats
    assert parser.parse_date("08.11.2009 11:02") == get_date("11-08-2009 11:02", "%d-%m-%Y %H:%M")
    assert parser.parse_date("08.11.2009 11:02:13") == get_date("11-08-2009 11:02:13", "%d-%m-%Y %H:%M:%S")
    assert parser.parse_date("08.11.2009 11:02:13.15") == get_date("11-08-2009 11:02:13.15", "%d-%m-%Y %H:%M:%S.%f")

    # Fallback date parsing - currently time detection not implemented
    # Mostly used for %H.%M
    assert parser.parse_date("08-nov-09 11.02") == get_date("08-11-2009")
    assert parser.parse_date("08.11.09 11.02") == get_date("11-08-2009")
    assert parser.parse_date("08.11.2009 11.02") == get_date("11-08-2009")
    assert parser.parse_date("13.11.09 11.02") == get_date("13-11-2009")
    assert parser.parse_date("13/11/09 11.02") == get_date("13-11-2009")
    assert parser.parse_date("13/11/2009 11.02") == get_date("13-11-2009")
    assert parser.parse_date("1/2/09 11.02") == get_date("02-01-2009")
    assert parser.parse_date("13/2/09 11.02") == get_date("13-02-2009")


def test_month_mapping():
    month_mapping = [
        ("sty",),
        ("lut",),
        ("mar",),
        ("kwi",),
        ("maj",),
        ("cze",),
        ("lip",),
        ("sie",),
        ("wrz",),
        ("paź",),
        ("lis",),
        ("gru",),
    ]
    parser = DateParser(month_mapping)
    assert parser.parse_date("paź 13 2001") == get_date("13-10-2001")
    assert parser.parse_date("13 Paź 2001") == get_date("13-10-2001")
    assert parser.parse_date("13 paź 01") == get_date("13-10-2001")
    assert parser.parse_date("13-Paź-2001") == get_date("13-10-2001")
    assert parser.parse_date("13-paź-01") == get_date("13-10-2001")
    assert parser.parse_date("13/paź/2001") == get_date("13-10-2001")
    assert parser.parse_date("13/Paź/01") == get_date("13-10-2001")

    assert parser.parse_date("13-oct-01") != get_date("13-10-2001")

    assert parser.parse_date("08-lis-09 11:02") == get_date("08-11-2009 11:02", "%d-%m-%Y %H:%M")
    # TODO: handle non-ASCII characters in regex fallback
    # assert parser.parse_date("08-paź-09 11:02") == get_date("08-10-2009 11:02")


def test_month_mapping_multi():
    month_mapping = [
        ("Jan", "sty"),
        ("Feb", "lut"),
        ("Mar", "mar"),
        ("Apr", "kwi"),
        ("May", "maj"),
        ("Jun", "cze"),
        ("Jul", "lip"),
        ("Aug", "sie"),
        ("Sep", "wrz"),
        ("Oct", "paź"),
        ("Nov", "lis"),
        ("Dec", "gru"),
    ]
    parser = DateParser(month_mapping)
    assert parser.parse_date("13-paź-01") == get_date("13-10-2001")
    assert parser.parse_date("13-oct-01") == get_date("13-10-2001")
    assert parser.parse_date("08-lis-09 11:02") == get_date("08-11-2009 11:02", "%d-%m-%Y %H:%M")
    assert parser.parse_date("08-nov-09 11:02") == get_date("08-11-2009 11:02", "%d-%m-%Y %H:%M")
