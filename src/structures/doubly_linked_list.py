# src/structures/doubly_linked_list.py
class DoublyLinkedListNode:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None
    def __str__(self): return str(self.data)

class DoublyLinkedList:
    def __init__(self):
        self.head = None; self.tail = None; self.count = 0
    def is_empty(self): return self.count == 0
    def append(self, data): # Adiciona ao final (mais recente)
        new_node = DoublyLinkedListNode(data)
        if self.is_empty(): self.head = new_node; self.tail = new_node
        else: new_node.prev = self.tail; self.tail.next = new_node; self.tail = new_node
        self.count += 1
    def prepend(self, data): # Adiciona ao início (mais antigo)
        new_node = DoublyLinkedListNode(data)
        if self.is_empty(): self.head = new_node; self.tail = new_node
        else: new_node.next = self.head; self.head.prev = new_node; self.head = new_node
        self.count += 1
    def get_all_entries(self): return [data for data in self] # Itera do head para o tail
    def get_all_entries_reversed(self): # Para mostrar mais recente primeiro
        entries = []; current = self.tail
        while current: entries.append(current.data); current = current.prev
        return entries
    def __iter__(self):
        current = self.head
        while current: yield current.data; current = current.next
    def __len__(self): return self.count
    def __str__(self): return " <-> ".join([str(node_data) for node_data in self])