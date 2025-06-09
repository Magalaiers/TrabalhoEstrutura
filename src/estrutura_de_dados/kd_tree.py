# src/data_structures/kd_tree.py
import sys

class KDNode:
    """Nó de uma KD-Tree. Armazena o ponto e as referências aos filhos."""
    def __init__(self, point, axis, left=None, right=None):
        self.point = point
        self.axis = axis
        self.left = left
        self.right = right

class KDTree:
    """Implementação de uma KD-Tree balanceada para buscas espaciais."""
    def __init__(self, points):
        # A árvore é construída de uma vez para garantir o balanceamento
        k = len(points[0]) # Dimensão dos pontos (ex: 2 para 2D)
        
        def build_kdtree(point_list, depth=0):
            if not point_list:
                return None
            
            axis = depth % k
            # Ordena os pontos pela dimensão atual e escolhe a mediana
            point_list.sort(key=lambda p: p[axis])
            median_idx = len(point_list) // 2
            
            node = KDNode(point=point_list[median_idx], axis=axis)
            node.left = build_kdtree(point_list[:median_idx], depth + 1)
            node.right = build_kdtree(point_list[median_idx + 1:], depth + 1)
            
            return node
            
        self.root = build_kdtree(list(points))

    def find_nearest_neighbor(self, query_point):
        """Encontra o vizinho mais próximo de um ponto de consulta."""
        k = len(query_point)
        
        def distance_sq(p1, p2):
            return sum([(c1 - c2) ** 2 for c1, c2 in zip(p1, p2)])

        def search_nn(node, best_dist_sq, best_point):
            if node is None:
                return best_dist_sq, best_point

            dist_sq = distance_sq(query_point, node.point)
            if dist_sq < best_dist_sq:
                best_dist_sq = dist_sq
                best_point = node.point
            
            axis = node.axis
            diff = query_point[axis] - node.point[axis]

            # Explora a subárvore mais provável primeiro
            close_branch, far_branch = (node.left, node.right) if diff < 0 else (node.right, node.left)
            
            best_dist_sq, best_point = search_nn(close_branch, best_dist_sq, best_point)
            
            # Verifica se a outra subárvore pode conter um ponto mais próximo
            if diff**2 < best_dist_sq:
                best_dist_sq, best_point = search_nn(far_branch, best_dist_sq, best_point)

            return best_dist_sq, best_point

        if self.root is None:
            return None
            
        # Começa a busca com a raiz como o melhor ponto inicial
        _, nearest_point = search_nn(self.root, float('inf'), None)
        return nearest_point
# Em src/data_structures/kd_tree.py

# ... (dentro da classe KDTree) ...

    def get_memory_usage(self):
        """Função pública para obter o uso de memória estimado da árvore."""
        if self.root is None:
            return 0
        return self._get_memory_recursive(self.root)

    def _get_memory_recursive(self, node):
        """Soma recursivamente o tamanho de cada nó na árvore."""
        if node is None:
            return 0
        
        # Tamanho do nó atual + tamanho da subárvore esquerda + tamanho da subárvore direita
        size = sys.getsizeof(node)
        size += self._get_memory_recursive(node.left)
        size += self._get_memory_recursive(node.right)
        return size