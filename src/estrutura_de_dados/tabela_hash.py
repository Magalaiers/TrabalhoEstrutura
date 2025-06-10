# src/data_structures/hash_table.py
import sys

class HashTable:
    """
    Implementação de uma Tabela Hash com encadeamento e contagem de colisões embutida.
    """
    def __init__(self, size=1000):
        self.size = size
        self.table = [[] for _ in range(self.size)]
        self.collision_count = 0  # Atributo de contagem inicializado aqui

    def _hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        """
        Insere um par chave-valor e incrementa o contador de colisões se necessário.
        """
        index = self._hash_function(key)
        bucket = self.table[index]

        # Verifica se a chave já existe (seria uma atualização, não uma nova colisão)
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)
                return

        # Se o balde já tem itens, é uma colisão para o novo item que será inserido.
        if len(bucket) > 0:
            self.collision_count += 1
        
        # Insere o novo par (chave, valor)
        bucket.append((key, value))

    def search(self, key):
        index = self._hash_function(key)
        bucket = self.table[index]
        for existing_key, value in bucket:
            if existing_key == key:
                return value
        return None

    def remove(self, key):
        index = self._hash_function(key)
        bucket = self.table[index]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                del bucket[i]
                return True
        return False

    def get_memory_usage(self):
        """Calcula o uso de memória estimado da tabela hash."""
        size = sys.getsizeof(self.table)
        for bucket in self.table:
            size += sys.getsizeof(bucket)
            for item in bucket:
                size += sys.getsizeof(item)
        return size