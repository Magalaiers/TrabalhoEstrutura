# src/data_structures/linked_list_optimized.py

class Node:
    """
    Um nó individual de uma lista encadeada.
    (Esta classe não muda, é exatamente a mesma de antes)
    """
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedListOptimized:
    """
    A estrutura da Lista Encadeada OTIMIZADA com um ponteiro para a cauda (tail).
    """
    def __init__(self):
        self.head = None
        self.tail = None  # <<< MUDANÇA 1: Adicionamos o ponteiro da cauda
        self.size = 0

    def __str__(self):
        # Este método não muda
        nodes = []
        current_node = self.head
        while current_node:
            nodes.append(str(current_node.data))
            current_node = current_node.next
        return " -> ".join(nodes)

    def insert(self, data):
        """
        <<< MUDANÇA 2: Lógica de inserção totalmente reescrita para ser O(1)
        """
        new_node = Node(data)
        self.size += 1

        # Caso 1: A lista está vazia
        if not self.head:
            self.head = new_node
            self.tail = new_node
            return

        # Caso 2: A lista já tem elementos
        # O antigo 'tail' agora aponta para o novo nó
        self.tail.next = new_node
        # O novo nó se torna o novo 'tail'
        self.tail = new_node

    def search(self, data_to_find):
        # A lógica de busca não muda
        current_node = self.head
        while current_node:
            if current_node.data == data_to_find:
                return True
            current_node = current_node.next
        return False

    def remove(self, data_to_remove):
        """
        <<< MUDANÇA 3: Pequeno ajuste na lógica de remoção para atualizar o 'tail'
        """
        if not self.head: # Se a lista estiver vazia, não há nada a fazer
            return False

        # Se o nó a ser removido for a cabeça
        if self.head.data == data_to_remove:
            self.head = self.head.next
            # Se a lista ficou vazia após a remoção, a cauda também é nula
            if not self.head:
                self.tail = None
            self.size -= 1
            return True

        # Percorre a lista para encontrar o nó a ser removido
        current_node = self.head
        while current_node.next and current_node.next.data != data_to_remove:
            current_node = current_node.next

        # Se o nó foi encontrado (current_node.next é o nó a ser removido)
        if current_node.next:
            node_to_remove = current_node.next
            # Se o nó a ser removido for a cauda, atualizamos a cauda
            if node_to_remove == self.tail:
                self.tail = current_node
            
            # Remove o nó fazendo o bypass
            current_node.next = node_to_remove.next
            self.size -= 1
            return True
        
        return False # Nó não encontrado