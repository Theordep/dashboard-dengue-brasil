'use client';

import { useState } from 'react';

// Mapear códigos de municípios para informações completas
const municipiosInfo = {
    '420540': {
        nome: 'Florianópolis',
        populacao: 508826,
        regiao: 'Grande Florianópolis',
        caracteristicas: ['Capital do Estado', 'Centro turístico', 'Ilha de Santa Catarina'],
        risco: 'Moderado - área turística com alta circulação'
    },
    '420820': {
        nome: 'Joinville',
        populacao: 597658,
        regiao: 'Norte do Estado',
        caracteristicas: ['Maior cidade de SC', 'Polo industrial', 'Festival de Dança'],
        risco: 'Alto - alta densidade populacional'
    },
    '420200': {
        nome: 'Blumenau',
        populacao: 366418,
        regiao: 'Vale do Itajaí',
        caracteristicas: ['Oktoberfest', 'Polo têxtil', 'Colonização alemã'],
        risco: 'Moderado - grande centro urbano'
    },
    '420420': {
        nome: 'Balneário Camboriú',
        populacao: 145796,
        regiao: 'Vale do Itajaí',
        caracteristicas: ['Destino turístico', 'Praia Central', 'Arranha-céus'],
        risco: 'Alto - grande fluxo turístico'
    },
    '420910': {
        nome: 'Lages',
        populacao: 157743,
        regiao: 'Serra Catarinense',
        caracteristicas: ['Maior cidade da Serra', 'Turismo rural', 'Festa do Pinhão'],
        risco: 'Baixo - clima mais frio'
    },
    '420830': {
        nome: 'Jaraguá do Sul',
        populacao: 184579,
        regiao: 'Norte do Estado',
        caracteristicas: ['Polo industrial', 'Colonização europeia', 'Economia diversificada'],
        risco: 'Moderado - área urbana em crescimento'
    },
    '421660': {
        nome: 'São José',
        populacao: 246204,
        regiao: 'Grande Florianópolis',
        caracteristicas: ['Região metropolitana', 'Área industrial', 'Próximo à capital'],
        risco: 'Moderado - região metropolitana'
    },
    '421720': {
        nome: 'São Miguel do Oeste',
        populacao: 40868,
        regiao: 'Extremo Oeste',
        caracteristicas: ['Fronteira com Argentina', 'Agronegócio', 'Comércio regional'],
        risco: 'Baixo - menor densidade populacional'
    },
    '420240': {
        nome: 'Brusque',
        populacao: 137689,
        regiao: 'Vale do Itajaí',
        caracteristicas: ['Polo têxtil', 'Colonização italiana e alemã', 'Cidade dos tecidos'],
        risco: 'Moderado - área industrial'
    },
    '420890': {
        nome: 'Itajaí',
        populacao: 223112,
        regiao: 'Vale do Itajaí',
        caracteristicas: ['Porto', 'Pesca', 'Logística'],
        risco: 'Alto - área portuária com grande circulação'
    },
    '420460': {
        nome: 'Criciúma',
        populacao: 217735,
        regiao: 'Sul do Estado',
        caracteristicas: ['Polo carbonífero', 'Centro regional', 'Universidades'],
        risco: 'Baixo - poucos casos identificados'
    }
};

export default function SantaCatarina({ data }) {
    const [selectedCity, setSelectedCity] = useState(null);

    if (!data) {
        return (
            <div className="p-4 bg-white rounded-lg shadow-md animate-pulse">
                <div className="h-8 bg-gray-200 rounded mb-4"></div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {[...Array(3)].map((_, i) => (
                        <div key={i} className="h-32 bg-gray-200 rounded"></div>
                    ))}
                </div>
            </div>
        );
    }

    const formatNumber = (num) => {
        return num ? num.toLocaleString('pt-BR') : '0';
    };

    const getStatusColor = (casos) => {
        if (casos === 0) return 'bg-gray-500';
        if (casos < 1000) return 'bg-green-500';
        if (casos < 10000) return 'bg-yellow-500';
        return 'bg-red-500';
    };

    const getStatusText = (casos) => {
        if (casos === 0) return 'Sem casos';
        if (casos < 1000) return 'Baixa incidência';
        if (casos < 10000) return 'Incidência moderada';
        return 'Alta incidência';
    };

    const getCidadesAfetadas = () => {
        if (!data.municipios || !data.municipios.codigos) return [];

        return data.municipios.codigos.map((codigo, index) => ({
            codigo,
            nome: municipiosInfo[codigo]?.nome || `Município ${codigo}`,
            casos: data.municipios.casos[index] || 0
        })).sort((a, b) => b.casos - a.casos);
    };

    const cidadesAfetadas = getCidadesAfetadas();
    const totalCasos = data.total_casos || 0;
    const percentualSC = totalCasos > 0 ? ((totalCasos / 1502259) * 100) : 0;

    const handleCityClick = (cidade) => {
        const cityInfo = municipiosInfo[cidade.codigo] || {
            nome: cidade.nome,
            populacao: 'Não disponível',
            regiao: 'Não disponível',
            caracteristicas: ['Informações em atualização'],
            risco: 'Análise em andamento'
        };

        setSelectedCity({
            ...cidade,
            ...cityInfo
        });
    };

    return (
        <div className="p-4 bg-white rounded-lg shadow-md">
            <h2 className="text-xl font-bold mb-4 text-gray-800 flex items-center">
                <span className="mr-2">🏖️</span> Santa Catarina - Análise Detalhada
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                {/* Total de Casos em SC */}
                <div className="bg-gradient-to-r from-blue-500 to-blue-700 text-white p-4 rounded-lg shadow-md">
                    <div className="flex flex-col items-center">
                        <h3 className="text-sm font-medium opacity-80">Santa Catarina</h3>
                        <p className="text-3xl font-bold mt-2">{formatNumber(totalCasos)}</p>
                        <p className="text-sm mt-1">casos de dengue</p>
                        <p className="text-xs opacity-80 mt-1">{percentualSC.toFixed(2)}% do total nacional</p>
                    </div>
                </div>

                {/* Municípios */}
                <div className="bg-white text-gray-800 p-4 rounded-lg shadow-md">
                    <div className="flex flex-col items-center">
                        <h3 className="text-sm font-medium text-blue-600">Municípios</h3>
                        <p className="text-3xl font-bold text-blue-600 mt-2">{data.municipios_afetados || 0}</p>
                        <p className="text-sm mt-1">municípios afetados</p>
                        <div className="mt-2">
                            <span className={`inline-block px-2 py-1 rounded-full text-xs text-white ${getStatusColor(totalCasos)}`}>
                                {getStatusText(totalCasos)}
                            </span>
                        </div>
                    </div>
                </div>

                {/* Ranking */}
                <div className="bg-white text-gray-800 p-4 rounded-lg shadow-md">
                    <div className="flex flex-col items-center">
                        <h3 className="text-sm font-medium text-purple-600">Ranking</h3>
                        <p className="text-3xl font-bold text-purple-600 mt-2">8º</p>
                        <p className="text-sm mt-1">posição nacional</p>
                        <p className="text-xs mt-1">entre os estados brasileiros</p>
                    </div>
                </div>
            </div>

            {/* Cidades mais afetadas */}
            {cidadesAfetadas.length > 0 && (
                <div className="mb-6 bg-white rounded-lg shadow-md overflow-hidden">
                    <div className="px-4 py-3 bg-gray-50 border-b border-gray-200">
                        <h3 className="text-lg font-medium text-gray-800 flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-blue-500" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                            </svg>
                            Cidades Mais Afetadas
                        </h3>
                    </div>

                    <div className="divide-y divide-gray-200">
                        {cidadesAfetadas.slice(0, 5).map((cidade, index) => {
                            const percentual = totalCasos > 0 ? (cidade.casos / totalCasos) * 100 : 0;

                            return (
                                <div
                                    key={cidade.codigo}
                                    className="px-4 py-3 hover:bg-gray-50 cursor-pointer transition-colors"
                                    onClick={() => handleCityClick(cidade)}
                                >
                                    <div className="flex items-center">
                                        <div className="flex-shrink-0">
                                            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white ${index < 3 ? 'bg-blue-500' : 'bg-blue-300'}`}>
                                                {index + 1}
                                            </div>
                                        </div>
                                        <div className="ml-4 flex-1">
                                            <div className="flex justify-between">
                                                <p className="text-sm font-medium text-gray-800">{cidade.nome}</p>
                                                <p className="text-sm font-bold text-blue-600">{formatNumber(cidade.casos)} casos</p>
                                            </div>
                                            <div className="mt-1">
                                                <div className="bg-gray-200 h-2 rounded-full overflow-hidden">
                                                    <div
                                                        className="bg-blue-500 h-2"
                                                        style={{ width: `${percentual}%` }}
                                                    ></div>
                                                </div>
                                                <div className="flex justify-between mt-1">
                                                    <p className="text-xs text-gray-500">{percentual.toFixed(1)}% dos casos de SC</p>
                                                    <p className="text-xs text-blue-500">Clique para detalhes</p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            )}

            {/* Análise por bairros - Preparado para dados futuros */}
            <div className="bg-white rounded-lg shadow-md overflow-hidden">
                <div className="px-4 py-3 bg-gray-50 border-b border-gray-200">
                    <h3 className="text-lg font-medium text-gray-800 flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-blue-500" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                        </svg>
                        Análise por Bairros
                    </h3>
                </div>

                <div className="p-4">
                    <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-4">
                        <p className="text-sm text-blue-700 font-medium mb-1">
                            Dados por bairros em desenvolvimento
                        </p>
                        <p className="text-sm text-blue-600">
                            Para uma análise mais detalhada por bairros, são necessários:
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="border border-dashed border-gray-300 rounded-lg p-4">
                            <h4 className="text-sm font-medium text-blue-600 mb-2">
                                📍 Dados Geográficos
                            </h4>
                            <ul className="text-sm text-gray-600 space-y-1">
                                <li>• Coordenadas GPS dos casos</li>
                                <li>• Mapas de bairros das cidades</li>
                                <li>• Setores censitários do IBGE</li>
                            </ul>
                        </div>

                        <div className="border border-dashed border-gray-300 rounded-lg p-4">
                            <h4 className="text-sm font-medium text-purple-600 mb-2">
                                📊 Dados Históricos
                            </h4>
                            <ul className="text-sm text-gray-600 space-y-1">
                                <li>• Séries temporais 2020-2024</li>
                                <li>• Dados climáticos regionais</li>
                                <li>• Fatores socioeconômicos</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            {/* Modal de Detalhes da Cidade */}
            {selectedCity && (
                <div className="fixed inset-0 bg-transparent backdrop-blur-sm flex items-center justify-center z-50 p-4">
                    <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                        <div className="bg-gradient-to-r from-blue-500 to-blue-700 text-white px-6 py-4 flex justify-between items-center">
                            <div className="flex items-center">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                </svg>
                                <h2 className="text-xl font-bold">{selectedCity.nome}</h2>
                            </div>
                            <button
                                onClick={() => setSelectedCity(null)}
                                className="text-white hover:text-gray-200 focus:outline-none"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </button>
                        </div>

                        <div className="p-6">
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                                {/* Casos */}
                                <div className="bg-red-50 p-4 rounded-lg text-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 mx-auto text-red-500 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                    </svg>
                                    <p className="text-2xl font-bold text-red-600">
                                        {formatNumber(selectedCity.casos)}
                                    </p>
                                    <p className="text-sm text-gray-600">
                                        Casos de Dengue
                                    </p>
                                </div>

                                {/* População */}
                                <div className="bg-blue-50 p-4 rounded-lg text-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 mx-auto text-blue-500 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                                    </svg>
                                    <p className="text-2xl font-bold text-blue-600">
                                        {typeof selectedCity.populacao === 'number'
                                            ? formatNumber(selectedCity.populacao)
                                            : selectedCity.populacao}
                                    </p>
                                    <p className="text-sm text-gray-600">
                                        População
                                    </p>
                                </div>

                                {/* Região */}
                                <div className="bg-purple-50 p-4 rounded-lg text-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 mx-auto text-purple-500 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    <p className="text-lg font-bold text-purple-600">
                                        {selectedCity.regiao}
                                    </p>
                                    <p className="text-sm text-gray-600">
                                        Região
                                    </p>
                                </div>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                                {/* Características */}
                                <div>
                                    <h3 className="text-lg font-bold text-blue-600 mb-3">
                                        🏙️ Características
                                    </h3>
                                    <ul className="space-y-2">
                                        {selectedCity.caracteristicas?.map((caracteristica, index) => (
                                            <li key={index} className="flex items-center">
                                                <div className="h-2 w-2 rounded-full bg-blue-500 mr-2"></div>
                                                <span className="text-gray-700">{caracteristica}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>

                                {/* Análise de Risco */}
                                <div>
                                    <h3 className="text-lg font-bold text-blue-600 mb-3">
                                        ⚠️ Análise de Risco
                                    </h3>
                                    <div className={`p-3 rounded-lg mb-4 ${selectedCity.risco?.includes('Alto') ? 'bg-red-100 text-red-700' :
                                        selectedCity.risco?.includes('Moderado') ? 'bg-yellow-100 text-yellow-700' :
                                            'bg-green-100 text-green-700'
                                        }`}>
                                        {selectedCity.risco}
                                    </div>

                                    {/* Taxa de Incidência */}
                                    {typeof selectedCity.populacao === 'number' && selectedCity.casos > 0 && (
                                        <div className="mt-4">
                                            <p className="text-sm text-gray-600 mb-1">
                                                Taxa de Incidência (por 100.000 hab.)
                                            </p>
                                            <p className="text-2xl font-bold text-blue-600">
                                                {((selectedCity.casos / selectedCity.populacao) * 100000).toFixed(1)}
                                            </p>
                                        </div>
                                    )}
                                </div>
                            </div>

                            {/* Recomendações */}
                            <div className="bg-blue-50 border-l-4 border-blue-500 p-4">
                                <p className="text-sm font-bold text-blue-700 mb-2">
                                    Recomendações para {selectedCity.nome}:
                                </p>
                                <ul className="text-sm text-blue-600 space-y-1">
                                    <li>• Intensificar campanhas de prevenção em áreas de maior risco</li>
                                    <li>• Monitorar focos de água parada em {selectedCity.caracteristicas?.[0]?.toLowerCase()}</li>
                                    <li>• Implementar ações educativas específicas para a região</li>
                                    <li>• Fortalecer a vigilância epidemiológica local</li>
                                </ul>
                            </div>
                        </div>

                        <div className="bg-gray-50 px-6 py-4 flex justify-end">
                            <button
                                onClick={() => setSelectedCity(null)}
                                className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
                            >
                                Fechar
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}