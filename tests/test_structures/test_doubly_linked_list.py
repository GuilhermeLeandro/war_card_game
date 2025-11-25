import unittest
from src.structures.doubly_linked_list import DoublyLinkedList, DoublyLinkedListNode

class TestDoublyLinkedList(unittest.TestCase):
    def setUp(self):
        self.dll = DoublyLinkedList()
# Testes da DoublyLinkedList

    def test_is_empty_initial(self):
        self.assertTrue(self.dll.is_empty())
        self.assertEqual(len(self.dll), 0)
        self.assertEqual(self.dll.get_all_entries(), [])

    def test_append(self):
        self.dll.append(10)
        self.assertFalse(self.dll.is_empty())
        self.assertEqual(len(self.dll), 1)
        self.assertEqual(self.dll.get_all_entries(), [10])
        self.dll.append(20)
        self.assertEqual(len(self.dll), 2)
        self.assertEqual(self.dll.get_all_entries(), [10, 20])

    def test_prepend(self):
        self.dll.prepend(30)
        self.assertEqual(self.dll.get_all_entries(), [30])
        self.dll.prepend(40)
        self.assertEqual(self.dll.get_all_entries(), [40, 30])

    def test_get_all_entries_reversed(self):
        self.dll.append(1)
        self.dll.append(2)
        self.dll.append(3)
        self.assertEqual(self.dll.get_all_entries(), [1, 2, 3])
        self.assertEqual(self.dll.get_all_entries_reversed(), [3, 2, 1])

    def test_iteration(self):
        values = [5, 6, 7]
        for v in values:
            self.dll.append(v)
        collected = [data for data in self.dll]
        self.assertEqual(collected, values)

    def test_str(self):
        self.dll.append("a")
        self.dll.append("b")
        self.assertEqual(str(self.dll), "a <-> b")

if __name__ == "__main__":
    unittest.main()
