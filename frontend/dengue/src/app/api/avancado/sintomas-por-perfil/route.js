import { NextResponse } from 'next/server';
import { readJsonFile } from '@/lib/fileReader';

export async function GET() {
    try {
        const data = readJsonFile('dengue_advanced_statistics.json');

        const sintomasPerfil = data.sintomas_por_perfil || {};
        const por_faixa = sintomasPerfil.por_faixa_etaria || {};

        // Encontrar sintoma mais comum por faixa
        const sintoma_mais_comum_por_faixa = {};
        for (const [faixa, sintomas] of Object.entries(por_faixa)) {
            let maxPercentual = 0;
            let sintomaMax = null;

            for (const [sintoma, valores] of Object.entries(sintomas)) {
                const percentual = valores?.percentual || 0;
                if (percentual > maxPercentual) {
                    maxPercentual = percentual;
                    sintomaMax = sintoma;
                }
            }

            if (sintomaMax) {
                sintoma_mais_comum_por_faixa[faixa] = {
                    sintoma: sintomaMax,
                    percentual: maxPercentual
                };
            }
        }

        // Função auxiliar para extrair o primeiro número de uma faixa etária
        const getFirstNumber = (faixa) => {
            const match = faixa.match(/^(\d+)/);
            return match ? parseInt(match[1]) : Infinity;
        };

        // Encontrar a faixa mais próxima para crianças (menor número inicial)
        const faixasDisponiveis = Object.keys(por_faixa);
        let faixaCriancas = '0-4';
        let faixaIdosos = '60+';

        // Se não existir '0-4', buscar a faixa com menor número inicial
        if (!sintoma_mais_comum_por_faixa['0-4'] && faixasDisponiveis.length > 0) {
            const faixaOrdenada = faixasDisponiveis.sort((a, b) => getFirstNumber(a) - getFirstNumber(b));
            faixaCriancas = faixaOrdenada[0];
        }

        // Se não existir '60+', buscar a faixa com maior número inicial
        if (!sintoma_mais_comum_por_faixa['60+'] && faixasDisponiveis.length > 0) {
            const faixaOrdenada = faixasDisponiveis.sort((a, b) => {
                const numA = a.includes('+') ? Infinity : getFirstNumber(a);
                const numB = b.includes('+') ? Infinity : getFirstNumber(b);
                return numB - numA;
            });
            faixaIdosos = faixaOrdenada[0];
        }

        return NextResponse.json({
            por_faixa_etaria: por_faixa,
            combinacoes_mais_comuns: sintomasPerfil.combinacoes_mais_comuns || [],
            sintoma_mais_comum_por_faixa: sintoma_mais_comum_por_faixa,
            destaques: {
                sintoma_mais_comum_criancas: sintoma_mais_comum_por_faixa[faixaCriancas]?.sintoma || 'N/A',
                sintoma_mais_comum_idosos: sintoma_mais_comum_por_faixa[faixaIdosos]?.sintoma || 'N/A',
                combinacao_mais_comum: sintomasPerfil.combinacoes_mais_comuns?.[0]?.sintomas || []
            }
        });
    } catch (error) {
        return NextResponse.json(
            { error: 'Erro ao buscar dados de sintomas por perfil' },
            { status: 500 }
        );
    }
}

