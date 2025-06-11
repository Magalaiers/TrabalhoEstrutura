# main.py - Versão Final, Completa e Interativa

import os
import sys
import time
import pandas as pd
import numpy as np
import joblib
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
import json
import random
import hashlib

# --- Constante para os Benchmarks ---
N_ITENS_BENCHMARK = 10000

# --- Seção de Compatibilidade para o Executável ---
def resource_path(relative_path):
    """ Obtém o caminho absoluto para o recurso, para funcionar no .exe """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Configurações Iniciais ---
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
sns.set_theme(style="whitegrid")
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# --- Imports das Estruturas de Dados ---
try:
    from src.estrutura_de_dados.lista_encadeada import Node # Importa o Node para a otimizada
    from src.estrutura_de_dados.lista_encadeada import LinkedList
    from src.estrutura_de_dados.lista_encadeada_otimizada import LinkedListOptimized
    from src.estrutura_de_dados.tabela_hash import HashTable
    from src.estrutura_de_dados.arvore_avl import AVLTree
    from src.estrutura_de_dados.cuckoo_hashing import CuckooHashing
    from src.estrutura_de_dados.bloom_filter2 import CountingBloomFilter
    from src.estrutura_de_dados.kd_tree import KDTree
    print("Estruturas de dados importadas com sucesso.")
except ImportError as e:
    print(f"--- ERRO CRÍTICO ---\nErro ao importar estruturas: {e}\nVerifique os arquivos em 'src/'.")
    input("Pressione Enter para sair."); sys.exit(1)

# --- Adição de métodos de memória ---
def get_ll_memory_usage(self):
    if not self.head: return 0
    size = sys.getsizeof(self)
    node = self.head
    while node: size += sys.getsizeof(node); node = node.next
    return size
LinkedList.get_memory_usage = get_ll_memory_usage
LinkedListOptimized.get_memory_usage = get_ll_memory_usage

# --- Cache e Funções de Inicialização ---
RECURSOS_CARREGADOS = {"df": None, "modelo": None, "scaler": None, "X_encoded": None, "y": None}

def carregar_recursos():
    if RECURSOS_CARREGADOS["df"] is not None: return True
    print("Carregando recursos (Dataset, Modelo de ML, etc.)...")
    try:
        path_df = resource_path(os.path.join("dataset", "heart_attack_prediction_dataset.csv"))
        df_raw = pd.read_csv(path_df)
        df_processed = df_raw.copy()
        if 'Blood Pressure' in df_processed.columns and df_processed['Blood Pressure'].dtype == 'object':
            split_bp = df_processed['Blood Pressure'].str.split('/', expand=True)
            df_processed['Pressao_Sistolica'] = pd.to_numeric(split_bp[0], errors='coerce')
            df_processed['Pressao_Diastolica'] = pd.to_numeric(split_bp[1], errors='coerce')
            df_processed = df_processed.drop(columns=['Blood Pressure'])
        if 'Patient ID' in df_processed.columns: df_processed = df_processed.drop('Patient ID', axis=1)
        df_processed.fillna(df_processed.median(numeric_only=True), inplace=True)
        RECURSOS_CARREGADOS["df"] = df_processed
        
        colunas_para_modelo = [
            'Age', 'Sex', 'Cholesterol', 'Heart Rate', 'Diabetes', 'Family History', 'Smoking', 'Obesity', 
            'Alcohol Consumption', 'Exercise Hours Per Week', 'Diet', 'Previous Heart Problems', 'Medication Use', 
            'Stress Level', 'Sedentary Hours Per Day', 'Income', 'BMI', 'Triglycerides', 
            'Physical Activity Days Per Week', 'Sleep Hours Per Day', 'Pressao_Sistolica', 'Pressao_Diastolica'
        ]
        colunas_para_modelo = [col for col in colunas_para_modelo if col in df_processed.columns]
        X = df_processed[colunas_para_modelo]
        y = df_processed['Heart Attack Risk']
        X_encoded = pd.get_dummies(X, drop_first=True)
        RECURSOS_CARREGADOS["X_encoded"] = X_encoded
        RECURSOS_CARREGADOS["y"] = y

        path_modelo = resource_path(os.path.join('models', 'modelo_arvore_final.joblib'))
        path_scaler = resource_path(os.path.join('models', 'scaler.joblib'))
        RECURSOS_CARREGADOS["modelo"] = joblib.load(path_modelo)
        RECURSOS_CARREGADOS["scaler"] = joblib.load(path_scaler)
    except FileNotFoundError as e:
        print(f"❌ ERRO CRÍTICO: Arquivo não encontrado: {e.filename}"); return False
    except Exception as e:
        print(f"❌ ERRO CRÍTICO ao carregar recursos: {e}"); return False
    print("✅ Recursos prontos e sincronizados.")
    return True

def inicializar_sistemas(num_registros=100):
    df = RECURSOS_CARREGADOS["df"]
    print(f"Populando estruturas com {num_registros} registros iniciais...")
    dados_numericos = df['Age'].head(num_registros).tolist()
    dados_chave_valor = df['Age'].head(num_registros).to_dict()
    dados_strings_json = [json.dumps(tuple(row)) for row in df.head(num_registros).to_numpy().tolist()]
    dados_pontos_2d = df[['Age', 'Cholesterol']].head(num_registros).to_numpy().tolist()
    sistemas = {
        "Lista Encadeada (Original)": LinkedList(),
        "Lista Encadeada (Otimizada)": LinkedListOptimized(),
        "Tabela Hash": HashTable(size=num_registros*2),
        "Árvore AVL": AVLTree(),
        "Cuckoo Hashing": CuckooHashing(size=num_registros*2),
        "Counting Bloom Filter": CountingBloomFilter(size=num_registros*20, hash_count=7),
        "KD-Tree (2D: Age, Cholesterol)": KDTree(dados_pontos_2d)
    }
    for item in dados_numericos:
        sistemas["Lista Encadeada (Original)"].insert(item)
        sistemas["Lista Encadeada (Otimizada)"].insert(item)
        sistemas["Árvore AVL"].insert(item)
    for key, value in dados_chave_valor.items():
        sistemas["Tabela Hash"].insert(key, value)
        sistemas["Cuckoo Hashing"].insert(key, value)
    for item_str in dados_strings_json:
        sistemas["Counting Bloom Filter"].insert(item_str)
    print("✅ Sistemas de estruturas de dados prontos.")
    return sistemas

def mostrar_menu_principal(sistemas):
    num_estruturas = len(sistemas)
    print("\n" + "="*50, "\n   SISTEMA DE ANÁLISE E PREVISÃO\n" + "="*50)
    print("--- Gerenciamento Interativo de Estruturas ---")
    for i, nome in enumerate(sistemas.keys()):
        print(f"{i+1}. Gerenciar {nome}")
    print("\n--- Benchmarks e Análises ---")
    print(f"{num_estruturas+1}. Executar Benchmark de Acesso Médio")
    print(f"{num_estruturas+2}. Executar Benchmark de Latência Média")
    print(f"{num_estruturas+3}. Executar Testes de Restrição")
    print("\n--- Módulo de Previsão ---")
    print(f"{num_estruturas+4}. Prever Risco de Ataque Cardíaco")
    print("\n" + "-"*50)
    print(f"{num_estruturas+5}. Sair")
    print("="*50)

def formatar_tempo(segundos):
    if segundos * 1000 < 1: return f"{segundos * 1_000_000:.2f} µs"
    if segundos < 1: return f"{segundos * 1000:.2f} ms"
    return f"{segundos:.4f} s"

# --- Funções de Sub-Menu para Gerenciamento ---
def gerenciar_simples(instancia, nome_estrutura):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear'); print("="*50, f"\nGerenciando: {nome_estrutura}\n", "="*50, sep="")
        print(f"Estado atual (primeiros 30 itens): {str(instancia)[:120]}...")
        print("\nOpções:\n1. Inserir\n2. Buscar\n3. Remover\n4. Ver Memória\n5. Voltar")
        escolha = input("Sua escolha: ")
        if escolha == '1':
            try: item = int(input("Valor numérico para inserir: "))
            except ValueError: print("Valor inválido."); continue
            start = time.perf_counter(); instancia.insert(item); tempo = time.perf_counter() - start; print(f"'{item}' inserido. (Execução: {formatar_tempo(tempo)})")
        elif escolha == '2':
            try: item = int(input("Valor numérico para buscar: "))
            except ValueError: print("Valor inválido."); continue
            start = time.perf_counter(); encontrado = instancia.search(item); tempo = time.perf_counter() - start
            print(f"Busca por '{item}': {'ENCONTRADO' if encontrado else 'NÃO ENCONTRADO'}. (Execução: {formatar_tempo(tempo)})")
        elif escolha == '3':
            try: item = int(input("Valor numérico para remover: "))
            except ValueError: print("Valor inválido."); continue
            start = time.perf_counter(); removido = instancia.remove(item); tempo = time.perf_counter() - start
            print(f"Remoção de '{item}': {'removido com sucesso' if removido else 'não encontrado'}. (Execução: {formatar_tempo(tempo)})")
        elif escolha == '4':
            memoria = instancia.get_memory_usage()
            print(f"Uso de memória estimado: {memoria:,} bytes ({memoria/1024:.2f} KB)")
        elif escolha == '5': return
        else: print("Opção inválida.")
        input("\nPressione Enter para continuar...")

def gerenciar_hash_kv(instancia, nome_estrutura):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear'); print("="*50, f"\nGerenciando: {nome_estrutura}\n", "="*50, sep="")
        print(f"\nEstado atual: {type(instancia).__name__} populada.")
        print("\nOpções:\n1. Inserir (chave, valor)\n2. Buscar por chave\n3. Remover por chave\n4. Ver Memória\n5. Voltar")
        escolha = input("Sua escolha: ")
        if escolha == '1':
            try: key, value = int(input("CHAVE (int): ")), int(input("VALOR (int): "))
            except ValueError: print("Valores inválidos."); continue
            start = time.perf_counter(); instancia.insert(key, value); tempo = time.perf_counter() - start
            print(f"Par ({key}, {value}) inserido. (Execução: {formatar_tempo(tempo)})")
        elif escolha == '2':
            try: key = int(input("CHAVE (int) para buscar: "))
            except ValueError: print("Valor inválido."); continue
            start = time.perf_counter(); valor_encontrado = instancia.search(key); tempo = time.perf_counter() - start
            resultado = f"ENCONTRADO (Valor: {valor_encontrado})" if valor_encontrado is not None else "NÃO ENCONTRADO"
            print(f"Busca por chave '{key}': {resultado}. (Execução: {formatar_tempo(tempo)})")
        elif escolha == '3':
            try: key = int(input("CHAVE (int) para remover: "))
            except ValueError: print("Valor inválido."); continue
            start = time.perf_counter(); removido = instancia.remove(key); tempo = time.perf_counter() - start
            resultado = "removido com sucesso" if removido else "não encontrado"
            print(f"Remoção da chave '{key}': {resultado}. (Execução: {formatar_tempo(tempo)})")
        elif escolha == '4':
            memoria = instancia.get_memory_usage()
            print(f"Uso de memória estimado: {memoria:,} bytes ({memoria/1024:.2f} KB)")
        elif escolha == '5': return
        else: print("Opção inválida.")
        input("\nPressione Enter para continuar...")

def gerenciar_bloom_filter(instancia, nome_estrutura):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear'); print("="*50, f"\nGerenciando: {nome_estrutura}\n", "="*50, sep="")
        print(f"\nEstado: Filtro com {instancia.size} posições e {instancia.hash_count} hashes.")
        print("\nOpções:\n1. Inserir item\n2. Buscar item\n3. Remover item\n4. Ver Memória\n5. Voltar")
        escolha = input("Sua escolha: ")
        if escolha == '1':
            item = input("Digite o item (string) para inserir: ")
            start = time.perf_counter(); instancia.insert(item); tempo = time.perf_counter() - start; print(f"'{item}' inserido. (Execução: {formatar_tempo(tempo)})")
        elif escolha == '2':
            item = input("Digite o item (string) para buscar: ")
            start = time.perf_counter(); encontrado = instancia.search(item); tempo = time.perf_counter() - start
            if encontrado: print(f"Resultado: '{item}' POSSIVELMENTE está no conjunto. (Execução: {formatar_tempo(tempo)})")
            else: print(f"Resultado: '{item}' DEFINITIVAMENTE NÃO está no conjunto. (Execução: {formatar_tempo(tempo)})")
        elif escolha == '3':
            item = input("Digite o item (string) para remover: ")
            start = time.perf_counter(); instancia.remove(item); tempo = time.perf_counter() - start
            print(f"'{item}' removido. (Execução: {formatar_tempo(tempo)})")
        elif escolha == '4':
            memoria = instancia.get_memory_usage()
            print(f"Uso de memória estimado: {memoria:,} bytes ({memoria/1024:.2f} KB)")
        elif escolha == '5': return
        else: print("Opção inválida.")
        input("\nPressione Enter para continuar...")

def gerenciar_kdtree(instancia, nome_estrutura):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear'); print("="*50, f"\nGerenciando: {nome_estrutura}\n", "="*50, sep="")
        print("\nKD-Tree populada. Operação principal: Busca por Vizinho Mais Próximo.")
        print("\nOpções:\n1. Encontrar vizinho mais próximo\n2. Ver Memória\n3. Voltar")
        escolha = input("Sua escolha: ")
        if escolha == '1':
            try:
                px = int(input("Digite a coordenada X (Idade) do ponto de busca (ex: 50): "))
                py = int(input("Digite a coordenada Y (Colesterol) do ponto de busca (ex: 250): "))
            except ValueError: print("Coordenadas inválidas."); continue
            query_point = (px, py)
            start = time.perf_counter(); vizinho = instancia.find_nearest_neighbor(query_point); tempo = time.perf_counter() - start
            print(f"\nVizinho mais próximo de {query_point} é: {vizinho}. (Execução: {formatar_tempo(tempo)})")
        elif escolha == '2':
            memoria = instancia.get_memory_usage()
            print(f"Uso de memória estimado: {memoria:,} bytes ({memoria/1024:.2f} KB)")
        elif escolha == '3': return
        else: print("Opção inválida.")
        input("\nPressione Enter para continuar...")

def gerenciar_estrutura_principal(nome_estrutura, instancia):
    if isinstance(instancia, KDTree): gerenciar_kdtree(instancia, nome_estrutura)
    elif isinstance(instancia, CountingBloomFilter): gerenciar_bloom_filter(instancia, nome_estrutura)
    elif isinstance(instancia, (HashTable, CuckooHashing)): gerenciar_hash_kv(instancia, nome_estrutura)
    else: gerenciar_simples(instancia, nome_estrutura)

# --- Funções para Benchmarks e Testes ---
def executar_benchmark_acesso_medio():
    os.system('cls' if os.name == 'nt' else 'clear'); print("--- Benchmark de Tempo Médio de Acesso ---")
    N_ACESSOS = 1000; df = RECURSOS_CARREGADOS['df']
    
    # --- CORREÇÃO AQUI ---
    n_real = min(N_ITENS_BENCHMARK, len(df))
    if n_real < N_ACESSOS:
        print("Dataset muito pequeno para um benchmark de acesso médio significativo.")
        return
    print(f"Usando N={n_real} para o teste.")
    # ---------------------
    
    dados_numericos = df['Age'].head(n_real).tolist()
    dados_chave_valor = df['Age'].head(n_real).to_dict()
    indices_aleatorios = np.random.randint(0, n_real, size=N_ACESSOS)
    
    estruturas = {"Lista Encadeada (Otimizada)": LinkedListOptimized(), "Tabela Hash": HashTable(size=n_real*2), "Árvore AVL": AVLTree()}
    resultados = {}
    print(f"Populando estruturas com {n_real} itens e executando {N_ACESSOS} buscas aleatórias...")
    for nome, instancia in estruturas.items():
        if isinstance(instancia, HashTable):
            for k,v in dados_chave_valor.items(): instancia.insert(k,v)
            itens_busca = indices_aleatorios
        else:
            for item in dados_numericos: instancia.insert(item)
            itens_busca = [dados_numericos[i] for i in indices_aleatorios]
        
        start = time.perf_counter(); [instancia.search(i) for i in itens_busca]; tempo_total = time.perf_counter() - start
        resultados[nome] = (tempo_total / N_ACESSOS) * 1e6
    
    df_acesso = pd.DataFrame.from_dict(resultados, orient='index', columns=['Tempo Médio de Acesso (µs)'])
    print("\n--- Resultados ---"); print(df_acesso.round(2))

def executar_benchmark_latencia_media():
    os.system('cls' if os.name == 'nt' else 'clear'); print("--- Benchmark de Latência Média (Carga Mista) ---")
    
    # --- CORREÇÃO AQUI ---
    n_real = min(N_ITENS_BENCHMARK, len(RECURSOS_CARREGADOS['df']))
    print(f"Usando N={n_real} para o teste.")
    # ---------------------

    operacoes = np.random.choice(['insercao', 'busca', 'remocao'], size=n_real, p=[0.5, 0.4, 0.1])
    chaves = np.random.randint(0, n_real*2, size=n_real)
    estruturas = {"Lista Encadeada (Otimizada)": LinkedListOptimized(), "Árvore AVL": AVLTree(), "Tabela Hash": HashTable(size=n_real*2)}
    resultados = {}
    print(f"Executando {n_real} operações mistas em cada estrutura...")
    for nome, instancia in estruturas.items():
        start = time.perf_counter()
        for op, chave in zip(operacoes, chaves):
            if op == 'insercao': instancia.insert(chave, chave) if isinstance(instancia, HashTable) else instancia.insert(chave)
            elif op == 'busca': instancia.search(chave)
            elif op == 'remocao': instancia.remove(chave)
        tempo_total = time.perf_counter() - start
        resultados[nome] = (tempo_total / n_real) * 1e6
    df_latencia = pd.DataFrame.from_dict(resultados, orient='index', columns=['Latência Média por Operação (µs)'])
    print("\n--- Resultados ---"); print(df_latencia.round(2))

def _teste_memoria():
    print("\n--- Executando Teste de Memória (R3) ---"); df_original = RECURSOS_CARREGADOS['df']
    memoria_antes = df_original.memory_usage(deep=True).sum()
    df_compactado = df_original.copy()
    for col in df_compactado.select_dtypes(include=np.number).columns:
        df_compactado[col] = pd.to_numeric(df_compactado[col], downcast='float'); df_compactado[col] = pd.to_numeric(df_compactado[col], downcast='integer')
    memoria_depois = df_compactado.memory_usage(deep=True).sum()
    print(f"Memória Original: {memoria_antes/1e6:.2f} MB | Memória Compactada: {memoria_depois/1e6:.2f} MB")
    if memoria_antes > 0: print(f"Redução: {(1 - memoria_depois/memoria_antes):.2%}")

def _teste_processamento():
    print("\n--- Executando Teste de Processamento (R9) ---"); N_ITENS = 3000
    dados_teste = RECURSOS_CARREGADOS['df']['Age'].head(N_ITENS)
    print("Realizando 'aquecimento' da CPU..."); avl_warmup = AVLTree(); [avl_warmup.insert(item) for item in dados_teste.head(500)]; time.sleep(0.5)
    print("CPU 'aquecida'. Iniciando medições...")
    tempos_normais, tempos_carga = [], []
    N_RODADAS = 5
    for _ in range(N_RODADAS):
        avl_normal = AVLTree(); start_normal = time.perf_counter(); [avl_normal.insert(item) for item in dados_teste]; tempos_normais.append(time.perf_counter() - start_normal)
        avl_carga = AVLTree(); start_carga = time.perf_counter()
        for item in dados_teste: avl_carga.insert(item); [(_**2) for _ in range(10)]
        tempos_carga.append(time.perf_counter() - start_carga)
    avg_normal = np.mean(tempos_normais[1:]); avg_carga = np.mean(tempos_carga[1:])
    print(f"Tempo médio de inserção normal: {avg_normal:.4f} segundos")
    print(f"Tempo médio com carga extra:   {avg_carga:.4f} segundos")
    if avg_normal > 0 and avg_carga > avg_normal: print(f"Aumento no tempo de execução: {((avg_carga - avg_normal) / avg_normal):.2%}")
    else: print("Resultado do teste inconsistente.")

def _teste_latencia_restricao():
    print("\n--- Executando Teste de Latência (R11) ---"); N_BUSCAS = 2000
    ht = HashTable(size=N_BUSCAS*2); [ht.insert(i,i) for i in range(N_BUSCAS)]
    start = time.perf_counter(); [ht.search(i) for i in range(N_BUSCAS)]; tempo_normal = time.perf_counter() - start
    print(f"Tempo para {N_BUSCAS} buscas (sem latência): {tempo_normal:.4f} segundos")
    LATENCIA_SIMULADA = 0.0001
    start = time.perf_counter()
    for i in range(N_BUSCAS): ht.search(i); time.sleep(LATENCIA_SIMULADA)
    tempo_latencia = time.perf_counter() - start
    print(f"Tempo com latência de {LATENCIA_SIMULADA*1000:.1f}ms por busca: {tempo_latencia:.4f} segundos")

def _teste_dados():
    print("\n--- Executando Teste de Dados (R18) ---")
    try:
        modelo, scaler, X_encoded, y = (RECURSOS_CARREGADOS["modelo"], RECURSOS_CARREGADOS["scaler"], RECURSOS_CARREGADOS["X_encoded"], RECURSOS_CARREGADOS["y"])
        from sklearn.model_selection import train_test_split
        _, X_test_original, _, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)
        expected_features = scaler.feature_names_in_
        X_test_alinhado = X_test_original.reindex(columns=expected_features, fill_value=0)
        X_test_scaled = scaler.transform(X_test_alinhado)
        acuracia_original = modelo.score(X_test_scaled, y_test)
        print(f"Acurácia em dados limpos: {acuracia_original:.2%}")
        X_test_corrompido = X_test_scaled.copy()
        coluna_age_index = list(X_test_alinhado.columns).index('Age')
        indices = np.random.choice(X_test_corrompido.shape[0], size=int(X_test_corrompido.shape[0]*0.15), replace=False)
        X_test_corrompido[indices, coluna_age_index] = 99
        acuracia_corrompida = modelo.score(X_test_corrompido, y_test)
        print(f"Acurácia em dados corrompidos: {acuracia_corrompida:.2%}")
    except Exception as e: print(f"Ocorreu um erro inesperado no teste de dados: {e}")

def _teste_algoritmico():
    print("\n--- Executando Teste Algorítmico (R23) ---")
    
    # --- CORREÇÃO AQUI ---
    n_real = min(N_ITENS_BENCHMARK, len(RECURSOS_CARREGADOS['df']))
    print(f"Usando N={n_real} para o teste.")
    # ---------------------

    def encrypt_data(data): return hashlib.sha256(str(data).encode()).hexdigest()
    dados = RECURSOS_CARREGADOS['df']['Age'].head(n_real).to_dict()
    ht_normal = HashTable(size=n_real*2); start = time.perf_counter(); [ht_normal.insert(k, v) for k,v in dados.items()]; tempo_normal = time.perf_counter() - start
    print(f"Tempo de inserção normal: {tempo_normal:.4f} segundos")
    ht_enc = HashTable(size=n_real*2); start = time.perf_counter()
    for k, v in dados.items(): ht_enc.insert(k, encrypt_data(v))
    tempo_enc = time.perf_counter() - start
    print(f"Tempo de inserção com 'encriptação': {tempo_enc:.4f} segundos")
    if tempo_normal > 0: print(f"Aumento no tempo: {((tempo_enc - tempo_normal) / tempo_normal):.2%}")

def executar_testes_restricao():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear'); print("--- Módulo de Testes de Restrição ---"); print("Escolha um teste para executar:")
        print("1. Teste de Memória (R3)\n2. Teste de Processamento (R9)\n3. Teste de Latência (R11)\n4. Teste de Dados (R18)\n5. Teste Algorítmico (R23)\n6. Voltar")
        escolha = input("Sua escolha: ")
        if escolha == '1': _teste_memoria()
        elif escolha == '2': _teste_processamento()
        elif escolha == '3': _teste_latencia_restricao()
        elif escolha == '4': _teste_dados()
        elif escolha == '5': _teste_algoritmico()
        elif escolha == '6': break
        else: print("Opção inválida.")
        input("\nPressione Enter para continuar...")

def executar_previsao_paciente():
    os.system('cls' if os.name == 'nt' else 'clear'); print("="*50, f"\nMódulo de Previsão de Risco Cardíaco\n", "="*50, sep="")
    modelo, scaler, df, X_encoded, y = (RECURSOS_CARREGADOS["modelo"], RECURSOS_CARREGADOS["scaler"], RECURSOS_CARREGADOS["df"], RECURSOS_CARREGADOS["X_encoded"], RECURSOS_CARREGADOS["y"])
    try:
        idx = int(input(f"Digite o índice do paciente para prever (0 a {len(df)-1}): "))
        if not (0 <= idx < len(df)): print("Índice inválido."); return
    except ValueError: print("Entrada inválida."); return
    colunas_do_modelo = pd.DataFrame(columns=scaler.get_feature_names_out())
    paciente_a_prever, _ = X_encoded.align(colunas_do_modelo, axis=1, fill_value=0)
    paciente_a_prever = paciente_a_prever.iloc[[idx]]
    paciente_scaled = scaler.transform(paciente_a_prever)
    previsao, probabilidade = modelo.predict(paciente_scaled)[0], modelo.predict_proba(paciente_scaled)[0]
    print("\n--- Relatório de Risco para o Paciente de Índice {} ---".format(idx))
    resultado_previsto = "ALTO RISCO" if previsao == 1 else "Baixo Risco"; confianca = probabilidade[previsao]
    print(f"Previsão do Modelo: {resultado_previsto} (Confiança: {confianca:.2%})")
    print("\n--- Verificação da Previsão ---")
    y_real = y.iloc[idx]; resultado_real = "ALTO RISCO" if y_real == 1 else "Baixo Risco"
    print(f"Valor Real no Dataset: {resultado_real}")
    if previsao == y_real: print("✅ O modelo ACERTOU a previsão.")
    else: print("❌ O modelo ERROU a previsão.")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    if not carregar_recursos(): input("Pressione Enter para sair."); sys.exit(1)
    sistemas = inicializar_sistemas()
    if sistemas is None: input("Pressione Enter para sair."); sys.exit(1)
    nomes_sistemas = list(sistemas.keys()); num_estruturas = len(sistemas)
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        mostrar_menu_principal(sistemas)
        try:
            escolha = int(input("Digite o número da sua escolha: "))
            if 1 <= escolha <= num_estruturas:
                gerenciar_estrutura_principal(nomes_sistemas[escolha - 1], sistemas[nomes_sistemas[escolha - 1]])
            elif escolha == num_estruturas + 1: executar_benchmark_acesso_medio()
            elif escolha == num_estruturas + 2: executar_benchmark_latencia_media()
            elif escolha == num_estruturas + 3: executar_testes_restricao()
            elif escolha == num_estruturas + 4: executar_previsao_paciente()
            elif escolha == num_estruturas + 5: print("Saindo..."); break
            else: print("Opção inválida.")
        except (ValueError, IndexError):
            print("Entrada inválida.")
        input("\nPressione Enter para voltar ao menu principal...")

if __name__ == "__main__":
    main()