from syntax_dictionary import BrainfuckSyntax


class Brainfuck:
    def __init__(self, tape_size=30_000):
        self.__output = None
        self.__program = None
        self.__jump_locations = None
        self.__command_pointer = None
        self.__tape_pointer = None
        self.__arr = None
        self.__tape_size = tape_size
        self.init_with_program()

    def init_with_program(self, program: str | None = None):
        self.__arr = [0] * self.__tape_size
        self.__tape_pointer = 0
        self.__command_pointer = 0
        self.__jump_locations = {}
        self.__output = ''
        self.__program = program or ''
        if self.__program is not None:
            self._parse_program()

    def get_tape(self):
        return self.__arr

    def get_pointer(self):
        return self.__tape_pointer

    def eval_program(self, program: str | None):
        self.__command_pointer = -1
        if program is not None:
            self.__program = program
            self._parse_program()
        while True:
            self.__command_pointer += 1
            self.__handle_token(program[self.__command_pointer])
            if self.__command_pointer == len(self.__program) - 1:
                break
        return self.__tape_pointer, self.__arr

    def _eval_output(self):
        symbol = chr(self.__arr[self.__tape_pointer])
        self.__output += symbol
        return symbol

    def get_output(self):
        return self.__output

    def __get_current_value(self):
        return self.__arr[self.__tape_pointer]

    def __set_current_value(self, val):
        self.__arr[self.__tape_pointer] = val

    def __handle_token(self, token):
        match token:
            case BrainfuckSyntax.INCREMENT_CELL.value:
                if self.__get_current_value() != 255:
                    self.__set_current_value(self.__get_current_value() + 1)
                else:
                    self.__set_current_value(0)
            case BrainfuckSyntax.DECREMENT_CELL.value:
                if self.__get_current_value() != 0:
                    self.__set_current_value(self.__get_current_value() - 1)
                else:
                    self.__set_current_value(255)
            case BrainfuckSyntax.INCREMENT_TAPE_POINTER.value:
                if self.__tape_pointer == len(self.__arr) - 1:
                    self.__tape_pointer = 0
                else:
                    self.__tape_pointer += 1
            case BrainfuckSyntax.DECREMENT_TAPE_POINTER.value:
                if self.__tape_pointer == 0:
                    self.__tape_pointer = len(self.__arr) - 1
                else:
                    self.__tape_pointer -= 1
            case BrainfuckSyntax.OUTPUT.value:
                self._eval_output()
            case BrainfuckSyntax.INPUT.value:
                self.__set_current_value(ord(input()[0]))
            case BrainfuckSyntax.START_LOOP.value:
                if self.__get_current_value() != 0:
                    return
                self.__command_pointer = self.__jump_locations[self.__command_pointer]
            case BrainfuckSyntax.END_LOOP.value:
                if self.__get_current_value() == 0:
                    return
                self.__command_pointer = self.__jump_locations[self.__command_pointer]
            case _:
                raise NotImplemented('Unknown token: ' + token)

    def _parse_program(self):
        loops = {}
        loops_stack = []
        for index, command in enumerate(self.__program):
            if command == '[':
                loops_stack.append(index)
            if command == ']':
                if len(loops_stack) == 0:
                    raise SyntaxError(
                        f'Trying to close the loop with "]" at position: {index} without matching opening symbol "["')
                opened_at = loops_stack.pop()
                loops[opened_at] = index
                loops[index] = opened_at
        self.__jump_locations = loops
        return loops
