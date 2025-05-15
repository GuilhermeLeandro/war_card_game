class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        """Adiciona um item ao topo da pilha."""
        self._items.append(item)

    def pop(self):
        """Remove e retorna o item do topo da pilha."""
        if not self.is_empty():
            return self._items.pop()
        raise IndexError("pop from empty stack")

    def peek(self):
        """Retorna o item do topo da pilha sem removê-lo."""
        if not self.is_empty():
            return self._items[-1]
        return None

    def is_empty(self):
        """Verifica se a pilha está vazia."""
        return len(self._items) == 0

    def size(self):
        """Retorna o número de itens na pilha."""
        return len(self._items)

    def __str__(self):
        return f"Stack({self._items})"