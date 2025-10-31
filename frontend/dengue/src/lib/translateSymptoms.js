/**
 * Traduz termos médicos para termos mais compreensíveis para o público geral
 */
export function translateSymptom(sintoma) {
    const traducoes = {
        'mialgia': 'Dor Muscular',
        'MIALGIA': 'DOR MUSCULAR',
        'cefaleia': 'Dor de Cabeça',
        'CEFALEIA': 'DOR DE CABEÇA',
        'exantema': 'Manchas na Pele',
        'EXANTEMA': 'MANCHAS NA PELE',
        'febre': 'Febre',
        'FEBRE': 'FEBRE',
        'vomito': 'Vômito',
        'VOMITO': 'VÔMITO',
        'nausea': 'Náusea',
        'NAUSEA': 'NÁUSEA',
    };

    // Retorna a tradução se existir, caso contrário retorna o termo original capitalizado
    if (traducoes[sintoma]) {
        return traducoes[sintoma];
    }

    // Se não encontrar tradução exata, tenta encontrar em lowercase
    const lowerSintoma = sintoma.toLowerCase();
    if (traducoes[lowerSintoma]) {
        // Preserva o formato original (maiúsculas/minúsculas)
        if (sintoma === sintoma.toUpperCase()) {
            return traducoes[lowerSintoma].toUpperCase();
        }
        return traducoes[lowerSintoma];
    }

    // Se não encontrar tradução, capitaliza a primeira letra
    return sintoma.charAt(0).toUpperCase() + sintoma.slice(1).toLowerCase();
}

