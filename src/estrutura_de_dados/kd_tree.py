# src/data_structures/kd_tree.py
import sys

class KDNode:
    """Nó de uma KD-Tree. Armazena o ponto, eixo, filhos e um status de exclusão."""
    def __init__(self, point, axis, left=None, right=None):
        self.point = point
        self.axis = axis
        self.left = left
        self.right = right
        self.deleted = False # <-- MUDANÇA 1: Adiciona a flag de exclusão

class KDTree:
    """Implementação de uma KD-Tree com remoção preguiçosa (lazy deletion)."""
    def __init__(self, points):
        self.k = len(points[0]) if points else 0
        def build_kdtree(point_list, depth=0):
            if not point_list: return None
            axis = depth % self.k
            point_list.sort(key=lambda p: p[axis])
            median_idx = len(point_list) // 2
            node = KDNode(point=point_list[median_idx], axis=axis)
            node.left = build_kdtree(point_list[:median_idx], depth + 1)
            node.right = build_kdtree(point_list[median_idx + 1:], depth + 1)
            return node
        self.root = build_kdtree(list(points))

    # --- MUDANÇA 2: Adiciona um método de busca para encontrar um nó exato ---
    def search(self, point_to_find):
        """Busca por um nó com um ponto exato e o retorna."""
        def search_recursive(node, point, depth=0):
            if node is None: return None
            if node.point == point: return node
            
            axis = depth % self.k
            if point[axis] < node.point[axis]:
                return search_recursive(node.left, point, depth + 1)
            return search_recursive(node.right, point, depth + 1)
            
        return search_recursive(self.root, point_to_find)

    # --- MUDANÇA 3: Implementa a remoção "preguiçosa" ---
    def remove(self, point_to_remove):
        """Marca um nó como deletado, sem removê-lo fisicamente."""
        node_to_mark = self.search(point_to_remove)
        if node_to_mark and not node_to_mark.deleted:
            node_to_mark.deleted = True
            return True
        return False

    def find_nearest_neighbor(self, query_point):
        """Encontra o vizinho mais próximo, ignorando nós deletados."""
        def distance_sq(p1, p2):
            return sum([(c1 - c2) ** 2 for c1, c2 in zip(p1, p2)])

        def search_nn(node, best_dist_sq, best_point):
            if node is None:
                return best_dist_sq, best_point

            # --- MUDANÇA 4: Verifica se o nó não foi deletado ---
            if not node.deleted:
                dist_sq = distance_sq(query_point, node.point)
                if dist_sq < best_dist_sq:
                    best_dist_sq = dist_sq
                    best_point = node.point
            
            axis = node.axis
            diff = query_point[axis] - node.point[axis]
            close_branch, far_branch = (node.left, node.right) if diff < 0 else (node.right, node.left)
            
            best_dist_sq, best_point = search_nn(close_branch, best_dist_sq, best_point)
            
            if diff**2 < best_dist_sq:
                best_dist_sq, best_point = search_nn(far_branch, best_dist_sq, best_point)

            return best_dist_sq, best_point

        if self.root is None: return None
        _, nearest_point = search_nn(self.root, float('inf'), None)
        return nearest_point

    def get_memory_usage(self):
        # Este método não muda e continua correto.
        if self.root is None: return 0
        def get_memory_recursive(node):
            if node is None: return 0
            size = sys.getsizeof(node)
            size += get_memory_recursive(node.left)
            size += get_memory_recursive(node.right)
            return size
        return get_memory_recursive(self.root)