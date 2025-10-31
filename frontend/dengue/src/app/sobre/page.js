import Layout from '@/components/layout/Layout';

export default function SobrePage() {
    return (
        <Layout>
            <div className="w-full">
                <div className="bg-white rounded-lg shadow-lg overflow-hidden">
                    {/* Cabeçalho */}
                    <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-4 sm:p-6">
                        <h1 className="text-xl sm:text-2xl md:text-3xl font-bold mb-2">Sobre o Projeto</h1>
                        <p className="text-sm sm:text-base text-blue-100">
                            Análise de Dados de Dengue - Projeto Python
                        </p>
                    </div>

                    {/* Conteúdo */}
                    <div className="p-4 sm:p-6 md:p-8">
                        <div className="prose max-w-none">
                            <h2>Objetivo</h2>
                            <p>
                                Demonstrar como a <strong>Engenharia de Software</strong>, <strong>Python</strong> e <strong>Estatística</strong> podem
                                ser aplicados para analisar dados de saúde pública, especificamente casos de dengue, com foco na cidade de <strong>Criciúma/SC</strong>.
                            </p>

                            <h2>Estrutura do Projeto</h2>
                            <div className="bg-gray-50 p-4 rounded-lg overflow-auto">
                                <pre className="text-sm">
                                    <code>
                                        {`ProjetoPythonDengue/
├── Documentos/
│   ├── DENGBR25.csv              # Dataset principal do DATASUS
│   ├── Briefing Dengue e Estatística Aplicada.pdf
│   └── dic_dados_dengue.pdf      # Dicionário de dados
├── analise_dengue_criciuma.py    # Script inicial
├── analise_dengue_melhorada.py   # Versão com tratamento de erros
├── analise_dengue_final.py       # Análise completa e robusta
├── backend/                      # API Django
├── frontend/                     # Interface Next.js
├── workshop_demo.py              # Demo para apresentação
├── script_criciuma_especifico.py # Script específico para Criciúma
└── requirements.txt              # Dependências Python`}
                                    </code>
                                </pre>
                            </div>

                            <h2>Resultados da Análise</h2>

                            <h3>Distribuição Geográfica</h3>
                            <ul>
                                <li><strong>Goiás (UF 52)</strong>: 26.178 casos (52.4%)</li>
                                <li><strong>Bahia (UF 29)</strong>: 6.684 casos (13.4%)</li>
                                <li><strong>Acre (UF 12)</strong>: 4.890 casos (9.8%)</li>
                                <li><strong>Santa Catarina (UF 42)</strong>: 25 casos</li>
                            </ul>

                            <h3>Perfil Demográfico</h3>
                            <ul>
                                <li><strong>Feminino</strong>: 55.2% dos casos</li>
                                <li><strong>Masculino</strong>: 44.7% dos casos</li>
                                <li><strong>Idade média</strong>: Variável (dados em formato específico)</li>
                            </ul>

                            <h3>Sintomas Mais Comuns</h3>
                            <ol>
                                <li><strong>Febre</strong>: 84.4% dos casos</li>
                                <li><strong>Cefaleia</strong>: 78.6% dos casos</li>
                                <li><strong>Mialgia</strong>: 76.1% dos casos</li>
                            </ol>

                            <h2>Situação de Criciúma</h2>

                            <h3>Status Atual</h3>
                            <ul>
                                <li><strong>Código IBGE</strong>: 4204608</li>
                                <li><strong>Casos em 2025</strong>: Não identificados na amostra analisada</li>
                                <li><strong>Necessário</strong>: Dados históricos e geográficos detalhados</li>
                            </ul>

                            <h3>Próximos Passos</h3>
                            <ol>
                                <li><strong>Obter dados completos</strong> do DATASUS</li>
                                <li><strong>Buscar dados históricos</strong> (2020-2024)</li>
                                <li><strong>Adquirir mapas de bairros</strong> de Criciúma</li>
                                <li><strong>Implementar análise geográfica</strong> detalhada</li>
                            </ol>

                            <h2>Tecnologias Utilizadas</h2>

                            <h3>Backend</h3>
                            <ul>
                                <li><strong>Python 3.13.7</strong>: Linguagem principal</li>
                                <li><strong>Pandas 2.3.2</strong>: Manipulação de dados</li>
                                <li><strong>NumPy 2.3.2</strong>: Computação numérica</li>
                                <li><strong>Django 5.2.7</strong>: Framework web</li>
                                <li><strong>Django REST Framework</strong>: API REST</li>
                            </ul>

                            <h3>Frontend</h3>
                            <ul>
                                <li><strong>Next.js 15.5.4</strong>: Framework React</li>
                                <li><strong>Tailwind CSS</strong>: Framework CSS</li>
                                <li><strong>Chart.js</strong>: Visualizações de dados</li>
                            </ul>

                            <h2>Contribuições Acadêmicas</h2>

                            <h3>Engenharia de Software</h3>
                            <ul>
                                <li><strong>Modularização</strong>: Código organizado em funções específicas</li>
                                <li><strong>Tratamento de erros</strong>: Robustez na manipulação de dados</li>
                                <li><strong>Documentação</strong>: Código bem documentado e comentado</li>
                                <li><strong>Escalabilidade</strong>: Preparado para datasets maiores</li>
                            </ul>

                            <h3>Estatística Aplicada</h3>
                            <ul>
                                <li><strong>Análise exploratória</strong>: Descoberta de padrões nos dados</li>
                                <li><strong>Estatísticas descritivas</strong>: Medidas de tendência central</li>
                                <li><strong>Análise temporal</strong>: Identificação de tendências</li>
                                <li><strong>Análise geográfica</strong>: Distribuição espacial</li>
                            </ul>
                        </div>
                    </div>

                    {/* Rodapé */}
                    <div className="bg-gray-50 px-6 py-4 border-t border-gray-200">
                        <p className="text-center text-gray-600">
                            Trabalho desenvolvido para a disciplina de <strong>Estatística Aplicada</strong> - Engenharia de Software
                        </p>
                        <p className="text-center text-gray-500 text-sm mt-1">
                            Última atualização: Outubro 2025
                        </p>
                    </div>
                </div>
            </div>
        </Layout>
    );
}