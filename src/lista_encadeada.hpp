#ifndef LISTA_ENCADEADA_HPP
#define LISTA_ENCADEADA_HPP

#include "csv_loader.hpp"

// Estrutura de um nó da lista
struct No {
    Paciente dado;
    No* proximo;

    No(const Paciente& paciente) : dado(paciente), proximo(nullptr) {}
};

// Classe da lista encadeada
class ListaEncadeada {
private:
    No* cabeca;

public:
    ListaEncadeada();
    ~ListaEncadeada();

    void inserir(const Paciente& paciente);
    bool removerPorId(int id);
    Paciente* buscarPorId(int id);
    void imprimirLista() const;
    int tamanho() const;

    // Getter para acessar o primeiro nó (cabeca)
    No* getCabeca() const;
};

#endif