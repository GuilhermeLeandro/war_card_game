# src/structures/queue.py

class Queue:
    def __init__(self):
        self._items = [] # Usará lista nativa do Python

    def enqueue(self, item):
        """Adiciona um item ao final da fila."""
        self._items.append(item)

    def append(self, item):
        """Adiciona um item ao final da fila (alias para enqueue)."""
        self.enqueue(item)

    def dequeue(self):
        """Remove e retorna o item do início da fila."""
        if not self.is_empty():
            return self._items.pop(0)
        raise IndexError("dequeue from empty queue")

    def popleft(self):
        """Remove e retorna o item do início da fila (alias para dequeue)."""
        return self.dequeue()

    def peek(self):
        """Retorna o item do início da fila sem removê-lo."""
        if not self.is_empty():
            return self._items[0]
        return None
    
    def is_empty(self):
        """Retorna True se a fila não contiver itens, False caso contrário."""
        return len(self._items) == 0

    def size(self):
        """Retorna o número de itens atualmente na fila."""
        return len(self._items)

    def __len__(self):
        """Retorna o número de itens atualmente na fila."""
        return self.size()

    def clear(self):
        """Remove todos os itens da fila."""
        self._items.clear()

    def __str__(self):
        # Mostra os itens na ordem em que seriam removidos (do início para o fim)
        return f"Queue({self._items})"