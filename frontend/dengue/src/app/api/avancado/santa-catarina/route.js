import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

const nomes_municipios = {
    '420540': 'Florianópolis',
    '420820': 'Joinville',
    '420200': 'Blumenau',
    '420420': 'Balneário Camboriú',
    '420910': 'Lages',
    '420830': 'Jaraguá do Sul',
    '421660': 'São José',
    '421720': 'São Miguel do Oeste',
    '420240': 'Brusque',
    '420890': 'Itajaí',
    '420460': 'Criciúma'
};

export async function GET() {
    try {
        const filePath = path.join(process.cwd(), 'public', 'data', 'dengue_advanced_statistics.json');
        const fileContents = fs.readFileSync(filePath, 'utf8');
        const data = JSON.parse(fileContents);

        const scData = data.santa_catarina || {};
        const municipios_data = scData.municipios || {};
        const codigos = municipios_data.codigos || [];
        const casos = municipios_data.casos || [];

        const nomes = codigos.map(codigo =>
            nomes_municipios[codigo] || `Município ${codigo}`
        );

        return NextResponse.json({
            total_casos: scData.total_casos || 0,
            municipios_afetados: scData.municipios_afetados || 0,
            municipios: {
                codigos,
                nomes,
                casos
            },
            analise_temporal: scData.analise_temporal || {},
            comparacao_nacional: scData.comparacao_nacional || {},
            destaques: {
                municipio_mais_casos: nomes[0] || null,
                percentual_do_total_nacional: scData.comparacao_nacional?.percentual_do_total || 0
            },
            criciuma: scData.criciuma || {}
        });
    } catch (error) {
        return NextResponse.json(
            { error: 'Erro ao buscar dados avançados de SC' },
            { status: 500 }
        );
    }
}

