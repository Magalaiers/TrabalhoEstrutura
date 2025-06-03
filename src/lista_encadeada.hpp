#ifndef LISTA_ENCADEADA_HPP
#define LISTA_ENCADEADA_HPP

#include "csv_loader.hpp"

// Estrutura de nó da lista encadeada
struct No {
    Paciente dado;
    No* proximo;

    No(const Paciente& p) : dado(p), proximo(nullptr) {}
};

class ListaEncadeada {
private:
    No* cabeca;

public:
    ListaEncadeada();
    ~ListaEncadeada();

    void inserir(const Paciente& paciente); // Insere no fim da lista
    void inserirNoFim(const Paciente& paciente); // Versão explícita para inserção no fim
    bool removerPorId(int id);
    Paciente* buscarPorId(int id);
    void imprimirLista() const;
    int tamanho() const;
    No* getCabeca() const;
};

#endif
