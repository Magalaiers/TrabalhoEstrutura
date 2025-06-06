# src/data_structures/hash_table.py

class HashTable:
    """
    Implementação de uma Tabela Hash com encadeamento para resolver colisões.
    """
    def __init__(self, size=1000):
        """
        Inicializa a tabela hash.
        :param size: O número de "baldes" (buckets) na tabela. Um número primo maior é geralmente uma boa escolha.
        """
        self.size = size
        self.table = [[] for _ in range(self.size)]  # Cria uma lista de listas vazias (nossos baldes)

    def _hash_function(self, key):
        """
        Calcula o índice para uma determinada chave.
        Usa a função hash nativa do Python e o operador de módulo.
        """
        return hash(key) % self.size

    def insert(self, key, value):
        """
        Insere um par chave-valor na tabela hash.
        Se a chave já existir, atualiza o valor.
        """
        index = self._hash_function(key)
        bucket = self.table[index]

        # Verifica se a chave já existe no balde para evitar duplicatas e permitir atualização
        for i, (existing_key, existing_value) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)  # Atualiza o valor se a chave for a mesma
                return
        
        # Se a chave não existe, adiciona o novo par chave-valor ao balde
        bucket.append((key, value))

    def search(self, key):
        """
        Busca um valor pela sua chave.
        Retorna o valor se a chave for encontrada, ou None caso contrário.
        """
        index = self._hash_function(key)
        bucket = self.table[index]

        # Procura a chave dentro do balde
        for existing_key, value in bucket:
            if existing_key == key:
                return value  # Retorna o valor associado à chave
        
        return None  # Retorna None se a chave não for encontrada

    def remove(self, key):
        """
        Remove um par chave-valor da tabela usando a chave.
        """
        index = self._hash_function(key)
        bucket = self.table[index]

        # Procura pela chave no balde e a remove se encontrar
        for i, (existing_key, value) in enumerate(bucket):
            if existing_key == key:
                del bucket[i]  # Remove o par (chave, valor) da lista do balde
                return