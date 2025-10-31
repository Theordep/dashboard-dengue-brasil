import { NextResponse } from 'next/server';
import { readJsonFile } from '@/lib/fileReader';

export async function GET() {
    try {
        const data = readJsonFile('dengue_advanced_statistics.json');

        const faixasData = data.faixa_etaria || {};
        const ordem_faixas = ['0-4', '5-14', '15-29', '30-44', '45-59', '60+'];

        const faixas = [];
        const casos = [];
        const obitos = [];
        const letalidade = [];
        const percentuais = [];

        for (const faixa of ordem_faixas) {
            if (faixa in faixasData) {
                faixas.push(faixa);
                casos.push(faixasData[faixa].casos || 0);
                obitos.push(faixasData[faixa].obitos || 0);
                letalidade.push(faixasData[faixa].letalidade || 0);
                percentuais.push(faixasData[faixa].percentual_do_total || 0);
            }
        }

        return NextResponse.json({
            faixas,
            casos,
            obitos,
            letalidade,
            percentuais,
            destaques: {
                faixa_mais_afetada: faixas.length > 0 ? faixas[casos.indexOf(Math.max(...casos))] : null,
                faixa_maior_letalidade: faixas.length > 0 ? faixas[letalidade.indexOf(Math.max(...letalidade))] : null,
                total_casos_criancas: faixasData['0-4']?.casos || 0,
                total_casos_idosos: faixasData['60+']?.casos || 0
            }
        });
    } catch (error) {
        return NextResponse.json(
            { error: 'Erro ao buscar dados de faixas etárias' },
            { status: 500 }
        );
    }
}

