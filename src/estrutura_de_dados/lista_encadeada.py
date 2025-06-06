# src/data_structures/linked_list.py

class Node:
    """
    Um nó individual de uma lista encadeada.
    Ele contém os dados e uma referência para o próximo nó na lista.
    """
    def __init__(self, data):
        self.data = data  # O dado que o nó armazena (pode ser qualquer coisa)
        self.next = None  # A referência para o próximo nó (inicialmente nula)


# Continue no mesmo arquivo: src/data_structures/linked_list.py

class LinkedList:
    """
    A estrutura da Lista Encadeada.
    Gerencia a coleção de nós.
    """
    def __init__(self):
        self.head = None  # O início da lista (inicialmente vazia, sem cabeça)
        self.size = 0     # (Opcional, mas útil) Mantém o controle do tamanho

    # Para facilitar a visualização da lista
    def __str__(self):
        nodes = []
        current_node = self.head
        while current_node:
            nodes.append(str(current_node.data))
            current_node = current_node.next
        return " -> ".join(nodes)
# Dentro da classe LinkedList

    def insert(self, data):
        """Insere um novo nó com os dados no final da lista."""
        new_node = Node(data)
        self.size += 1

        # Se a lista está vazia, o novo nó é a cabeça
        if not self.head:
            self.head = new_node
            return

        # Se não, percorre a lista até o último nó
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        
        # Faz o último nó apontar para o novo nó
        last_node.next = new_node
# Dentro da classe LinkedList

    def search(self, data_to_find):
        """Busca por um dado na lista. Retorna True se encontrar, False caso contrário."""
        current_node = self.head
        while current_node:
            if current_node.data == data_to_find:
                return True  # Encontrou!
            current_node = current_node.next
        return False  # Não encontrou após percorrer toda a lista
# Dentro da classe LinkedList

    def remove(self, data_to_remove):
        """Remove a primeira ocorrência de um nó com os dados especificados."""
        current_node = self.head
        previous_node = None

        # Percorre a lista procurando o dado
        while current_node and current_node.data != data_to_remove:
            previous_node = current_node
            current_node = current_node.next

        # Caso 1: O dado não foi encontrado
        if current_node is None:
            return False # Não encontrou, não removeu nada

        # Caso 2: O dado está na cabeça da lista (não há nó anterior)
        if previous_node is None:
            self.head = current_node.next
        else:
            # Caso 3: O dado está no meio ou no fim da lista
            previous_node.next = current_node.next
        
        self.size -= 1
        return True # Removeu com sucesso