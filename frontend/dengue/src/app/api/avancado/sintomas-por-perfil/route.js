import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET() {
    try {
        const filePath = path.join(process.cwd(), 'public', 'data', 'dengue_advanced_statistics.json');
        const fileContents = fs.readFileSync(filePath, 'utf8');
        const data = JSON.parse(fileContents);

        const sintomasPerfil = data.sintomas_por_perfil || {};

        return NextResponse.json({
            por_faixa_etaria: sintomasPerfil.por_faixa_etaria || {},
            combinacoes_mais_comuns: sintomasPerfil.combinacoes_mais_comuns || [],
            sintoma_mais_comum_por_faixa: {},
            destaques: {
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

