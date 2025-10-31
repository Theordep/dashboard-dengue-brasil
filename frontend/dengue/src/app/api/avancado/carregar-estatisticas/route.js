import { NextResponse } from 'next/server';

// Rota POST para compatibilidade - em produção os dados já estão carregados
export async function POST() {
    return NextResponse.json({
        message: 'Estatísticas avançadas já disponíveis. Dados carregados de arquivos estáticos.',
        created: false
    });
}

