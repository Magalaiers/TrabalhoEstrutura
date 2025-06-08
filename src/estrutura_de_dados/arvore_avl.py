# src/data_structures/avl_tree.py
import sys

class AVLNode:
    """Nó de uma Árvore AVL. Contém a chave, referências para os filhos e a altura."""
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1 # A altura de um novo nó (folha) é sempre 1

class AVLTree:
    """A estrutura da Árvore AVL. Gerencia os nós e as operações de balanceamento."""

    def __init__(self):
        self.root = None

    # --- Funções Auxiliares ---

    def _get_height(self, node):
        """Retorna a altura de um nó (0 se o nó for nulo)."""
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        """Calcula o fator de balanceamento de um nó."""
        if not node:
            return 0
        # Fator de Balanceamento = Altura da Subárvore Esquerda - Altura da Subárvore Direita
        return self._get_height(node.left) - self._get_height(node.right)

    def _update_height(self, node):
        """Atualiza a altura de um nó com base na altura de seus filhos."""
        if node:
            node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
# Dentro da classe AVLTree

    def _right_rotate(self, z):
        y = z.left
        T3 = y.right

        # Realiza a rotação
        y.right = z
        z.left = T3

        # Atualiza as alturas (a ordem é importante)
        self._update_height(z)
        self._update_height(y)

        # Retorna a nova raiz da subárvore
        return y

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left

        # Realiza a rotação
        y.left = z
        z.right = T2

        # Atualiza as alturas
        self._update_height(z)
        self._update_height(y)

        # Retorna a nova raiz
        return y
    
# Dentro da classe AVLTree

    def insert(self, key):
        """Função pública para inserir uma chave na árvore."""
        self.root = self._insert_recursive(self.root, key)

# Em src/estrutura_de_dados/arvore_avl.py, dentro da classe AVLTree

    def _insert_recursive(self, root, key):
        # 1. Realiza a inserção padrão de uma Árvore de Busca Binária
        if not root:
            return AVLNode(key)
        elif key < root.key:
            root.left = self._insert_recursive(root.left, key)
        # Lida com chaves duplicadas, inserindo à direita
        # (uma árvore AVL geralmente não tem chaves duplicadas, mas esta é uma forma de lidar com isso)
        else:
            root.right = self._insert_recursive(root.right, key)

        # 2. Atualiza a altura do nó ancestral
        self._update_height(root)

        # 3. Calcula o fator de balanceamento para ver se o nó ficou desbalanceado
        balance = self._get_balance(root)

        # 4. Se o nó ficou desbalanceado, existem 4 casos (AGORA USANDO A LÓGICA CORRETA)

        # Caso Esquerda-Esquerda (Rotação Simples à Direita)
        if balance > 1 and self._get_balance(root.left) >= 0:
            return self._right_rotate(root)

        # Caso Direita-Direita (Rotação Simples à Esquerda)
        if balance < -1 and self._get_balance(root.right) <= 0:
            return self._left_rotate(root)

        # Caso Esquerda-Direita (Rotação Dupla à Direita)
        if balance > 1 and self._get_balance(root.left) < 0:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)

        # Caso Direita-Esquerda (Rotação Dupla à Esquerda)
        if balance < -1 and self._get_balance(root.right) > 0:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)

        # Retorna a raiz (potencialmente nova após rotações)
        return root
# Dentro da classe AVLTree

    def search(self, key):
        """Função pública para buscar uma chave na árvore."""
        return self._search_recursive(self.root, key)

    def _search_recursive(self, root, key):
        if not root or root.key == key:
            return root is not None # Retorna True se encontrou, False se a árvore acabou

        if key < root.key:
            return self._search_recursive(root.left, key)
        
        return self._search_recursive(root.right, key)
    
# Dentro da classe AVLTree

    def _get_min_value_node(self, root):
        """Encontra o nó com o menor valor em uma subárvore (o mais à esquerda)."""
        if root is None or root.left is None:
            return root
        return self._get_min_value_node(root.left)
    
# Dentro da classe AVLTree

    def remove(self, key):
        """Função pública para remover uma chave da árvore."""
        self.root = self._remove_recursive(self.root, key)

    def _remove_recursive(self, root, key):
        # 1. Realiza a remoção padrão de BST
        if not root:
            return root

        if key < root.key:
            root.left = self._remove_recursive(root.left, key)
        elif key > root.key:
            root.right = self._remove_recursive(root.right, key)
        else:
            # O nó a ser deletado foi encontrado!
            # Caso 1 ou 2: Nó com um filho ou sem filhos
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp

            # Caso 3: Nó com dois filhos
            # Pega o sucessor in-order (menor na subárvore direita)
            temp = self._get_min_value_node(root.right)
            root.key = temp.key # Copia a chave do sucessor para este nó
            # Deleta o sucessor
            root.right = self._remove_recursive(root.right, temp.key)

        # Se a árvore ficou vazia (só tinha um nó)
        if root is None:
            return root

        # 2. Atualiza a altura do nó atual
        self._update_height(root)

        # 3. Calcula o fator de balanceamento
        balance = self._get_balance(root)

        # 4. Se o nó ficou desbalanceado, aplica as rotações (4 casos)

        # Caso Esquerda-Esquerda
        if balance > 1 and self._get_balance(root.left) >= 0:
            return self._right_rotate(root)

        # Caso Direita-Direita
        if balance < -1 and self._get_balance(root.right) <= 0:
            return self._left_rotate(root)

        # Caso Esquerda-Direita
        if balance > 1 and self._get_balance(root.left) < 0:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)

        # Caso Direita-Esquerda
        if balance < -1 and self._get_balance(root.right) > 0:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)

        return root
    
# Dentro da classe AVLTree
# Dentro da classe AVLTree
    
    def get_memory_usage(self):
        """Função pública para obter o uso de memória estimado da árvore."""
        if not self.root:
            return 0
        return self._get_memory_recursive(self.root)

    def _get_memory_recursive(self, node):
        """Soma recursivamente o tamanho de cada nó na árvore."""
        if not node:
            return 0
        
        # Tamanho do nó atual + tamanho da subárvore esquerda + tamanho da subárvore direita
        size = sys.getsizeof(node)
        size += self._get_memory_recursive(node.left)
        size += self._get_memory_recursive(node.right)
        return size