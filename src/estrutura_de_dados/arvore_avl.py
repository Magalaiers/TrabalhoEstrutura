# src/data_structures/avl_tree.py

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
        """
        Realiza uma rotação para a direita na subárvore com raiz z.
              z                                      y
             / \                                    / \
            y   T4      -- Rotação Direita -->     x   z
           / \                                    / \ / \
          x   T3                                 T1 T2 T3 T4
         / \
        T1  T2
        """
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
        """
        Realiza uma rotação para a esquerda na subárvore com raiz z.
            z                                y
           / \                              / \
          T1  y      -- Rotação Esquerda --> z  x
             / \                          / \ / \
            T2  x                        T1 T2 T3 T4
               / \
              T3 T4
        """
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

    def _insert_recursive(self, root, key):
        # 1. Realiza a inserção padrão de uma Árvore de Busca Binária
        if not root:
            return AVLNode(key)
        elif key < root.key:
            root.left = self._insert_recursive(root.left, key)
        else:
            root.right = self._insert_recursive(root.right, key)

        # 2. Atualiza a altura do nó ancestral
        self._update_height(root)

        # 3. Calcula o fator de balanceamento para ver se o nó ficou desbalanceado
        balance = self._get_balance(root)

        # 4. Se o nó ficou desbalanceado, existem 4 casos:

        # Caso 1: Rotação Simples à Direita (Esquerda-Esquerda)
        if balance > 1 and key < root.left.key:
            return self._right_rotate(root)

        # Caso 2: Rotação Simples à Esquerda (Direita-Direita)
        if balance < -1 and key > root.right.key:
            return self._left_rotate(root)

        # Caso 3: Rotação Dupla à Direita (Esquerda-Direita)
        if balance > 1 and key > root.left.key:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)

        # Caso 4: Rotação Dupla à Esquerda (Direita-Esquerda)
        if balance < -1 and key < root.right.key:
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