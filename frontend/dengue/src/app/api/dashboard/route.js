import { NextResponse } from 'next/server';
import { readJsonFile } from '@/lib/fileReader';

export async function GET() {
    try {
        const data = readJsonFile('dengue_statistics.json');

        // Preparar resposta no formato esperado
        const response = {
            geral: data.geral,
            por_estado: data.por_estado,
            demografico: data.demografico,
            sintomas: data.sintomas,
            santa_catarina: data.santa_catarina,
            metadata: data.metadata
        };

        return NextResponse.json(response);
    } catch (error) {
        return NextResponse.json(
            { error: 'Erro ao carregar dados do dashboard' },
            { status: 500 }
        );
    }
}

