from enum import Enum


class TokenType(Enum):
    TEXT = 1
    DATE = 2
    FILE_NAME = 3


class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.type == other.type and self.value == other.value
        return False


def __iter_starting_at(start_pos, string):
    for i in range(start_pos, len(string)):
        yield string[i]


def __parse_placeholder(iterator):
    placeholder_name = ""
    for placeholder_char in iterator:
        if placeholder_char == "}":
            break
        elif placeholder_char == "{":
            print("ERROR: '{' unexpected placeholder opening token")
            return None
        placeholder_name += placeholder_char

    if not placeholder_name:
        # error
        print("ERROR: Placeholder name is empty")
        return None
    elif placeholder_name.lower() == "date":
        return Token(TokenType.DATE)
    elif placeholder_name.lower() == "name":
        return Token(TokenType.FILE_NAME)


def parse_name_string(name_pattern):
    tokens = []
    string_iterator = __iter_starting_at(0, name_pattern)
    text_value = ""
    for char in string_iterator:
        if char == "}":
            print("ERROR: '}' unexpected placeholder closing token")
            return None
        elif char != "{":
            text_value += char
            continue
        if text_value:
            tokens.append(Token(TokenType.TEXT, text_value))
            text_value = ""
        placeholder = __parse_placeholder(string_iterator)
        if placeholder:
            tokens.append(placeholder)
        else:
            return None
    if text_value:
        tokens.append(Token(TokenType.TEXT, text_value))
    return tokens


def get_file_name(date, file_name, tokens):
    output_file_name = ""
    for token in tokens:
        if token.type == TokenType.TEXT:
            output_file_name += token.value
        elif token.type == TokenType.DATE:
            output_file_name += date
        elif token.type == TokenType.FILE_NAME:
            output_file_name += file_name

    return output_file_name
