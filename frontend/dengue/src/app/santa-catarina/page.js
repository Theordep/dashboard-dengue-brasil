'use client';

import { useState, useEffect } from 'react';
import Layout from '@/components/layout/Layout';
import SantaCatarina from '@/components/dashboard/SantaCatarina';
import ApiStatus from '@/components/dashboard/ApiStatus';
import { apiService } from '@/services/api';

export default function SantaCatarinaPage() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadData = async () => {
            try {
                setLoading(true);
                setError(null);

                // Buscar dados específicos de Santa Catarina
                const scData = await apiService.getSantaCatarinaData();
                setData(scData.data);

            } catch (err) {
                console.error('Erro ao carregar dados de Santa Catarina:', err);

                if (err.response?.status === 404) {
                    setError('Dados de Santa Catarina não encontrados. Verifique se as estatísticas foram carregadas.');
                } else if (err.code === 'ERR_NETWORK') {
                    setError('Não foi possível conectar ao backend. Verifique se o servidor Django está rodando na porta 8000.');
                } else {
                    setError(`Erro ao carregar dados: ${err.message}`);
                }
            } finally {
                setLoading(false);
            }
        };

        loadData();
    }, []);

    return (
        <Layout>
            <div className="w-full">
                {/* Cabeçalho */}
                <div className="mb-6">
                    <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-4 sm:p-6 rounded-lg shadow-lg">
                        <h1 className="text-xl sm:text-2xl md:text-3xl font-bold mb-2">Santa Catarina - Análise Detalhada</h1>
                        <p className="text-sm sm:text-base text-blue-100">
                            Foco especial em dados epidemiológicos de Santa Catarina e Criciúma
                        </p>
                    </div>
                </div>

                {/* Status da API */}
                <div className="mb-6">
                    <ApiStatus />
                </div>

                {/* Mensagem de erro */}
                {error && (
                    <div className="mb-6">
                        <div className="bg-red-100 border-l-4 border-red-500 p-4 rounded-r-lg shadow-md">
                            <div className="flex">
                                <div className="flex-shrink-0">
                                    <svg className="h-5 w-5 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                </div>
                                <div className="ml-3">
                                    <p className="text-sm font-medium text-red-800">
                                        Erro ao carregar dados
                                    </p>
                                    <p className="text-sm text-red-700 mt-1">
                                        {error}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* Loading */}
                {loading && !error && (
                    <div className="flex flex-col items-center justify-center py-12">
                        <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                        <p className="mt-4 text-gray-700">Carregando dados de Santa Catarina...</p>
                    </div>
                )}

                {/* Conteúdo principal */}
                {!loading && !error && data && (
                    <div className="mb-8">
                        <SantaCatarina data={data} />
                    </div>
                )}

                {/* Informações adicionais */}
                <div className="bg-white rounded-lg shadow-md p-6 mb-8">
                    <h2 className="text-xl font-bold mb-4 text-gray-800 flex items-center">
                        <span className="mr-2">🔍</span> Sobre a Análise de Santa Catarina
                    </h2>

                    <div className="prose max-w-none">
                        <p>
                            Esta seção apresenta uma análise detalhada dos casos de dengue em Santa Catarina,
                            com foco especial na cidade de Criciúma. Os dados são provenientes do DATASUS e
                            foram processados para fornecer insights sobre a distribuição geográfica dos casos.
                        </p>

                        <h3>Metodologia</h3>
                        <p>
                            Os dados foram extraídos do arquivo DENGBR25.csv do DATASUS, que contém registros
                            de casos de dengue notificados no Brasil. A análise foi realizada utilizando Python,
                            com as bibliotecas Pandas e NumPy para processamento de dados.
                        </p>

                        <h3>Limitações</h3>
                        <p>
                            É importante notar que a análise por bairros em Criciúma ainda está em desenvolvimento,
                            necessitando de dados geográficos mais detalhados e séries históricas mais longas para
                            uma compreensão completa da dinâmica da doença na região.
                        </p>

                        <h3>Próximos Passos</h3>
                        <ul>
                            <li>Obtenção de dados históricos (2020-2023)</li>
                            <li>Integração com mapas de bairros de Criciúma</li>
                            <li>Correlação com dados climáticos</li>
                            <li>Análise de fatores socioeconômicos</li>
                        </ul>
                    </div>
                </div>
            </div>
        </Layout>
    );
}