#ifndef CSV_LOADER_HPP
#define CSV_LOADER_HPP

#include <string>
#include <vector>

struct Paciente {
    int id;
    int idade;
    std::string sexo;
    int colesterol;
    int pressao_sistolica;
    int pressao_diastolica;
    int frequencia_cardiaca;
    int diabetes;
    int historico_familiar;
    int fumante;
    int obeso;
    int alcool;
    float horas_exercicio_semana;
    std::string dieta;
    int problemas_cardiacos_anteriores;
    int uso_medicamento;
    int nivel_estresse;
    float horas_sedentarias_dia;
    float renda;
    float imc;
    float triglicerideos;
    int dias_atividade_fisica_semana;
    float horas_sono_dia;
    std::string pais;
    std::string continente;
    std::string hemisferio;
    int risco_ataque;

    void imprimePaciente() const;
};

int carregar_csv(const std::string& nome_arquivo, std::vector<Paciente>& pacientes);

#endif
