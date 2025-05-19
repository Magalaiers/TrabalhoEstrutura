#include <iostream>
#include <vector>
#include <filesystem>
#include "csv_loader.hpp"

int main() {
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

    return 0;
}
