import unittest
from src.structures.stack import Stack
# Testes unitários para a classe Stack

class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()

    def test_initial_state(self):
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)
        self.assertIsNone(self.stack.peek())
        self.assertEqual(str(self.stack), "Stack([])")

    def test_push_and_peek(self):
        self.stack.push(5)
        self.assertFalse(self.stack.is_empty())
        self.assertEqual(self.stack.peek(), 5)
        self.assertEqual(self.stack.size(), 1)

    def test_pop(self):
        self.stack.push('a')
        self.stack.push('b')
        self.assertEqual(self.stack.pop(), 'b')
        self.assertEqual(self.stack.pop(), 'a')
        self.assertTrue(self.stack.is_empty())
        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_size(self):
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(3)
        self.assertEqual(self.stack.size(), 3)

if __name__ == "__main__":
    unittest.main()
