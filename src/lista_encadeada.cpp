#include "lista_encadeada.hpp"
#include <iostream>

ListaEncadeada::ListaEncadeada() : cabeca(nullptr) {}

ListaEncadeada::~ListaEncadeada() {
    No* atual = cabeca;
    while (atual) {
        No* temp = atual;
        atual = atual->proximo;
        delete temp;
    }
}

// Insere no fim da lista
void ListaEncadeada::inserir(const Paciente& paciente) {
    inserirNoFim(paciente);
}

// Inserção explícita no final da lista encadeada
void ListaEncadeada::inserirNoFim(const Paciente& paciente) {
    No* novo = new No(paciente);  // cria novo nó com o paciente

    if (cabeca == nullptr) {
        cabeca = novo;
    } else {
        No* atual = cabeca;
        while (atual->proximo != nullptr) {
            atual = atual->proximo;
        }
        atual->proximo = novo;
    }
}


// Remove um nó com base no ID do paciente
bool ListaEncadeada::removerPorId(int id) {
    No* atual = cabeca;
    No* anterior = nullptr;

    while (atual) {
        if (atual->dado.id == id) {
            if (anterior) {
                anterior->proximo = atual->proximo;
            } else {
                cabeca = atual->proximo;
            }
            delete atual;
            return true;
        }
        anterior = atual;
        atual = atual->proximo;
    }
    return false;
}

// Busca um paciente pelo ID
Paciente* ListaEncadeada::buscarPorId(int id) {
    No* atual = cabeca;
    while (atual) {
        if (atual->dado.id == id) {
            return &atual->dado;
        }
        atual = atual->proximo;
    }
    return nullptr;
}

// Imprime todos os pacientes da lista
void ListaEncadeada::imprimirLista() const {
    No* atual = cabeca;
    while (atual) {
        atual->dado.imprimePaciente();
        atual = atual->proximo;
    }
}

// Retorna o tamanho da lista
int ListaEncadeada::tamanho() const {
    int cont = 0;
    No* atual = cabeca;
    while (atual) {
        cont++;
        atual = atual->proximo;
    }
    return cont;
}

// Retorna o ponteiro para a cabeça da lista
No* ListaEncadeada::getCabeca() const {
    return cabeca;
}
