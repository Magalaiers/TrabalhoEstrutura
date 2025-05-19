#include "csv_loader.hpp"
#include <iostream>
#include <fstream>
#include <sstream>

void Paciente::imprimePaciente() const {
    std::cout << "ID: " << id
              << ", Idade: " << idade
              << ", Sexo: " << sexo
              << ", Colesterol: " << colesterol
              << ", Pressão: " << pressao_sistolica << "/" << pressao_diastolica
              << ", Freq. Cardíaca: " << frequencia_cardiaca
              << ", Diabetes: " << diabetes
              << ", Histórico Familiar: " << historico_familiar
              << ", Fumante: " << fumante
              << ", Obeso: " << obeso
              << ", Álcool: " << alcool
              << ", Exercício (h/sem): " << horas_exercicio_semana
              << ", Dieta: " << dieta
              << ", Problemas cardíacos anteriores: " << problemas_cardiacos_anteriores
              << ", Medicamento: " << uso_medicamento
              << ", Estresse: " << nivel_estresse
              << ", Sedentarismo (h/dia): " << horas_sedentarias_dia
              << ", Renda: " << renda
              << ", IMC: " << imc
              << ", Triglicerídeos: " << triglicerideos
              << ", Atividade física (dias/sem): " << dias_atividade_fisica_semana
              << ", Sono (h/dia): " << horas_sono_dia
              << ", País: " << pais
              << ", Continente: " << continente
              << ", Hemisfério: " << hemisferio
              << ", Risco de ataque cardíaco: " << risco_ataque
              << "\n";
}

int carregar_csv(const std::string& nome_arquivo, std::vector<Paciente>& pacientes) {
    std::ifstream arquivo(nome_arquivo);
    if (!arquivo.is_open()) {
        std::cerr << "Erro ao abrir arquivo: " << nome_arquivo << "\n";
        return -1;
    }

    std::string linha;
    std::getline(arquivo, linha); // pular cabeçalho
    int id_contador = 1;

    while (std::getline(arquivo, linha)) {
        std::stringstream ss(linha);
        std::string campo;
        Paciente p;

        try {
            std::getline(ss, campo, ','); // Patient ID (ignorar)

            std::getline(ss, campo, ','); p.idade = std::stoi(campo);
            std::getline(ss, campo, ','); p.sexo = campo;
            std::getline(ss, campo, ','); p.colesterol = std::stoi(campo);

            std::getline(ss, campo, ','); // Blood Pressure (ex: 158/88)
            std::stringstream bp(campo);
            std::string sistolica, diastolica;
            std::getline(bp, sistolica, '/');
            std::getline(bp, diastolica);
            p.pressao_sistolica = std::stoi(sistolica);
            p.pressao_diastolica = std::stoi(diastolica);

            std::getline(ss, campo, ','); p.frequencia_cardiaca = std::stoi(campo);
            std::getline(ss, campo, ','); p.diabetes = std::stoi(campo);
            std::getline(ss, campo, ','); p.historico_familiar = std::stoi(campo);
            std::getline(ss, campo, ','); p.fumante = std::stoi(campo);
            std::getline(ss, campo, ','); p.obeso = std::stoi(campo);
            std::getline(ss, campo, ','); p.alcool = std::stoi(campo);
            std::getline(ss, campo, ','); p.horas_exercicio_semana = std::stof(campo);
            std::getline(ss, campo, ','); p.dieta = campo;
            std::getline(ss, campo, ','); p.problemas_cardiacos_anteriores = std::stoi(campo);
            std::getline(ss, campo, ','); p.uso_medicamento = std::stoi(campo);
            std::getline(ss, campo, ','); p.nivel_estresse = std::stoi(campo);
            std::getline(ss, campo, ','); p.horas_sedentarias_dia = std::stof(campo);
            std::getline(ss, campo, ','); p.renda = std::stof(campo);
            std::getline(ss, campo, ','); p.imc = std::stof(campo);
            std::getline(ss, campo, ','); p.triglicerideos = std::stof(campo);
            std::getline(ss, campo, ','); p.dias_atividade_fisica_semana = std::stoi(campo);
            std::getline(ss, campo, ','); p.horas_sono_dia = std::stof(campo);
            std::getline(ss, campo, ','); p.pais = campo;
            std::getline(ss, campo, ','); p.continente = campo;
            std::getline(ss, campo, ','); p.hemisferio = campo;
            std::getline(ss, campo, ','); p.risco_ataque = std::stoi(campo);

        } catch (const std::exception& e) {
            std::cerr << "Erro ao processar linha:\n" << linha << "\nMotivo: " << e.what() << "\n";
            continue;
        }

        p.id = id_contador++;
        pacientes.push_back(p);
    }

    return pacientes.size();
}
