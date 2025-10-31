import { NextResponse } from 'next/server';
import data from '@/data/dengue_statistics.json';
import { translateSymptom } from '@/lib/translateSymptoms';

export async function GET() {
    try {

        const sintomasData = data.sintomas || {};
        const sintomas_lista = [];

        for (const [sintoma, dados] of Object.entries(sintomasData)) {
            sintomas_lista.push({
                nome: translateSymptom(sintoma.toUpperCase()),
                casos: dados.casos || 0,
                percentual: dados.percentual || 0
            });
        }

        sintomas_lista.sort((a, b) => b.casos - a.casos);

        return NextResponse.json({
            sintomas: sintomas_lista,
            total_sintomas: sintomas_lista.length
        });
    } catch (error) {
        return NextResponse.json(
            { error: 'Erro ao buscar sintomas' },
            { status: 500 }
        );
    }
}

