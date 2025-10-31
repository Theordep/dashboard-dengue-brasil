import fs from 'fs';
import path from 'path';

/**
 * Função auxiliar para ler arquivos JSON de forma robusta
 * Funciona tanto em desenvolvimento quanto no Vercel
 */
export function readJsonFile(filename) {
    const possiblePaths = [
        path.join(process.cwd(), 'public', 'data', filename),
        path.join(process.cwd(), 'src', 'app', 'public', 'data', filename),
        path.join(process.cwd(), filename),
        path.resolve(process.cwd(), 'public', 'data', filename),
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

    // Se nenhum caminho funcionou, lança erro
    throw new Error(
        `Arquivo ${filename} não encontrado. Tentou os seguintes caminhos:\n${possiblePaths.join('\n')}`
    );
}

