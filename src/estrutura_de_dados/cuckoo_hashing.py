# src/data_structures/cuckoo_hashing.py
import random
import hashlib
import sys

class CuckooHashing:
    """
    Implementação de Cuckoo Hashing com duas tabelas e duas funções de hash.
    Busca garantir acesso O(1) no pior caso.
    """
    def __init__(self, size):
        self.size = size
        self.table1 = [None] * size
        self.table2 = [None] * size
        self.rehash_count = 0

    def _hash1(self, key):
        # Usamos SHA256 para uma boa distribuição.
        key_bytes = str(key).encode('utf-8')
        return int(hashlib.sha256(key_bytes + b'salt1').hexdigest(), 16) % self.size

    def _hash2(self, key):
        key_bytes = str(key).encode('utf-8')
        return int(hashlib.sha256(key_bytes + b'salt2').hexdigest(), 16) % self.size

    def insert(self, key, value):
        """Insere um par chave-valor, lidando com colisões e rehashes."""
        max_kicks = self.size # Limite para evitar loops infinitos
        
        for _ in range(max_kicks):
            # Tenta inserir na Tabela 1
            idx1 = self._hash1(key)
            if self.table1[idx1] is None:
                self.table1[idx1] = (key, value)
                return True
            
            # Se colidiu, expulsa o antigo e tenta colocar na Tabela 2
            key, value, self.table1[idx1] = self.table1[idx1][0], self.table1[idx1][1], (key, value)
            
            # Tenta inserir o item expulso na Tabela 2
            idx2 = self._hash2(key)
            if self.table2[idx2] is None:
                self.table2[idx2] = (key, value)
                return True
                
            # Se colidiu de novo, expulsa e volta o loop para tentar na Tabela 1
            key, value, self.table2[idx2] = self.table2[idx2][0], self.table2[idx2][1], (key, value)

        # Se o loop terminou (muitos "kicks"), faz o rehash
        print(f"!!! Ciclo detectado. Realizando rehash... (Contagem: {self.rehash_count + 1})")
        self._rehash()
        # Tenta inserir o item original novamente após o rehash
        self.insert(key, value)
        return True

    def _rehash(self):
        """Dobra o tamanho das tabelas e reinsere todos os itens."""
        self.rehash_count += 1
        all_items = []
        for item in self.table1:
            if item: all_items.append(item)
        for item in self.table2:
            if item: all_items.append(item)
        
        # Dobra o tamanho
        self.size *= 2
        self.table1 = [None] * self.size
        self.table2 = [None] * self.size
        
        # Reinsere todos os itens
        for key, value in all_items:
            self.insert(key, value)

    def search(self, key):
        """Busca uma chave em ambas as tabelas."""
        idx1 = self._hash1(key)
        if self.table1[idx1] and self.table1[idx1][0] == key:
            return self.table1[idx1][1] # Retorna o valor

        idx2 = self._hash2(key)
        if self.table2[idx2] and self.table2[idx2][0] == key:
            return self.table2[idx2][1]

        return None

    def remove(self, key):
        """Remove uma chave de qualquer uma das tabelas."""
        idx1 = self._hash1(key)
        if self.table1[idx1] and self.table1[idx1][0] == key:
            self.table1[idx1] = None
            return True
        
        idx2 = self._hash2(key)
        if self.table2[idx2] and self.table2[idx2][0] == key:
            self.table2[idx2] = None
            return True
            
        return False
        
    def get_memory_usage(self):
        """Retorna o uso de memória estimado das tabelas."""
        return sys.getsizeof(self.table1) + sys.getsizeof(self.table2)