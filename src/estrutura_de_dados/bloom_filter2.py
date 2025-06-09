# src/data_structures/counting_bloom_filter.py
import hashlib
import sys

class CountingBloomFilter:
    """
    Implementação de um Counting Bloom Filter.
    Permite inserções, remoções e buscas probabilísticas com baixo consumo de memória.
    Pode gerar falsos positivos, mas nunca falsos negativos.
    """
    def __init__(self, size=100000, hash_count=5):
        if size <= 0 or hash_count <= 0:
            raise ValueError("Tamanho e contagem de hash devem ser maiores que zero.")
        self.size = size
        self.hash_count = hash_count
        self.count_array = [0] * size

    def _hashes(self, item):
        """Gera 'hash_count' valores de hash para um item."""
        # Garante que o item seja uma string para consistência no encoding
        item_str = str(item)
        item_bytes = item_str.encode('utf-8')
        
        for i in range(self.hash_count):
            # Gera um hash diferente para cada iteração 'i'
            hasher = hashlib.sha256(item_bytes + str(i).encode('utf-8'))
            yield int(hasher.hexdigest(), 16) % self.size

    def insert(self, item):
        """Insere um item no filtro, incrementando os contadores."""
        for idx in self._hashes(item):
            self.count_array[idx] += 1

    def remove(self, item):
        """Remove um item do filtro, decrementando os contadores."""
        # Antes de decrementar, verifica se o item provavelmente existe
        # para evitar que os contadores fiquem negativos se remover algo que não foi inserido.
        if self.search(item):
            for idx in self._hashes(item):
                if self.count_array[idx] > 0:
                    self.count_array[idx] -= 1

    def search(self, item):
        """
        Verifica se um item PODE estar no filtro.
        Retorna False se o item definitivamente não está.
        Retorna True se o item PODE estar (risco de falso positivo).
        """
        return all(self.count_array[idx] > 0 for idx in self._hashes(item))

    def get_memory_usage(self):
        """Retorna o uso de memória estimado do array do filtro em bytes."""
        return sys.getsizeof(self.count_array)