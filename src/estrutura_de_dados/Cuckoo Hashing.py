import pandas as pd
import argparse
import json
import sys

class CuckooHashTable:
    def __init__(self, capacity=101, max_kicks=500):
        self.capacity = capacity
        self.max_kicks = max_kicks
        self.table = [None] * self.capacity

    def _hash1(self, key):
        return hash(key) % self.capacity

    def _hash2(self, key):
        return (hash(key) * 7 + 13) % self.capacity

    def _find_slot(self, key):
        i1 = self._hash1(key)
        if self.table[i1] and self.table[i1][0] == key:
            return i1
        i2 = self._hash2(key)
        if self.table[i2] and self.table[i2][0] == key:
            return i2
        return None

    def insert(self, key, data):
        if self._find_slot(key) is not None:
            return False  # Duplicado
        pos = self._hash1(key)
        for kick in range(self.max_kicks):
            if self.table[pos] is None:
                self.table[pos] = (key, data)
                return True
            # Realoca o item existente
            evicted_key, evicted_data = self.table[pos]
            self.table[pos] = (key, data)
            key, data = evicted_key, evicted_data
            # Alterna entre as funções de hash
            pos = self._hash2(key) if pos == self._hash1(key) else self._hash1(key)
        self._rehash()
        return self.insert(key, data)

    def remove(self, key):
        slot = self._find_slot(key)
        if slot is not None:
            self.table[slot] = None
            return True
        return False

    def search(self, key):
        slot = self._find_slot(key)
        if slot is not None:
            return self.table[slot][1]
        return None

    def _rehash(self):
        old_items = [(k, d) for slot in self.table if slot is not None for k, d in [slot]]
        self.capacity = self.capacity * 2 + 1
        self.table = [None] * self.capacity
        for k, d in old_items:
            self.insert(k, d)


def build_table(csv_path, feature_cols):
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"\nErro: Arquivo '{csv_path}' não encontrado!")
        sys.exit(1)
    
    initial_capacity = max(101, len(df) * 2 + 1)
    cuckoo = CuckooHashTable(capacity=initial_capacity)
    
    for row in df.to_dict(orient='records'):
        key = tuple(str(row[col]) for col in feature_cols)
        key_str = json.dumps(key, sort_keys=True)
        cuckoo.insert(key_str, row)
    
    return cuckoo

def main():
    feature_cols = [
        "Patient ID", "Age", "Sex", "Cholesterol", "Blood Pressure", "Heart Rate",
        "Diabetes", "Family History", "Smoking", "Obesity", "Alcohol Consumption",
        "Exercise Hours Per Week", "Diet", "Previous Heart Problems", "Medication Use",
        "Stress Level", "Sedentary Hours Per Day", "Income", "BMI", "Triglycerides",
        "Physical Activity Days Per Week", "Sleep Hours Per Day", "Country", "Continent",
        "Hemisphere", "Heart Attack Risk"
    ]
    
    parser = argparse.ArgumentParser(
        description='Sistema de gestão de registros médicos usando Cuckoo Hashing',
        add_help=False
    )
    parser.add_argument('--csv', default='heart.csv', help='Caminho do arquivo CSV')
    parser.add_argument('--help', action='help', help='Mostrar esta mensagem de ajuda')
    
    subparsers = parser.add_subparsers(dest='command', title='comandos')
    
    inserir_parser = subparsers.add_parser('inserir', help='Inserir novos registros')
    remover_parser = subparsers.add_parser('remover', help='Remover registros existentes')
    buscar_parser = subparsers.add_parser('buscar', help='Buscar registros')
    
    args = parser.parse_args()
    
    # Mostrar ajuda se nenhum comando for fornecido
    if not hasattr(args, 'command') or args.command is None:
        parser.print_help()
        return

    cuckoo = build_table(args.csv, feature_cols)
    
    print('\nDigite registros JSON (um por linha). Linha vazia para finalizar:')
    records = []
    while True:
        try:
            line = sys.stdin.readline().strip()
            if not line:
                break
            records.append(json.loads(line))
        except json.JSONDecodeError:
            print("Erro: JSON inválido! Tente novamente.")

    for record in records:
        try:
            key_tuple = tuple(str(record.get(col, '')) for col in feature_cols)
            key_str = json.dumps(key_tuple, sort_keys=True)
        except Exception as e:
            print(f"Erro ao processar registro: {e}")
            continue

        if args.command == 'inserir':
            success = cuckoo.insert(key_str, record)
            print("✅ Inserção bem-sucedida" if success else "❌ Chave duplicada (não inserido)")
            
        elif args.command == 'remover':
            success = cuckoo.remove(key_str)
            print("✅ Remoção bem-sucedida" if success else "❌ Registro não encontrado")
            
        elif args.command == 'buscar':
            result = cuckoo.search(key_str)
            print("🔍 Registro encontrado:", json.dumps(result, indent=2) if result else "🔍 Registro não encontrado")

if __name__ == '__main__':
    main()