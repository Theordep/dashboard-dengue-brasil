import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET() {
    try {
        const filePath = path.join(process.cwd(), 'public', 'data', 'dengue_statistics.json');
        const fileContents = fs.readFileSync(filePath, 'utf8');
        const data = JSON.parse(fileContents);

        const scData = data.santa_catarina || {};

        return NextResponse.json({
            total_casos: scData.total_casos || 0,
            municipios_afetados: scData.municipios_afetados || 0,
            municipios: scData.municipios || {},
            criciuma: scData.criciuma || {},
            analise: {
                tem_dados: (scData.total_casos || 0) > 0,
                criciuma_identificada: (scData.criciuma?.casos || 0) > 0,
                recomendacao: scData.total_casos > 0
                    ? 'Dados disponíveis para análise detalhada'
                    : 'Necessário obter mais dados históricos'
            }
        });
    } catch (error) {
        return NextResponse.json(
            { error: 'Erro ao buscar dados de SC' },
            { status: 500 }
        );
    }
}

