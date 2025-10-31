'use client';

import { useState, useEffect } from 'react';
import Layout from '@/components/layout/Layout';
import { apiService } from '@/services/api';
import GraficoFaixaEtaria from '@/components/charts/GraficoFaixaEtaria';
import GraficoGenero from '@/components/charts/GraficoGenero';
import GraficoSintomasPerfil from '@/components/charts/GraficoSintomasPerfil';
import { GraficoMunicipiosSC, GraficoCrescimentoSC } from '@/components/charts/GraficoSCAvancado';
import { translateSymptom } from '@/lib/translateSymptoms';

export default function AnaliseAvancada() {
    const [faixasEtariasData, setFaixasEtariasData] = useState(null);
    const [generoData, setGeneroData] = useState(null);
    const [sintomasPerfilData, setSintomasPerfilData] = useState(null);
    const [santaCatarinaData, setSantaCatarinaData] = useState(null);
    const [faixaSelecionada, setFaixaSelecionada] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadData = async () => {
            try {
                setLoading(true);
                setError(null);

                // Carregar dados de faixas etárias
                try {
                    const response = await apiService.getFaixasEtarias();
                    setFaixasEtariasData(response.data);
                    console.log('Dados de faixas etárias carregados com sucesso!');
                } catch (err) {
                    console.error('Erro ao carregar dados de faixas etárias:', err);
                }

                // Carregar dados de gênero
                try {
                    const response = await apiService.getGeneroDetalhado();
                    setGeneroData(response.data);
                    console.log('Dados de gênero carregados com sucesso!');
                } catch (err) {
                    console.error('Erro ao carregar dados de gênero:', err);
                }

                // Carregar dados de sintomas por perfil
                try {
                    const response = await apiService.getSintomasPorPerfil();
                    setSintomasPerfilData(response.data);
                    console.log('Dados de sintomas por perfil carregados com sucesso!', response.data);
                } catch (err) {
                    console.error('Erro ao carregar dados de sintomas por perfil:', err);
                }

                // Carregar dados avançados de Santa Catarina
                try {
                    const response = await apiService.getSantaCatarinaAvancado();
                    setSantaCatarinaData(response.data);
                    console.log('Dados avançados de Santa Catarina carregados com sucesso!');
                } catch (err) {
                    console.error('Erro ao carregar dados avançados de Santa Catarina:', err);
                }

            } catch (err) {
                console.error('Erro ao carregar dados avançados:', err);
                setError('Erro ao carregar dados avançados. Verifique se o processador avançado foi executado.');
            } finally {
                setLoading(false);
            }
        };

        loadData();
    }, []);

    // Atualizar faixa selecionada quando os dados forem carregados
    useEffect(() => {
        if (sintomasPerfilData && sintomasPerfilData.por_faixa_etaria) {
            const faixasDisponiveis = Object.keys(sintomasPerfilData.por_faixa_etaria);
            if (faixasDisponiveis.length > 0) {
                // Se não tem faixa selecionada OU a faixa selecionada não existe mais
                setFaixaSelecionada(prev => {
                    if (!prev || !faixasDisponiveis.includes(prev)) {
                        return faixasDisponiveis[0];
                    }
                    return prev;
                });
            }
        }
    }, [sintomasPerfilData]);

    const handleCarregarEstatisticasAvancadas = async () => {
        try {
            setLoading(true);
            const response = await apiService.loadAdvancedStatistics();
            console.log('Estatísticas avançadas carregadas:', response.data);

            // Recarregar dados
            window.location.reload();
        } catch (err) {
            console.error('Erro ao carregar estatísticas avançadas:', err);
            setError('Erro ao carregar estatísticas avançadas. Verifique se o arquivo JSON existe.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Layout>
            <div className="w-full">
                <h1 className="text-xl sm:text-2xl md:text-3xl font-bold mb-4 sm:mb-6">Análise Avançada de Dados</h1>

                {/* Botão para carregar estatísticas avançadas */}
                <div className="mb-6">
                    <button
                        onClick={handleCarregarEstatisticasAvancadas}
                        className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 sm:px-6 rounded-md transition-colors text-sm sm:text-base"
                    >
                        Carregar Estatísticas Avançadas
                    </button>
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
                        <p className="mt-4 text-gray-700">Carregando dados avançados...</p>
                    </div>
                )}

                {/* Conteúdo principal */}
                {!loading && !error && (
                    <>
                        {/* Seção 1: Análise Demográfica */}
                        <div className="mb-8">
                            <h2 className="text-xl font-bold mb-4 text-gray-800">📊 Análise Demográfica</h2>

                            {/* Faixas Etárias */}
                            <div className="bg-white rounded-lg shadow-md p-4 mb-6">
                                <h3 className="text-lg font-semibold mb-3">Análise por Faixa Etária</h3>

                                {faixasEtariasData ? (
                                    <>
                                        <div className="h-80 mb-4">
                                            <GraficoFaixaEtaria data={faixasEtariasData} />
                                        </div>

                                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
                                            <div className="bg-blue-50 p-3 rounded-lg border border-blue-200">
                                                <p className="text-sm text-gray-600">Faixa mais afetada</p>
                                                <p className="text-lg font-bold text-blue-700">
                                                    {faixasEtariasData.destaques?.faixa_mais_afetada || 'N/A'}
                                                </p>
                                            </div>

                                            <div className="bg-red-50 p-3 rounded-lg border border-red-200">
                                                <p className="text-sm text-gray-600">Maior letalidade</p>
                                                <p className="text-lg font-bold text-red-700">
                                                    {faixasEtariasData.destaques?.faixa_maior_letalidade || 'N/A'}
                                                </p>
                                            </div>

                                            <div className="bg-amber-50 p-3 rounded-lg border border-amber-200">
                                                <p className="text-sm text-gray-600">Casos em grupos de risco</p>
                                                <p className="text-lg font-bold text-amber-700">
                                                    {((faixasEtariasData.destaques?.total_casos_criancas || 0) +
                                                        (faixasEtariasData.destaques?.total_casos_idosos || 0)).toLocaleString('pt-BR')}
                                                </p>
                                            </div>
                                        </div>
                                    </>
                                ) : (
                                    <p className="text-gray-500 italic">Dados de faixas etárias não disponíveis</p>
                                )}
                            </div>

                            {/* Análise de Gênero */}
                            <div className="bg-white rounded-lg shadow-md p-4">
                                <h3 className="text-lg font-semibold mb-3">Análise por Gênero</h3>

                                {generoData ? (
                                    <>
                                        <div className="h-80 mb-4">
                                            <GraficoGenero data={generoData} />
                                        </div>

                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                                            <div className="bg-purple-50 p-3 rounded-lg border border-purple-200">
                                                <p className="text-sm text-gray-600">Faixa com maior diferença entre gêneros</p>
                                                <p className="text-lg font-bold text-purple-700">
                                                    {generoData.destaques?.faixa_maior_diferenca || 'N/A'}
                                                </p>
                                            </div>

                                            <div className="bg-green-50 p-3 rounded-lg border border-green-200">
                                                <p className="text-sm text-gray-600">Sintoma com maior diferença entre gêneros</p>
                                                <p className="text-lg font-bold text-green-700">
                                                    {generoData.destaques?.sintoma_maior_diferenca || 'N/A'}
                                                </p>
                                            </div>
                                        </div>
                                    </>
                                ) : (
                                    <p className="text-gray-500 italic">Dados de gênero não disponíveis</p>
                                )}
                            </div>
                        </div>

                        {/* Seção 2: Análise Clínica */}
                        <div className="mb-8">
                            <h2 className="text-xl font-bold mb-4 text-gray-800">🩺 Análise Clínica</h2>

                            {/* Sintomas por Perfil */}
                            <div className="bg-white rounded-lg shadow-md p-4">
                                <h3 className="text-lg font-semibold mb-3">Sintomas por Faixa Etária</h3>

                                {sintomasPerfilData && sintomasPerfilData.por_faixa_etaria ? (
                                    <>
                                        <div className="mb-4">
                                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                                Selecione a faixa etária:
                                            </label>
                                            <select
                                                className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                                                value={faixaSelecionada || ''}
                                                onChange={(e) => setFaixaSelecionada(e.target.value)}
                                            >
                                                {Object.keys(sintomasPerfilData.por_faixa_etaria).length > 0 ? (
                                                    Object.keys(sintomasPerfilData.por_faixa_etaria).map(faixa => (
                                                        <option key={faixa} value={faixa}>
                                                            {faixa} anos
                                                        </option>
                                                    ))
                                                ) : (
                                                    <option value="">Nenhuma faixa disponível</option>
                                                )}
                                            </select>
                                        </div>

                                        <div className="h-80 mb-4">
                                            <GraficoSintomasPerfil
                                                data={sintomasPerfilData}
                                                faixaEtaria={faixaSelecionada}
                                            />
                                        </div>

                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                                            <div className="bg-blue-50 p-3 rounded-lg border border-blue-200">
                                                <p className="text-sm text-gray-600">Sintoma mais comum em crianças</p>
                                                <p className="text-lg font-bold text-blue-700">
                                                    {sintomasPerfilData.destaques?.sintoma_mais_comum_criancas
                                                        ? translateSymptom(sintomasPerfilData.destaques.sintoma_mais_comum_criancas)
                                                        : 'N/A'}
                                                </p>
                                            </div>

                                            <div className="bg-amber-50 p-3 rounded-lg border border-amber-200">
                                                <p className="text-sm text-gray-600">Sintoma mais comum em idosos</p>
                                                <p className="text-lg font-bold text-amber-700">
                                                    {sintomasPerfilData.destaques?.sintoma_mais_comum_idosos
                                                        ? translateSymptom(sintomasPerfilData.destaques.sintoma_mais_comum_idosos)
                                                        : 'N/A'}
                                                </p>
                                            </div>
                                        </div>

                                        <div className="mt-6">
                                            <h4 className="text-md font-semibold mb-2">Combinações de Sintomas Mais Comuns</h4>
                                            {sintomasPerfilData.combinacoes_mais_comuns && sintomasPerfilData.combinacoes_mais_comuns.length > 0 ? (
                                                <ul className="space-y-2">
                                                    {sintomasPerfilData.combinacoes_mais_comuns.map((combinacao, index) => (
                                                        <li key={index} className="bg-gray-50 p-2 rounded border border-gray-200">
                                                            <span className="font-medium">
                                                                {combinacao.sintomas?.map(s => translateSymptom(s)).join(' + ') || 'N/A'}
                                                            </span>
                                                            <span className="text-sm text-gray-600 ml-2">
                                                                ({combinacao.percentual !== undefined && combinacao.percentual !== null
                                                                    ? combinacao.percentual.toFixed(2)
                                                                    : '0.00'}% dos casos)
                                                            </span>
                                                        </li>
                                                    ))}
                                                </ul>
                                            ) : (
                                                <p className="text-gray-500 italic">Nenhuma combinação disponível</p>
                                            )}
                                        </div>
                                    </>
                                ) : (
                                    <p className="text-gray-500 italic">Dados de sintomas por perfil não disponíveis</p>
                                )}
                            </div>
                        </div>

                        {/* Seção 3: Santa Catarina Avançado */}
                        <div className="mb-8">
                            <h2 className="text-xl font-bold mb-4 text-gray-800">🗺️ Santa Catarina - Análise Detalhada</h2>

                            {/* Municípios */}
                            <div className="bg-white rounded-lg shadow-md p-4 mb-6">
                                <h3 className="text-lg font-semibold mb-3">Top 10 Municípios</h3>

                                {santaCatarinaData ? (
                                    <>
                                        <div className="h-80 mb-4">
                                            <GraficoMunicipiosSC data={santaCatarinaData} />
                                        </div>

                                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
                                            <div className="bg-blue-50 p-3 rounded-lg border border-blue-200">
                                                <p className="text-sm text-gray-600">Município com mais casos</p>
                                                <p className="text-lg font-bold text-blue-700">
                                                    {santaCatarinaData.destaques?.municipio_mais_casos || 'N/A'}
                                                </p>
                                            </div>

                                            <div className="bg-green-50 p-3 rounded-lg border border-green-200">
                                                <p className="text-sm text-gray-600">% do total nacional</p>
                                                <p className="text-lg font-bold text-green-700">
                                                    {santaCatarinaData.destaques?.percentual_do_total_nacional
                                                        ? santaCatarinaData.destaques.percentual_do_total_nacional.toFixed(2)
                                                        : '0.00'}%
                                                </p>
                                            </div>

                                            <div className="bg-purple-50 p-3 rounded-lg border border-purple-200">
                                                <p className="text-sm text-gray-600">Incidência vs. nacional</p>
                                                <p className="text-lg font-bold text-purple-700">
                                                    {santaCatarinaData.destaques?.incidencia_vs_nacional
                                                        ? santaCatarinaData.destaques.incidencia_vs_nacional.toFixed(2)
                                                        : '0.00'}x
                                                </p>
                                            </div>
                                        </div>
                                    </>
                                ) : (
                                    <p className="text-gray-500 italic">Dados de municípios não disponíveis</p>
                                )}
                            </div>

                            {/* Análise Temporal */}
                            <div className="bg-white rounded-lg shadow-md p-4">
                                <h3 className="text-lg font-semibold mb-3">Análise Temporal</h3>

                                {santaCatarinaData && santaCatarinaData.analise_temporal ? (
                                    <>
                                        <div className="h-80 mb-4">
                                            <GraficoCrescimentoSC data={santaCatarinaData} />
                                        </div>

                                        <div className="bg-amber-50 p-3 rounded-lg border border-amber-200 mt-4">
                                            <p className="text-sm text-gray-600">Maior crescimento mensal</p>
                                            <p className="text-lg font-bold text-amber-700">
                                                {santaCatarinaData.destaques?.maior_crescimento_mensal !== undefined
                                                    ? santaCatarinaData.destaques.maior_crescimento_mensal.toFixed(2)
                                                    : '0.00'}%
                                            </p>
                                        </div>
                                    </>
                                ) : (
                                    <p className="text-gray-500 italic">Dados de análise temporal não disponíveis</p>
                                )}
                            </div>
                        </div>
                    </>
                )}
            </div>
        </Layout>
    );
}
