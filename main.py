# main.py
import os
import sys
import time
import pandas as pd
import numpy as np
import joblib
import warnings
import matplotlib.pyplot as plt
import seaborn as sns

# --- Início da Seção de Compatibilidade para o Executável ---

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

# --- Fim da Seção de Compatibilidade ---


# Ignora avisos para uma saída mais limpa no console
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Adiciona a raiz do projeto ao path para encontrar o 'src' (necessário para rodar como script)
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# --- Imports das suas Estruturas de Dados ---
try:
    from src.estrutura_de_dados.lista_encadeada import LinkedList
    from src.estrutura_de_dados.lista_encadeada_otimizada import LinkedListOptimized
    from src.estrutura_de_dados.tabela_hash import HashTable
    from src.estrutura_de_dados.arvore_avl import AVLTree
    # Adicione aqui os imports das estruturas do seu colega quando estiverem prontas
    # Ex: from src.data_structures.skip_list import SkipList 
except ImportError as e:
    print(f"--- ERRO CRÍTICO ---")
    print(f"Erro ao importar estruturas: {e}")
    print("Verifique se os arquivos e classes existem nos caminhos corretos dentro de 'src/'.")
    input("Pressione Enter para sair.")
    sys.exit(1)


# --- Cache para evitar recarregar arquivos pesados ---
RECURSOS_CARREGADOS = {
    "df": None,
    "modelo": None,
    "scaler": None,
    "X_encoded": None,
    "y": None
}

def carregar_recursos():
    """Carrega o DataFrame, o modelo e o scaler uma única vez."""
    print("Verificando e carregando recursos necessários...")
    try:
        if RECURSOS_CARREGADOS["df"] is None:
            path_df = resource_path("dataset/heart_attack_prediction_dataset.csv")
            df = pd.read_csv(path_df)
            if 'Patient ID' in df.columns:
                df = df.drop('Patient ID', axis=1)
            RECURSOS_CARREGADOS["df"] = df
        
        if RECURSOS_CARREGADOS["modelo"] is None:
            path_modelo = resource_path('models/melhor_modelo_otimizado.joblib')
            path_scaler = resource_path('models/scaler.joblib')
            RECURSOS_CARREGADOS["modelo"] = joblib.load(path_modelo)
            RECURSOS_CARREGADOS["scaler"] = joblib.load(path_scaler)
        
        # Prepara X e y para serem usados por outras funções
        if RECURSOS_CARREGADOS["X_encoded"] is None:
            df = RECURSOS_CARREGADOS["df"]
            X = df.drop('Heart Attack Risk', axis=1)
            y = df['Heart Attack Risk']
            RECURSOS_CARREGADOS["X_encoded"] = pd.get_dummies(X, drop_first=True)
            RECURSOS_CARREGADOS["y"] = y

    except FileNotFoundError as e:
        print(f"\n--- ERRO CRÍTICO ---")
        print(f"Arquivo não encontrado: {e.filename}")
        print("Certifique-se de que as pastas 'data' e 'models' estão no mesmo diretório que o executável.")
        print("Se estiver rodando pela primeira vez, execute o notebook de ML para gerar os arquivos de modelo.")
        return False
            
    print("✅ Recursos prontos.")
    return True

def mostrar_menu():
    """Exibe o menu principal de opções."""
    print("\n" + "="*50)
    print("   Sistema de Análise de Estruturas de Dados")
    print("="*50)
    print("1. Análise Estatística do Dataset")
    print("2. Executar Benchmark Geral de Estruturas")
    print("3. Comparar Otimização da Lista Encadeada")
    print("4. Previsão de Risco Cardíaco para um Paciente")
    print("5. Sair")
    print("="*50)

def executar_analise_estatistica():
    """Opção 1: Mostra estatísticas descritivas e um histograma."""
    df = RECURSOS_CARREGADOS['df']
    print("\n--- Estatísticas Descritivas (Colunas Numéricas) ---")
    print(df.describe().T) 

    colunas_numericas = df.select_dtypes(include=np.number).columns.tolist()
    print("\n--- Visualização da Distribuição de uma Feature ---")
    for i, col in enumerate(colunas_numericas):
        print(f"  {i+1}. {col}")
    
    try:
        escolha = int(input("\nDigite o número da feature para ver seu histograma: ")) - 1
        if 0 <= escolha < len(colunas_numericas):
            coluna = colunas_numericas[escolha]
            plt.figure(figsize=(10, 6))
            sns.histplot(df[coluna], kde=True, bins=30)
            plt.title(f'Distribuição de "{coluna}"', fontsize=16)
            plt.show()
    except (ValueError, IndexError):
        print("Opção inválida.")

def executar_benchmarks():
    """Opção 2: Roda benchmarks de inserção e busca."""
    df = RECURSOS_CARREGADOS['df']
    try:
        n_itens = int(input("Digite o número de itens para o benchmark (ex: 3000): "))
        if not (0 < n_itens <= len(df)):
            print(f"Número inválido. Deve ser entre 1 e {len(df)}.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    dados_teste = df['Age'].head(n_itens)
    item_busca = dados_teste.iloc[-1]
    estruturas = {"Lista Encadeada": LinkedList(), "Tabela Hash": HashTable(size=n_itens*2), "Árvore AVL": AVLTree()}
    resultados = []
    
    for nome, estrutura in estruturas.items():
        print(f"\n--- Benchmark para: {nome} ---")
        start = time.perf_counter()
        if isinstance(estrutura, HashTable):
            for i, item in enumerate(dados_teste): estrutura.insert(key=i, value=item)
        else:
            for item in dados_teste: estrutura.insert(item)
        t_insert = time.perf_counter() - start
        
        start = time.perf_counter()
        if isinstance(estrutura, HashTable): estrutura.search(key=n_itens - 1)
        else: estrutura.search(item_busca)
        t_search = time.perf_counter() - start
        
        resultados.append({"Estrutura": nome, "Inserção (s)": t_insert, "Busca (s)": t_search})

    df_resultados = pd.DataFrame(resultados).set_index('Estrutura')
    print("\n--- Tabela de Resultados do Benchmark ---")
    print(df_resultados.round(6))

def executar_comparacao_otimizacao():
    """Opção 3: Compara a inserção na LinkedList original vs otimizada."""
    try:
        n_itens = int(input("Digite o número de itens para o teste (ex: 10000): "))
    except ValueError:
        print("Entrada inválida.")
        return
    
    lista_original, lista_otimizada = LinkedList(), LinkedListOptimized()
    start = time.perf_counter()
    for i in range(n_itens): lista_original.insert(i)
    t_original = time.perf_counter() - start
    
    start = time.perf_counter()
    for i in range(n_itens): lista_otimizada.insert(i)
    t_otimizada = time.perf_counter() - start

    print("\n--- Comparativo de Inserção na Lista Encadeada ---")
    print(f"Tempo da versão Original (O(n²)): {t_original:.4f}s")
    print(f"Tempo da versão Otimizada (O(n)): {t_otimizada:.4f}s")
    if t_otimizada > 0:
        print(f"Ganho de performance: {t_original / t_otimizada:.2f} vezes mais rápido!")

def executar_previsao_paciente():
    """Opção 4: Usa o modelo de ML para prever o risco de um paciente."""
    modelo, scaler = RECURSOS_CARREGADOS["modelo"], RECURSOS_CARREGADOS["scaler"]
    df, X_encoded = RECURSOS_CARREGADOS["df"], RECURSOS_CARREGADOS["X_encoded"]

    try:
        idx = int(input(f"Digite o índice do paciente para prever (0 a {len(df)-1}): "))
        if not (0 <= idx < len(df)):
            print("Índice inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return
        
    paciente_encoded = X_encoded.iloc[[idx]]
    paciente_scaled = scaler.transform(paciente_encoded)
    previsao, probabilidade = modelo.predict(paciente_scaled)[0], modelo.predict_proba(paciente_scaled)[0]
    
    print("\n--- Relatório de Risco para o Paciente de Índice {} ---".format(idx))
    resultado = "ALTO RISCO" if previsao == 1 else "Baixo Risco"
    confianca = probabilidade[previsao]
    print(f"Previsão: {resultado} (Confiança: {confianca:.2%})")
    print("\n--- Dados do Paciente ---")
    print(df.iloc[idx])

def main():
    """Função principal que gerencia o menu e o loop do programa."""
    if not carregar_recursos():
        input("Pressione Enter para sair.")
        sys.exit(1)
        
    while True:
        mostrar_menu()
        escolha = input("Digite o número da sua escolha: ")

        if escolha == '1':
            executar_analise_estatistica()
        elif escolha == '2':
            executar_benchmarks()
        elif escolha == '3':
            executar_comparacao_otimizacao()
        elif escolha == '4':
            executar_previsao_paciente()
        elif escolha == '5':
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")
        
        input("\nPressione Enter para voltar ao menu...")
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()