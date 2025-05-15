from collections import deque

class Queue:
    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        """Adiciona um item ao final da fila."""
        self._items.append(item)

    def dequeue(self):
        """Remove e retorna o item do início da fila."""
        if not self.is_empty():
            return self._items.popleft()
        raise IndexError("dequeue from empty queue")

    def peek(self):
        """Retorna o item do início da fila sem removê-lo."""
        if not self.is_empty():
            return self._items[0]
        return None

    def is_empty(self):
        """Verifica se a fila está vazia."""
        return len(self._items) == 0

    def size(self):
        """Retorna o número de itens na fila."""
        return len(self._items)

    def __str__(self):
        return f"Queue({list(self._items)})"