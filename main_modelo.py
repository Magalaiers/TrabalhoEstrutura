# main.py
import os
import sys
import time
import pandas as pd
import joblib
import warnings
import json

# --- Seção de Compatibilidade para o Executável ---
def resource_path(relative_path):
    """
    Obtém o caminho absoluto para o recurso. Funciona tanto no ambiente de
    desenvolvimento quanto no executável criado pelo PyInstaller.
    """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Se não estiver rodando como um executável, usa o caminho normal
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# --- Configurações Iniciais ---
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# --- Imports das suas Estruturas de Dados ---
try:
    from src.estrutura_de_dados.lista_encadeada import Node # Importa o Node para a otimizada
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
def get_ll_memory_usage(self):
    if not self.head: return 0
    size = sys.getsizeof(self)
    node = self.head
    while node:
        size += sys.getsizeof(node)
        node = node.next
    return size
LinkedListOptimized.get_memory_usage = get_ll_memory_usage

# --- Cache e Funções de Inicialização ---
RECURSOS_CARREGADOS = {"df": None, "modelo": None, "scaler": None, "X_encoded": None, "y": None}

def carregar_recursos():
    """Carrega o DataFrame, o modelo e o scaler uma única vez."""
    if RECURSOS_CARREGADOS["df"] is not None: return True
    print("Carregando recursos (Dataset, Modelo de ML, etc.)...")
    try:
        # --- AJUSTE DE BOAS PRÁTICAS AQUI ---
        path_df = resource_path(os.path.join("dataset", "heart_attack_prediction_dataset.csv"))
        path_modelo = resource_path(os.path.join('models', 'melhor_modelo_otimizado.joblib'))
        path_scaler = resource_path(os.path.join('models', 'scaler.joblib'))
        
        df = pd.read_csv(path_df)
        if 'Patient ID' in df.columns:
            df = df.drop('Patient ID', axis=1)
        RECURSOS_CARREGADOS["df"] = df
        
        RECURSOS_CARREGADOS["modelo"] = joblib.load(path_modelo)
        RECURSOS_CARREGADOS["scaler"] = joblib.load(path_scaler)
        
        X = df.drop('Heart Attack Risk', axis=1)
        y = df['Heart Attack Risk']
        RECURSOS_CARREGADOS["X_encoded"] = pd.get_dummies(X, drop_first=True)
        RECURSOS_CARREGADOS["y"] = y

    except FileNotFoundError as e:
        print(f"❌ ERRO CRÍTICO: Arquivo não encontrado: {e.filename}")
        print("Certifique-se de que as pastas 'dataset' e 'models' estão no mesmo diretório que o executável.")
        return False
    print("✅ Recursos prontos.")
    return True

def inicializar_sistemas(num_registros=100):
    df = RECURSOS_CARREGADOS["df"]
    print(f"Populando estruturas com {num_registros} registros iniciais...")
    
    dados_numericos = df['Age'].head(num_registros).tolist()
    dados_chave_valor = df['Age'].head(num_registros).to_dict()
    dados_strings_json = [json.dumps(tuple(row)) for row in df.head(num_registros).to_numpy().tolist()]
    dados_pontos_2d = df[['Age', 'Cholesterol']].head(num_registros).to_numpy().tolist()

    sistemas = {
        "Lista Encadeada Otimizada": LinkedListOptimized(), "Tabela Hash": HashTable(size=num_registros*2),
        "Árvore AVL": AVLTree(), "Cuckoo Hashing": CuckooHashing(size=num_registros*2),
        "Counting Bloom Filter": CountingBloomFilter(size=num_registros*20, hash_count=7),
        "KD-Tree (2D: Age, Cholesterol)": KDTree(dados_pontos_2d)
    }
    for item in dados_numericos:
        sistemas["Lista Encadeada Otimizada"].insert(item)
        sistemas["Árvore AVL"].insert(item)
    for key, value in dados_chave_valor.items():
        sistemas["Tabela Hash"].insert(key, value)
        sistemas["Cuckoo Hashing"].insert(key, value)
    for item_str in dados_strings_json:
        sistemas["Counting Bloom Filter"].insert(item_str)
        
    print("✅ Sistemas de estruturas de dados prontos.")
    return sistemas

def mostrar_menu_principal(sistemas):
    print("\n" + "="*50, "\n   SISTEMA DE ANÁLISE E PREVISÃO\n" + "="*50)
    print("--- Operações com Estruturas de Dados ---")
    for i, nome in enumerate(sistemas.keys()):
        print(f"{i+1}. Gerenciar {nome}")
    print("\n--- Módulo de Previsão ---")
    print(f"{len(sistemas)+1}. Prever Risco de Ataque Cardíaco para Paciente")
    print("\n" + "-"*50)
    print(f"{len(sistemas)+2}. Sair")
    print("="*50)

def formatar_tempo(segundos):
    if segundos * 1000 < 1: return f"{segundos * 1_000_000:.2f} µs"
    if segundos < 1: return f"{segundos * 1000:.2f} ms"
    return f"{segundos:.4f} s"

def gerenciar_simples(instancia):
    while True:
        escolha = instancia
        if escolha == '1':
            try: item = int(input("Valor numérico para inserir: "))
            except ValueError: print("Valor inválido."); continue
            start = time.perf_counter(); instancia.insert(item); tempo = time.perf_counter() - start
            print(f"'{item}' inserido. (Execução: {formatar_tempo(tempo)})")
        elif escolha == '2':
            try: item = int(input("Valor numérico para buscar: "))
            except ValueError: print("Valor inválido."); continue
            start = time.perf_counter(); encontrado = instancia.search(item); tempo = time.perf_counter() - start
            resultado = "ENCONTRADO" if encontrado else "NÃO ENCONTRADO"
            print(f"Busca por '{item}': {resultado}. (Execução: {formatar_tempo(tempo)})")
        elif escolha == '3':
            try: item = int(input("Valor numérico para remover: "))
            except ValueError: print("Valor inválido."); continue
            start = time.perf_counter(); removido = instancia.remove(item); tempo = time.perf_counter() - start
            resultado = "removido com sucesso" if removido else "não encontrado"
            print(f"Remoção de '{item}': {resultado}. (Execução: {formatar_tempo(tempo)})")
        elif escolha == '4':
            memoria = instancia.get_memory_usage()
            print(f"Uso de memória estimado: {memoria} bytes ({memoria/1024:.2f} KB)")
        elif escolha == '5': return
        else: print("Opção inválida.")
        input("\nPressione Enter para continuar...")
        os.system('cls' if os.name == 'nt' else 'clear')

def gerenciar_hash_kv(instancia):
    while True:
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
            print(f"Uso de memória estimado: {memoria} bytes ({memoria/1024:.2f} KB)")
        elif escolha == '5': return
        else: print("Opção inválida.")
        input("\nPressione Enter para continuar...")
        os.system('cls' if os.name == 'nt' else 'clear')

def gerenciar_bloom_filter(instancia):
    while True:
        print(f"\nEstado: Filtro com {instancia.size} posições e {instancia.hash_count} hashes.")
        print("\nOpções:\n1. Inserir item\n2. Buscar item\n3. Remover item\n4. Ver Memória\n5. Voltar")
        escolha = input("Sua escolha: ")
        if escolha == '1':
            item = input("Digite o item (string) para inserir: ")
            start = time.perf_counter(); instancia.insert(item); tempo = time.perf_counter() - start
            print(f"'{item}' inserido. (Execução: {formatar_tempo(tempo)})")
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
            print(f"Uso de memória estimado: {memoria} bytes ({memoria/1024:.2f} KB)")
        elif escolha == '5': return
        else: print("Opção inválida.")
        input("\nPressione Enter para continuar...")
        os.system('cls' if os.name == 'nt' else 'clear')

def gerenciar_kdtree(instancia):
    while True:
        print("\nKD-Tree populada. Operação principal: Busca por Vizinho Mais Próximo.")
        print("\nOpções:\n1. Inserir item\n2. Encontrar vizinho mais próximo\n3. Remover item\n4. Ver Memória\n5. Voltar")
def gerenciar_kdtree(instancia):
    while True:
        print("\nKD-Tree populada. Operação principal: Busca por Vizinho Mais Próximo.")
        print("\nOpções:\n1. Inserir item\n2. Encontrar vizinho mais próximo\n3. Remover item\n4. Ver Memória\n5. Voltar")
        escolha = input("Sua escolha: ")
        if escolha == '1':
            try:
                px = int(input("Digite a coordenada X (Idade) do ponto de inserção (ex: 50): "))
                py = int(input("Digite a coordenada Y (Colesterol) do ponto de inserção (ex: 250): "))
                item = (px, py)
            except ValueError:
                print("Coordenadas inválidas.")
                input("\nPressione Enter para continuar...")
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            start = time.perf_counter()
            instancia.insert(item)
            tempo = time.perf_counter() - start
            print(f"'{item}' inserido. (Execução: {formatar_tempo(tempo)})")
        elif escolha == '2':
            try:
                px = int(input("Digite a coordenada X (Idade) do ponto de busca (ex: 50): "))
                py = int(input("Digite a coordenada Y (Colesterol) do ponto de busca (ex: 250): "))
                query_point = (px, py)
            except ValueError:
                print("Coordenadas inválidas.")
                input("\nPressione Enter para continuar...")
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            start = time.perf_counter()
            vizinho = instancia.find_nearest_neighbor(query_point)
            tempo = time.perf_counter() - start
            print(f"\nVizinho mais próximo de {query_point} é: {vizinho}. (Execução: {formatar_tempo(tempo)})")
        elif escolha == '3':
            try:
                px = int(input("Digite a coordenada X (Idade) do ponto de exclusão (ex: 50): "))
                py = int(input("Digite a coordenada Y (Colesterol) do ponto de exclusão (ex: 250): "))
                item = (px, py)
            except ValueError:
                print("Coordenadas inválidas.")
                input("\nPressione Enter para continuar...")
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            start = time.perf_counter()
            instancia.remove(item)
            tempo = time.perf_counter() - start
            print(f"'{item}' removido. (Execução: {formatar_tempo(tempo)})")
        elif escolha == '4':
            memoria = instancia.get_memory_usage()
            print(f"Uso de memória estimado: {memoria} bytes ({memoria / 1024:.2f} KB)")
        elif escolha == '5':
            return
        else:
            print("Opção inválida.")
        input("\nPressione Enter para continuar...")
        os.system('cls' if os.name == 'nt' else 'clear')
    print("="*50, f"\nGerenciando: {nome_estrutura}\n", "="*50, sep="")
    if isinstance(instancia, KDTree): gerenciar_kdtree(instancia)
    elif isinstance(instancia, CountingBloomFilter): gerenciar_bloom_filter(instancia)
    elif isinstance(instancia, (HashTable, CuckooHashing)): gerenciar_hash_kv(instancia)
    else: gerenciar_simples(instancia)

def gerenciar_estrutura_principal(nome_estrutura, instancia):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*50, f"\nGerenciando: {nome_estrutura}\n", "="*50, sep="")
    if isinstance(instancia, KDTree): gerenciar_kdtree(instancia)
    elif isinstance(instancia, CountingBloomFilter): gerenciar_bloom_filter(instancia)
    elif isinstance(instancia, (HashTable, CuckooHashing)): gerenciar_hash_kv(instancia)
    else: gerenciar_simples(instancia)

def executar_previsao_paciente():
    """Função para o módulo de previsão de ML com verificação de acerto."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*50, f"\nMódulo de Previsão de Risco Cardíaco\n", "="*50, sep="")
    
    modelo, scaler, df, X_encoded, y = (
        RECURSOS_CARREGADOS["modelo"], RECURSOS_CARREGADOS["scaler"], RECURSOS_CARREGADOS["df"],
        RECURSOS_CARREGADOS["X_encoded"], RECURSOS_CARREGADOS["y"]
    )
    
    try:
        idx = int(input(f"Digite o índice do paciente para prever (0 a {len(df)-1}): "))
        if not (0 <= idx < len(df)):
            print("Índice inválido."); return
    except ValueError:
        print("Entrada inválida."); return
        
    paciente_a_prever, _ = X_encoded.align(pd.DataFrame(columns=scaler.get_feature_names_out()), axis=1, fill_value=0)
    paciente_a_prever = paciente_a_prever.iloc[[idx]]
    paciente_scaled = scaler.transform(paciente_a_prever)
    
    previsao, probabilidade = modelo.predict(paciente_scaled)[0], modelo.predict_proba(paciente_scaled)[0]
    
    print("\n--- Relatório de Risco para o Paciente de Índice {} ---".format(idx))
    resultado_previsto = "ALTO RISCO" if previsao == 1 else "Baixo Risco"
    confianca = probabilidade[previsao]
    print(f"Previsão do Modelo: {resultado_previsto} (Confiança: {confianca:.2%})")
    print("\n--- Dados do Paciente Original ---")
    print(RECURSOS_CARREGADOS['df'].iloc[idx])
    
    print("\n--- Verificação da Previsão ---")
    y_real = y.iloc[idx]
    resultado_real = "ALTO RISCO" if y_real == 1 else "Baixo Risco"
    print(f"Valor Real no Dataset: {resultado_real}")
    if previsao == y_real: print("✅ O modelo ACERTOU a previsão.")
    else: print("❌ O modelo ERROU a previsão.")

def main():
    """Função principal que gerencia o menu e o loop do programa."""
    os.system('cls' if os.name == 'nt' else 'clear')
    if not carregar_recursos():
        input("Pressione Enter para sair."); sys.exit(1)
    sistemas = inicializar_sistemas()
    if sistemas is None: input("Pressione Enter para sair."); sys.exit(1)

    nomes_sistemas = list(sistemas.keys())
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        mostrar_menu_principal(sistemas)
        try:
            escolha_str = input("Digite o número da sua escolha: ")
            if not escolha_str: continue
            escolha = int(escolha_str)
            
            num_estruturas = len(sistemas)
            if 1 <= escolha <= num_estruturas:
                nome_escolhido = nomes_sistemas[escolha - 1]
                instancia_escolhida = sistemas[nome_escolhido]
                gerenciar_estrutura_principal(nome_escolhido, instancia_escolhida)
            elif escolha == num_estruturas + 1:
                executar_previsao_paciente()
                input("\nPressione Enter para voltar ao menu principal...")
            elif escolha == num_estruturas + 2:
                print("Saindo do sistema. Até logo!"); break
            else:
                print("Opção inválida."); time.sleep(1)
        except ValueError:
            print("Entrada inválida. Por favor, digite um número."); time.sleep(1)

if __name__ == "__main__":
    main()