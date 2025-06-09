import pandas as pd
import argparse
import json
import sys
import hashlib

class CountingBloomFilter:
    def __init__(self, size=100000, hash_count=5):
        self.size = size
        self.hash_count = hash_count
        self.count = [0] * size

    def _hashes(self, item):
        """Generate hash_count hash values for item."""
        item_bytes = item.encode('utf-8')
        for i in range(self.hash_count):
            hasher = hashlib.md5(item_bytes + i.to_bytes(2, byteorder='little'))
            yield int(hasher.hexdigest(), 16) % self.size

    def insert(self, item):
        for idx in self._hashes(item):
            self.count[idx] += 1

    def remove(self, item):
        for idx in self._hashes(item):
            if self.count[idx] > 0:
                self.count[idx] -= 1

    def search(self, item):
        return all(self.count[idx] > 0 for idx in self._hashes(item))
    
# Adicione esta função ao seu script
import time

def run_benchmark(csv_path, feature_cols, n_items):
    """Executa um benchmark completo no CountingBloomFilter."""
    print(f"--- Iniciando Benchmark com {n_items} Itens ---")
    
    # 1. Prepara os dados de teste
    df = pd.read_csv(csv_path).head(n_items)
    records_to_test = [json.dumps(tuple(row[col] for col in feature_cols)) for row in df.to_dict(orient="records")]
    
    # --- Medição de Performance ---
    resultados = {}

    # 2. Benchmark de INSERÇÃO
    bloom_insert = CountingBloomFilter(size=n_items * 20, hash_count=7) # Tamanho maior para menos colisões
    start_time = time.perf_counter()
    for item in records_to_test:
        bloom_insert.insert(item)
    resultados["Tempo de Inserção (s)"] = time.perf_counter() - start_time

    # 3. Benchmark de BUSCA (Itens existentes)
    start_time = time.perf_counter()
    for item in records_to_test:
        bloom_insert.search(item)
    resultados["Tempo de Busca (Existente) (s)"] = time.perf_counter() - start_time
    
    # 4. Benchmark de REMOÇÃO
    start_time = time.perf_counter()
    for item in records_to_test:
        bloom_insert.remove(item)
    resultados["Tempo de Remoção (s)"] = time.perf_counter() - start_time

    # --- Medição de Taxa de Falsos Positivos (MÉTRICA CRUCIAL) ---
    print("\nCalculando a taxa de falsos positivos...")
    bloom_fp = CountingBloomFilter(size=n_items * 20, hash_count=7)
    for item in records_to_test:
        bloom_fp.insert(item)

    # Cria itens que definitivamente NÃO estão no filtro
    test_items_not_in_filter = [f"item_falso_{i}" for i in range(n_items)]
    false_positive_count = 0
    for item in test_items_not_in_filter:
        if bloom_fp.search(item):
            false_positive_count += 1
            
    fp_rate = (false_positive_count / n_items)
    resultados["Taxa de Falsos Positivos"] = f"{fp_rate:.2%}"

    # 5. Exibe o Relatório Final
    print("\n--- Relatório de Benchmark do CountingBloomFilter ---")
    for metrica, valor in resultados.items():
        print(f"{metrica:<30}: {valor}")


def build_filter_and_index(csv_path, feature_cols):
    df = pd.read_csv(csv_path)
    bloom = CountingBloomFilter(size=200000, hash_count=7)
    index = {}
    for row in df.to_dict(orient="records"):
        key = tuple(row[col] for col in feature_cols)
        key_str = json.dumps(key)
        bloom.insert(key_str)
        index[key_str] = row
    return bloom, index

if __name__ == "__main__":
    feature_cols = [
        "Patient ID","Age","Sex","Cholesterol","Blood Pressure","Heart Rate",
        "Diabetes","Family History","Smoking","Obesity","Alcohol Consumption",
        "Exercise Hours Per Week","Diet","Previous Heart Problems","Medication Use",
        "Stress Level","Sedentary Hours Per Day","Income","BMI","Triglycerides",
        "Physical Activity Days Per Week","Sleep Hours Per Day","Country","Continent",
        "Hemisphere","Heart Attack Risk"
    ]

    parser = argparse.ArgumentParser(description="Counting Bloom Filter operations for heart dataset")
    parser.add_argument("--csv", default="heart_attack_prediction_dataset.csv", help="Path to CSV file")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("inserir", help="Inserir registros no filtro")
    sub.add_parser("remover", help="Remover registros do filtro")
    sub.add_parser("buscar", help="Buscar registros no filtro")

    bench_parser = sub.add_parser("benchmark", help="Executar um benchmark de performance")
    bench_parser.add_argument("--n_items", type=int, default=5000, help="Número de itens para usar no benchmark")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    bloom, index = build_filter_and_index(args.csv, feature_cols)
    print("Digite registros JSON, um por linha. Pressione Enter em linha vazia para finalizar.")
    records = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line.strip():
            break
        try:
            rec = json.loads(line)
            records.append(rec)
        except json.JSONDecodeError:
            print("JSON inválido, tente novamente.")

    for record in records:
        key = tuple(record[col] for col in feature_cols)
        key_str = json.dumps(key)
        if args.command == "inserir":
            bloom.insert(key_str)
            index[key_str] = record
            print("Inserido:", record)
        elif args.command == "remover":
            bloom.remove(key_str)
            index.pop(key_str, None)
            print("Removido:", record)
        elif args.command == "buscar":
            found = bloom.search(key_str)
            if found:
                # true positive or false positive
                data = index.get(key_str)
                if data:
                    print("Encontrado (positivo):", data)
                else:
                    print("Possível falso positivo para:", record)
            else:
                print("Definitivamente não existe:", record)
    args = parser.parse_args()

    # --- Lógica de Execução ---
    if args.command == "benchmark":
        run_benchmark(args.csv, feature_cols, args.n_items)
    elif args.command in ["inserir", "remover", "buscar"]:
        # Mantém a funcionalidade interativa original
        bloom, index = build_filter_and_index(args.csv, feature_cols)
        print("Digite registros JSON, um por linha. Pressione Enter em linha vazia para finalizar.")
        records = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if not line.strip():
                break
            try:
                rec = json.loads(line)
                records.append(rec)
            except json.JSONDecodeError:
                print("JSON inválido, tente novamente.")

        # ... (resto da sua lógica de loop para os comandos interativos) ...
        for record in records:
            key = tuple(record[col] for col in feature_cols)
            key_str = json.dumps(key)
            if args.command == "inserir":
                bloom.insert(key_str)
                index[key_str] = record
                print("Inserido:", record)
            elif args.command == "remover":
                bloom.remove(key_str)
                index.pop(key_str, None)
                print("Removido:", record)
            elif args.command == "buscar":
                found = bloom.search(key_str)
                if found:
                    data = index.get(key_str)
                    if data:
                        print("Encontrado (positivo):", data)
                    else:
                        print("Possível falso positivo para:", record)
                else:
                    print("Definitivamente não existe:", record)
    else:
        # Se nenhum comando foi dado
        parser.print_help()
        sys.exit(0)
