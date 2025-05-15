#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINHA 1024
#define MAX_AMOSTRAS 10000

typedef struct {
    int id;
    int idade;
    char sexo[10];
    int colesterol;
    int pressao;
    int freq_cardiaca;
    int diabetes;
    float imc;
    float risco_ataque;
} Paciente;

int carregar_csv(const char *arquivo, Paciente dados[], int max_amostras) {
    FILE *fp = fopen(arquivo, "r");
    if (!fp) {
        perror("Erro ao abrir o arquivo");
        return -1;
    }

    char linha[MAX_LINHA];
    int count = 0;

    // Ignorar cabeçalho
    fgets(linha, MAX_LINHA, fp);

    while (fgets(linha, MAX_LINHA, fp) && count < max_amostras) {
        char *token;
        int coluna = 0;
        token = strtok(linha, ",");
        Paciente p;

        while (token != NULL) {
            switch (coluna) {
                case 0: p.id = atoi(token); break;
                case 1: p.idade = atoi(token); break;
                case 2: strncpy(p.sexo, token, sizeof(p.sexo)); break;
                case 3: p.colesterol = atoi(token); break;
                case 4: p.pressao = atoi(token); break;
                case 5: p.freq_cardiaca = atoi(token); break;
                case 6: p.diabetes = atoi(token); break;
                case 18: p.imc = atof(token); break;
                case 26: p.risco_ataque = atof(token); break;
                default: break;
            }
            token = strtok(NULL, ",");
            coluna++;
        }

        dados[count++] = p;
    }

    fclose(fp);
    return count;
}

int main() {
    Paciente pacientes[MAX_AMOSTRAS];
    int total = carregar_csv("heart_attack_prediction_dataset.csv", pacientes, MAX_AMOSTRAS);

    if (total > 0) {
        printf("Leitura concluída: %d pacientes carregados.\n", total);
        for(int i=0;i<5;i++){    
            printf("Exemplo:\n");
            printf("ID: %d | Idade: %d | Sexo: %s | Colesterol: %d | Pressão: %d | FC: %d | Diabetes: %d | IMC: %.1f | Risco: %.2f\n",
                pacientes[i].id, pacientes[i].idade, pacientes[i].sexo,
                pacientes[i].colesterol, pacientes[i].pressao,
                pacientes[i].freq_cardiaca, pacientes[i].diabetes,
                pacientes[i].imc, pacientes[i].risco_ataque);
        }
    } else {
        printf("Nenhum paciente carregado.\n");
    }

    return 0;
}
