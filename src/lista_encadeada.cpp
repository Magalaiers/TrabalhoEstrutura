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

void ListaEncadeada::inserir(const Paciente& paciente) {
    No* novo = new No(paciente);
    novo->proximo = cabeca;
    cabeca = novo;
}

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

void ListaEncadeada::imprimirLista() const {
    No* atual = cabeca;
    while (atual) {
        atual->dado.imprimePaciente();
        atual = atual->proximo;
    }
}

int ListaEncadeada::tamanho() const {
    int cont = 0;
    No* atual = cabeca;
    while (atual) {
        cont++;
        atual = atual->proximo;
    }
    return cont;
}

No* ListaEncadeada::getCabeca() const {
    return cabeca;
}
