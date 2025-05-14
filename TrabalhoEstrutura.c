#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINHA 512
#define MAX_STR 50
#define TAM_INICIAL 10000

typedef struct {
    int age;
    int cholesterol;
    int heart_rate;
    char diabetes[MAX_STR];
    char family_history[MAX_STR];
    char smoking[MAX_STR];
    char obesity[MAX_STR];
    char alcohol_consumption[MAX_STR];
    int exercise_hours_per_week;
    char diet[MAX_STR];
    char previous_heart_problems[MAX_STR];
    char medication_use[MAX_STR];
    char stress_level[MAX_STR];
    int sedentary_hours_per_day;
    int income;
    float bmi;
    int triglycerides;
    int physical_activity_days;
    int sleep_hours_per_day;
    int heart_attack_risk_binary;
    float blood_sugar;
    float ck_mb;
    float troponin;
    char heart_attack_risk_text[MAX_STR];
    char gender[MAX_STR];
    int systolic_bp;
    int diastolic_bp;
} RegistroPaciente;

int main() {
    FILE *arquivo = fopen("dataset.csv", "r");
    if (arquivo == NULL) {
        perror("Erro ao abrir o arquivo");
        return 1;
    }

    char linha[MAX_LINHA];
    fgets(linha, sizeof(linha), arquivo); // Ignora o cabeçalho

    int capacidade = TAM_INICIAL;
    int total = 0;
    RegistroPaciente *dados = malloc(capacidade * sizeof(RegistroPaciente));
    if (dados == NULL) {
        perror("Erro de alocação");
        fclose(arquivo);
        return 1;
    }

    while (fgets(linha, sizeof(linha), arquivo)) {
        if (total >= capacidade) {
            capacidade *= 2;
            RegistroPaciente *tmp = realloc(dados, capacidade * sizeof(RegistroPaciente));
            if (tmp == NULL) {
                perror("Erro ao realocar");
                free(dados);
                fclose(arquivo);
                return 1;
            }
            dados = tmp;
        }

        RegistroPaciente *p = &dados[total];
        linha[strcspn(linha, "\n")] = '\0'; // remove newline

        sscanf(linha, "%d,%d,%d,%49[^,],%49[^,],%49[^,],%49[^,],%49[^,],%d,%49[^,],%49[^,],%49[^,],%49[^,],%d,%d,%f,%d,%d,%d,%d,%f,%f,%f,%49[^,],%49[^,],%d,%d",
               &p->age, &p->cholesterol, &p->heart_rate, p->diabetes, p->family_history,
               p->smoking, p->obesity, p->alcohol_consumption, &p->exercise_hours_per_week,
               p->diet, p->previous_heart_problems, p->medication_use, p->stress_level,
               &p->sedentary_hours_per_day, &p->income, &p->bmi, &p->triglycerides,
               &p->physical_activity_days, &p->sleep_hours_per_day,
               &p->heart_attack_risk_binary, &p->blood_sugar, &p->ck_mb, &p->troponin,
               p->heart_attack_risk_text, p->gender, &p->systolic_bp, &p->diastolic_bp);

        total++;
    }

    fclose(arquivo);

    printf("Leituras carregadas: %d\n", total);
    for (int i = 0; i < 5 && i < total; i++) {
        printf("Paciente %d: Idade %d, Colesterol %d, IMC %.2f, Risco (Bin): %d, Risco (Texto): %s\n",
               i + 1,
               dados[i].age,
               dados[i].cholesterol,
               dados[i].bmi,
               dados[i].heart_attack_risk_binary,
               dados[i].heart_attack_risk_text);
    }

    free(dados);
    return 0;
}
