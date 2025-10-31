import { NextResponse } from 'next/server';

export async function GET() {
    return NextResponse.json({
        name: 'Dengue Dashboard API',
        version: '1.0.0',
        description: 'API para análise de dados de dengue do DATASUS',
        endpoints: {
            dashboard_overview: '/api/dashboard',
            estatisticas_por_estado: '/api/estados',
            estatisticas_por_ano: '/api/anos',
            sintomas_mais_comuns: '/api/sintomas',
            santa_catarina_detalhes: '/api/santa-catarina',
            health_check: '/api/health'
        }
    });
}

