import unittest
from src.structures.queue import Queue

class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()

    def test_is_empty_initial(self):
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(len(self.queue), 0)
        self.assertEqual(self.queue.size(), 0)
        self.assertEqual(str(self.queue), "Queue([])")

    def test_enqueue_and_peek(self):
        self.queue.enqueue(1)
        self.assertFalse(self.queue.is_empty())
        self.assertEqual(self.queue.peek(), 1)
        self.assertEqual(len(self.queue), 1)

    def test_append_alias(self):
        self.queue.append(2)
        self.assertEqual(self.queue.peek(), 2)
        self.assertEqual(self.queue.size(), 1)

    def test_dequeue_and_popleft_alias(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.assertEqual(self.queue.dequeue(), 10)
        self.assertEqual(self.queue.popleft(), 20)
        self.assertTrue(self.queue.is_empty())
        with self.assertRaises(IndexError):
            self.queue.dequeue()  # dequeuing empty queue should raise

    def test_clear(self):
        self.queue.enqueue("a")
        self.queue.enqueue("b")
        self.queue.clear()
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(len(self.queue), 0)

if __name__ == "__main__":
    unittest.main()
