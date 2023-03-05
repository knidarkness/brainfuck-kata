import unittest

from src.brainfuck import Brainfuck


class TestBrainfuck(unittest.TestCase):
    def test_init(self):
        self.assertNotEqual(Brainfuck(), None)

    def test_get_tape(self):
        brainfuck = Brainfuck()
        tape = brainfuck.get_tape()
        self.assertEqual(tape[0], 0)

    def test_get_pointer(self):
        brainfuck = Brainfuck()
        pointer = brainfuck.get_pointer()
        self.assertEqual(pointer, 0)

    def test_eval_plus(self):
        brainfuck = Brainfuck(5)
        brainfuck.eval_program('+')
        self.assertEqual(brainfuck.get_tape(), [1, 0, 0, 0, 0])

    def test_eval_minus(self):
        brainfuck = Brainfuck(5)
        brainfuck.eval_program('-')
        self.assertEqual(brainfuck.get_tape(), [255, 0, 0, 0, 0])

    def test_incr_pointer(self):
        brainfuck = Brainfuck(5)
        brainfuck.eval_program('>')
        self.assertEqual(brainfuck.get_pointer(), 1)

    def test_decr_pointer(self):
        brainfuck = Brainfuck(5)
        brainfuck.eval_program('<')
        self.assertEqual(brainfuck.get_pointer(), 4)

    def test_output_command(self):
        brainfuck = Brainfuck(5)
        brainfuck.eval_program('+' * 67)
        self.assertEqual(brainfuck._eval_output(), 'C')
        self.assertEqual(brainfuck._eval_output(), 'C')

    def test_detect_matching_loops(self):
        brainfuck = Brainfuck()
        brainfuck.set_program('++++[--++[+++++]]++')
        parser_output = brainfuck._parse_program()
        self.assertEqual(parser_output, {
            4: 16,
            9: 15,
            15: 9,
            16: 4,
        })

    def test_detect_matching_loops_throws_error_on_wrong_loop_syntax(self):
        brainfuck = Brainfuck()
        with self.assertRaises(SyntaxError):
            brainfuck.set_program('++++[--++[+++++]]++]')

    def test_jump_if_zero(self):
        brainfuck = Brainfuck(5)
        brainfuck.eval_program('+++++>+++++[-]')
        self.assertEqual(brainfuck.get_tape(), [5, 0, 0, 0, 0])

    def test_exits_hw(self):
        brainfuck = Brainfuck()
        brainfuck.eval_program(
            '>+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.>>>++++++++[<++++>-]<.>>>++++++++++['
            '<+++++++++>-]<---.<<<<.+++.------.--------.>>+.>++++++++++.')
        self.assertEqual(brainfuck.get_output(), 'Hello World!\n')
