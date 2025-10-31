import { NextResponse } from 'next/server';
import { readJsonFile } from '@/lib/fileReader';

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
        const data = readJsonFile('dengue_advanced_statistics.json');

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
                percentual_do_total_nacional: scData.comparacao_nacional?.percentual_do_total || 0,
                incidencia_vs_nacional: scData.comparacao_nacional?.razao_incidencia || 0,
                maior_crescimento_mensal: (() => {
                    const crescimento = scData.analise_temporal?.crescimento_percentual;
                    if (!crescimento || !Array.isArray(crescimento)) return 0;
                    const numeros = crescimento.filter(v => typeof v === 'number' && !isNaN(v));
                    return numeros.length > 0 ? Math.max(...numeros) : 0;
                })()
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

