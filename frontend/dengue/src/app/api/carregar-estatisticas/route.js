import { NextResponse } from 'next/server';

// Rota POST para compatibilidade - em produção os dados já estão carregados
export async function POST() {
    return NextResponse.json({
        message: 'Estatísticas já disponíveis. Dados carregados de arquivos estáticos.',
        total_registros: 1502259,
        created: false
    });
}

