'use client';

import { useState, useEffect } from 'react';
import Layout from '@/components/layout/Layout';
import EstatisticasGerais from '@/components/dashboard/EstatisticasGerais';
import GraficoEstados from '@/components/charts/GraficoEstados';
import GraficoSintomas from '@/components/charts/GraficoSintomas';
import GraficoAnos from '@/components/charts/GraficoAnos';
import ApiStatus from '@/components/dashboard/ApiStatus';
import { apiService } from '@/services/api';

export default function Home() {
  const [data, setData] = useState(null);
  const [anosData, setAnosData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        setError(null);

        console.log('Tentando carregar dados do dashboard...');

        // Buscar dados do dashboard diretamente
        const dashboardData = await apiService.getDashboardData();
        setData(dashboardData.data);
        console.log('Dados do dashboard carregados com sucesso!');

        // Buscar dados de anos separadamente
        try {
          const anosResponse = await apiService.getAnosData();
          setAnosData(anosResponse.data);
          console.log('Dados de anos carregados com sucesso!');
        } catch (anosError) {
          console.error('Erro ao carregar dados de anos:', anosError);
          // Não definimos erro aqui para não interromper o carregamento do dashboard
        }

      } catch (err) {
        console.error('Erro ao carregar dados:', err);

        if (err.response?.status === 404) {
          // Se não encontrar dados, tentar carregar estatísticas
          console.log('Dados não encontrados, tentando carregar estatísticas...');
          try {
            const response = await apiService.loadStatistics();
            console.log('Estatísticas carregadas:', response.data);

            // Depois de carregar estatísticas, buscar dados do dashboard novamente
            const dashboardData = await apiService.getDashboardData();
            setData(dashboardData.data);
            console.log('Dados do dashboard carregados após carregar estatísticas!');

            // Buscar dados de anos novamente
            try {
              const anosResponse = await apiService.getAnosData();
              setAnosData(anosResponse.data);
              console.log('Dados de anos carregados com sucesso!');
            } catch (anosError) {
              console.error('Erro ao carregar dados de anos após estatísticas:', anosError);
            }
          } catch (loadError) {
            setError('Erro ao carregar estatísticas. Verifique se o arquivo dengue_statistics.json existe.');
          }
        } else if (err.response?.status === 405) {
          setError('Erro de método HTTP. Verifique se o backend está configurado corretamente.');
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
        {/* Status da API */}
        <div className="mb-8 sm:mb-10">
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
            <p className="mt-4 text-gray-700">Carregando dados de dengue...</p>
          </div>
        )}

        {/* Conteúdo principal */}
        {!loading && !error && data && (
          <>
            {/* Estatísticas Gerais */}
            <div className="mb-8 sm:mb-10">
              <EstatisticasGerais data={data.geral} />
            </div>

            {/* Seção Principal - Casos por Estado */}
            <div className="mb-10 sm:mb-12">
              <div className="bg-white rounded-lg shadow-md p-3 sm:p-4 md:p-6 overflow-hidden">
                <h2 className="text-lg sm:text-xl font-bold mb-4 text-gray-800 flex items-center">
                  <span className="mr-2">📊</span> Distribuição Nacional de Casos
                </h2>
                <div className="h-64 sm:h-80 md:h-96 w-full overflow-hidden">
                  <GraficoEstados data={data.por_estado} />
                </div>
              </div>
            </div>

            {/* Seção Análises Detalhadas */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 sm:gap-10 lg:gap-8 mb-10 sm:mb-12 md:mb-14">
              {/* Sintomas Mais Comuns */}
              <div className="bg-white rounded-lg shadow-md p-3 sm:p-4 md:p-6 overflow-hidden">
                <h2 className="text-lg sm:text-xl font-bold mb-4 text-gray-800 flex items-center">
                  <span className="mr-2">🦠</span> Sintomas Mais Comuns
                </h2>
                <div className="h-64 sm:h-72 md:h-80 w-full overflow-hidden">
                  <GraficoSintomas data={data.sintomas} />
                </div>
              </div>

              {/* Evolução Temporal */}
              <div className="bg-white rounded-lg shadow-md p-3 sm:p-4 md:p-6 overflow-hidden">
                <h2 className="text-lg sm:text-xl font-bold mb-4 text-gray-800 flex items-center">
                  <span className="mr-2">📈</span> Evolução Temporal
                </h2>
                <div className="h-64 sm:h-72 md:h-80 w-full overflow-hidden">
                  <GraficoAnos data={anosData} />
                </div>
              </div>
            </div>

            {/* Informações do Dataset */}
            <div className="bg-gray-50 rounded-lg shadow-md p-4 sm:p-6 mt-8 sm:mt-10">
              <h2 className="text-base sm:text-lg font-medium text-gray-800 mb-4 flex items-center">
                <span className="mr-2">📋</span> Informações do Dataset
              </h2>
              <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4">
                <div className="text-center p-4">
                  <p className="text-lg font-bold text-blue-600">DATASUS</p>
                  <p className="text-sm text-gray-600">Fonte dos dados</p>
                </div>
                <div className="text-center p-4">
                  <p className="text-lg font-bold text-blue-600">
                    {data.geral?.total_casos?.toLocaleString('pt-BR') || 'N/A'}
                  </p>
                  <p className="text-sm text-gray-600">Total de registros</p>
                </div>
                <div className="text-center p-4">
                  <p className="text-lg font-bold text-blue-600">
                    {data.geral?.estados_unicos || 'N/A'}
                  </p>
                  <p className="text-sm text-gray-600">Estados brasileiros</p>
                </div>
                <div className="text-center p-4">
                  <p className="text-lg font-bold text-blue-600">
                    {data.geral?.anos_disponiveis?.join('-') || 'N/A'}
                  </p>
                  <p className="text-sm text-gray-600">Período analisado</p>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </Layout>
  );
}