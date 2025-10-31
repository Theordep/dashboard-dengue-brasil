import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET() {
    try {
        const filePath = path.join(process.cwd(), 'public', 'data', 'dengue_statistics.json');
        const fileContents = fs.readFileSync(filePath, 'utf8');
        const data = JSON.parse(fileContents);

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

