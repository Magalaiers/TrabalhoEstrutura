import pandas as pd
import argparse
import json
import sys

# KD-Tree Node class
class KDNode:
    def __init__(self, point, data=None, left=None, right=None, axis=0):
        self.point = point
        self.data = data
        self.left = left
        self.right = right
        self.axis = axis

# KD-Tree class with insert, search, and remove
class KDTree:
    def __init__(self, k):
        self.k = k
        self.root = None

    def insert(self, point, data=None):
        def _insert(node, point, data, depth):
            if node is None:
                return KDNode(point, data, axis=depth % self.k)
            cd = node.axis
            if point[cd] < node.point[cd]:
                node.left = _insert(node.left, point, data, depth+1)
            else:
                node.right = _insert(node.right, point, data, depth+1)
            return node
        self.root = _insert(self.root, point, data, 0)

    def search(self, point):
        def _search(node, point):
            if node is None:
                return None
            if node.point == point:
                return node
            cd = node.axis
            if point[cd] < node.point[cd]:
                return _search(node.left, point)
            return _search(node.right, point)
        return _search(self.root, point)

    def find_min(self, node, d, depth):
        if node is None:
            return None
        cd = node.axis
        if cd == d:
            if node.left is None:
                return node
            return self.find_min(node.left, d, depth+1)
        left_min = self.find_min(node.left, d, depth+1)
        right_min = self.find_min(node.right, d, depth+1)
        candidates = [n for n in (node, left_min, right_min) if n]
        return min(candidates, key=lambda n: n.point[d])

    def remove(self, point):
        def _remove(node, point, depth):
            if node is None:
                return None
            cd = node.axis
            if node.point == point:
                if node.right:
                    min_node = self.find_min(node.right, cd, depth+1)
                    node.point, node.data = min_node.point, min_node.data
                    node.right = _remove(node.right, min_node.point, depth+1)
                elif node.left:
                    min_node = self.find_min(node.left, cd, depth+1)
                    node.point, node.data = min_node.point, min_node.data
                    node.left = _remove(node.left, min_node.point, depth+1)
                else:
                    return None
                return node
            if point[cd] < node.point[cd]:
                node.left = _remove(node.left, point, depth+1)
            else:
                node.right = _remove(node.right, point, depth+1)
            return node
        self.root = _remove(self.root, point, 0)

# Load dataset and build tree
def build_tree(csv_path, feature_cols):
    df = pd.read_csv(csv_path)
    # Convert non-numeric columns to numeric codes
    for col in feature_cols:
        if df[col].dtype == 'object':
            df[col] = pd.factorize(df[col])[0]
    data_points = df[feature_cols].values
    tree = KDTree(len(feature_cols))
    for row, point in zip(df.to_dict(orient="records"), data_points):
        tree.insert(tuple(point), data=row)
    return tree

if __name__ == "__main__":
    # Use only numeric-compatible features
    feature_cols = [
        "Age", "Cholesterol", "Heart Rate", "Diabetes", "Family History", 
        "Smoking", "Obesity", "Alcohol Consumption", "Exercise Hours Per Week",
        "Previous Heart Problems", "Medication Use", "Stress Level", 
        "Sedentary Hours Per Day", "Income", "BMI", "Triglycerides",
        "Physical Activity Days Per Week", "Sleep Hours Per Day", "Heart Attack Risk"
    ]
    
    parser = argparse.ArgumentParser(description="KD-Tree operations for heart dataset")
    parser.add_argument("--csv", default="heart_attack_prediction_dataset.csv", help="Caminho para o CSV")
    sub = parser.add_subparsers(dest="command")  # comandos: inserir, remover, buscar

    sub.add_parser("inserir", help="Inserir um ou mais registros.")
    sub.add_parser("remover", help="Remover um ou mais registros.")
    sub.add_parser("buscar", help="Buscar um ou mais registros (exibe o registro completo se encontrado).")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    tree = build_tree(args.csv, feature_cols)

    print("Digite registros JSON, um por linha. Pressione Enter em linha vazia para finalizar.")
    records = []
    while True:
        try:
            line = input()
            if not line.strip():
                break
            rec = json.loads(line)
            records.append(rec)
        except EOFError:
            break
        except json.JSONDecodeError:
            print("JSON inválido, tente novamente.")

    for record in records:
        # Convert non-numeric fields in input
        point_data = []
        for col in feature_cols:
            val = record.get(col)
            if isinstance(val, str):
                # Simple categorical encoding for input
                point_data.append(hash(val) % 1000000)  # Simple hash for demo
            else:
                point_data.append(val)
        point = tuple(point_data)
        
        if args.command == "inserir":
            tree.insert(point, data=record)
            print("Inserido:", record)
        elif args.command == "remover":
            tree.remove(point)
            print("Removido:", record)
        elif args.command == "buscar":
            node = tree.search(point)
            if node:
                print("Encontrado:", node.data)
            else:
                print("Não encontrado:", record)