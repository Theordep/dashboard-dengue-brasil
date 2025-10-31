import fs from 'fs';
import path from 'path';

/**
 * Função auxiliar para ler arquivos JSON de forma robusta
 * Funciona tanto em desenvolvimento quanto no Vercel
 * 
 * IMPORTANTE: No Vercel, arquivos em public/ não podem ser lidos com fs.
 * Esta função tenta ler de src/data/ primeiro (que funciona no Vercel),
 * e depois tenta public/data/ como fallback (para desenvolvimento local).
 */
export function readJsonFile(filename) {
    const possiblePaths = [
        // Primeiro, tentar src/data/ (funciona no Vercel)
        path.join(process.cwd(), 'src', 'data', filename),
        path.resolve(process.cwd(), 'src', 'data', filename),
        // Fallback para public/data/ (desenvolvimento local)
        path.join(process.cwd(), 'public', 'data', filename),
        path.resolve(process.cwd(), 'public', 'data', filename),
        // Outros caminhos possíveis
        path.join(process.cwd(), 'src', 'app', 'public', 'data', filename),
        path.join(process.cwd(), filename),
    ];

    for (const filePath of possiblePaths) {
        try {
            if (fs.existsSync(filePath)) {
                const fileContents = fs.readFileSync(filePath, 'utf8');
                return JSON.parse(fileContents);
            }
        } catch (error) {
            // Continua tentando outros caminhos
            continue;
        }
    }

    // Se nenhum caminho funcionou, lança erro com mensagem mais informativa
    throw new Error(
        `Arquivo ${filename} não encontrado. Tentou os seguintes caminhos:\n${possiblePaths.join('\n')}\n\n` +
        `Certifique-se de que o arquivo existe em src/data/ ou public/data/`
    );
}

