#include <iostream>
#include <vector>
#include <filesystem>
#include <windows.h>
#include "csv_loader.hpp"
#include "lista_encadeada.hpp"

int main() {
    SetConsoleOutputCP(CP_UTF8);
    std::string path = "dataset/heart_attack_prediction_dataset.csv";
    if (!std::filesystem::exists(path)) {
        std::cerr << "Arquivo NÃO encontrado: " << path << "\n";
        return 1;
    } else {
        std::cout << "Arquivo encontrado: " << path << "\n";
    }

    std::vector<Paciente> pacientes;
    int total = carregar_csv(path, pacientes);

    if (total < 0) {
        std::cerr << "Falha ao carregar o dataset.\n";
        return 1;
    }

    std::cout << "Total de pacientes carregados: " << total << "\n";

    int qtd_mostrar = 5;
    if (total < qtd_mostrar) qtd_mostrar = total;

    std::cout << "Mostrando os " << qtd_mostrar << " primeiros pacientes:\n";
    for (int i = 0; i < qtd_mostrar; ++i) {
        pacientes[i].imprimePaciente();
    }

    ListaEncadeada lista;
    for (const auto& p : pacientes) {
        lista.inserir(p);
    }

    std::cout << "Total de pacientes na lista: " << lista.tamanho() << "\n";

    std::cout << "\nMostrando os 5 primeiros pacientes da lista encadeada:\n";
    No* atual = lista.getCabeca();  // Correto!
    int mostrados = 0;
    while (atual && mostrados < 5) {
        atual->dado.imprimePaciente();
        atual = atual->proximo;
        mostrados++;
    }

    // Exemplo de busca por ID
    int id_busca = pacientes.back().id;
    Paciente* encontrado = lista.buscarPorId(id_busca);
    if (encontrado) {
        std::cout << "\nPaciente com ID " << id_busca << " encontrado:\n";
        encontrado->imprimePaciente();
    } else {
        std::cout << "\nPaciente com ID " << id_busca << " não encontrado.\n";
    }

    return 0;
}
