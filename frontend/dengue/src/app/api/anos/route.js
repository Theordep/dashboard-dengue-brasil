import { NextResponse } from 'next/server';
import data from '@/data/dengue_statistics.json';

export async function GET() {
    try {

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

