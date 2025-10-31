import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET() {
    try {
        const filePath = path.join(process.cwd(), 'public', 'data', 'dengue_advanced_statistics.json');
        const fileContents = fs.readFileSync(filePath, 'utf8');
        const data = JSON.parse(fileContents);

        const generoData = data.genero_detalhado || {};

        return NextResponse.json({
            distribuicao_por_faixa: generoData.distribuicao_por_faixa || {},
            sintomas_por_genero: generoData.sintomas_por_genero || {},
            evolucao_por_genero: generoData.evolucao_por_genero || {},
            destaques: {}
        });
    } catch (error) {
        return NextResponse.json(
            { error: 'Erro ao buscar dados de gênero' },
            { status: 500 }
        );
    }
}

