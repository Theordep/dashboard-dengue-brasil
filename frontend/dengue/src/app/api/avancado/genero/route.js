import { NextResponse } from 'next/server';
import { readJsonFile } from '@/lib/fileReader';

export async function GET() {
    try {
        const data = readJsonFile('dengue_advanced_statistics.json');

        const generoData = data.genero_detalhado || {};
        const distribuicao = generoData.distribuicao_por_faixa || {};
        const sintomas = generoData.sintomas_por_genero || {};

        // Calcular faixa com maior diferença entre gêneros
        let maior_diferenca = 0;
        let faixa_maior_diferenca = null;

        for (const [faixa, valores] of Object.entries(distribuicao)) {
            const feminino = valores?.feminino || 0;
            const masculino = valores?.masculino || 0;
            const diferenca = Math.abs(feminino - masculino);

            if (diferenca > maior_diferenca) {
                maior_diferenca = diferenca;
                faixa_maior_diferenca = faixa;
            }
        }

        // Calcular sintoma com maior diferença percentual entre gêneros
        let maior_dif_sintoma = 0;
        let sintoma_maior_diferenca = null;

        const sintomas_fem = sintomas.feminino || {};
        const sintomas_masc = sintomas.masculino || {};

        for (const sintoma in sintomas_fem) {
            if (sintoma in sintomas_masc) {
                const perc_fem = sintomas_fem[sintoma]?.percentual || 0;
                const perc_masc = sintomas_masc[sintoma]?.percentual || 0;
                const dif_sintoma = Math.abs(perc_fem - perc_masc);

                if (dif_sintoma > maior_dif_sintoma) {
                    maior_dif_sintoma = dif_sintoma;
                    sintoma_maior_diferenca = sintoma;
                }
            }
        }

        // Calcular diferença na letalidade
        const evolucao = generoData.evolucao_por_genero || {};
        const letalidade_fem = evolucao.feminino?.obito?.percentual || 0;
        const letalidade_masc = evolucao.masculino?.obito?.percentual || 0;

        return NextResponse.json({
            distribuicao_por_faixa: distribuicao,
            sintomas_por_genero: sintomas,
            evolucao_por_genero: evolucao,
            destaques: {
                faixa_maior_diferenca: faixa_maior_diferenca,
                sintoma_maior_diferenca: sintoma_maior_diferenca,
                letalidade: {
                    feminino: letalidade_fem,
                    masculino: letalidade_masc,
                    diferenca: Math.abs(letalidade_fem - letalidade_masc)
                }
            }
        });
    } catch (error) {
        return NextResponse.json(
            { error: 'Erro ao buscar dados de gênero' },
            { status: 500 }
        );
    }
}

