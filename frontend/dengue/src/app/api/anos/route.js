import { NextResponse } from 'next/server';
import { readJsonFile } from '@/lib/fileReader';

export async function GET() {
    try {
        const data = readJsonFile('dengue_statistics.json');

        const anosData = data.por_ano || {};

        return NextResponse.json({
            anos: anosData.anos || [],
            casos: anosData.casos || [],
            total_anos: anosData.anos?.length || 0
        });
    } catch (error) {
        return NextResponse.json(
            { error: 'Erro ao buscar dados por ano' },
            { status: 500 }
        );
    }
}

