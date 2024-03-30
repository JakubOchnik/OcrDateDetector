from ocr_date_detector.filename_parser import parse_name_string, Token, TokenType, get_file_name


def expect_parser_output(input, expected):
    tokens = parse_name_string(input)
    assert tokens == expected


def test_token_parser():
    expect_parser_output(
        "abcd_{date}{name}", [Token(TokenType.TEXT, "abcd_"), Token(TokenType.DATE), Token(TokenType.FILE_NAME)]
    )
    expect_parser_output("abcd", [Token(TokenType.TEXT, "abcd")])
    expect_parser_output("{date}", [Token(TokenType.DATE)])


def expect_parser_error(input):
    tokens = parse_name_string(input)
    assert not tokens


def test_token_parser_errors():
    expect_parser_error("abcd_{{}")
    expect_parser_error("abcd_{}}")
    expect_parser_error("abcd_{}")
    expect_parser_error("abcd_{blahblah}")
    expect_parser_error("abcd_{ }")
    expect_parser_error("{")
    expect_parser_error("}")
    expect_parser_error("abcd{")
    expect_parser_error("abcd}")
    expect_parser_error("")


def test_get_file_name():
    assert (
        get_file_name("01-01-1991", "test", [Token(TokenType.TEXT, "abc"), Token(TokenType.DATE), Token(TokenType.FILE_NAME)])
        == "abc01-01-1991test"
    )
    assert get_file_name("01-01-1991", "test", []) == ""
