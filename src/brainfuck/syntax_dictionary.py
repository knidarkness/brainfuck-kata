from enum import Enum


class BrainfuckSyntax(Enum):
    INCREMENT_CELL = '+'
    DECREMENT_CELL = '-'
    INCREMENT_TAPE_POINTER = '>'
    DECREMENT_TAPE_POINTER = '<'
    OUTPUT = '.'
    INPUT = ','
    START_LOOP = '['
    END_LOOP = ']'
