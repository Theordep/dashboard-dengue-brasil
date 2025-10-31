'use client';

import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
} from 'chart.js';

// Registrar componentes do Chart.js
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

export default function GraficoAnos({ data }) {
    // Verificar se os dados estão disponíveis
    if (!data) {
        return (
            <div className="h-80 bg-white rounded-lg shadow-md p-4 animate-pulse">
                <div className="h-full bg-gray-200 rounded"></div>
            </div>
        );
    }

    // Extrair os anos e casos, lidando com diferentes formatos de dados
    let anos = [];
    let casos = [];

    // Formato da API /anos/
    if (data.anos && data.casos) {
        anos = data.anos;
        casos = data.casos;
    }
    // Nenhum dado válido encontrado
    else {
        console.error("Formato de dados inválido para o gráfico de anos:", data);
        return (
            <div className="w-full h-full flex items-center justify-center">
                <div className="text-center text-gray-500">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                    <p className="text-lg font-medium">Dados de evolução temporal não disponíveis</p>
                    <p className="text-sm mt-2">Verifique se o processamento de dados foi concluído corretamente</p>
                </div>
            </div>
        );
    }

    // Verificar se há dados suficientes para criar o gráfico
    if (anos.length === 0 || casos.length === 0) {
        return (
            <div className="w-full h-full flex items-center justify-center">
                <div className="text-center text-gray-500">
                    <p className="text-lg font-medium">Sem dados disponíveis</p>
                    <p className="text-sm mt-2">Não há dados de evolução temporal para exibir</p>
                </div>
            </div>
        );
    }

    // Garantir que os anos estão ordenados cronologicamente
    const indices = Array.from({ length: anos.length }, (_, i) => i);
    indices.sort((a, b) => anos[a] - anos[b]);

    const sortedAnos = indices.map(i => anos[i]);
    const sortedCasos = indices.map(i => casos[i]);

    // Criar dados para o gráfico
    const chartData = {
        labels: sortedAnos,
        datasets: [
            {
                label: 'Número de Casos',
                data: sortedCasos,
                fill: {
                    target: 'origin',
                    above: 'rgba(75, 192, 192, 0.2)',
                },
                backgroundColor: 'rgba(75, 192, 192, 0.8)',
                borderColor: 'rgba(75, 192, 192, 1)',
                tension: 0.3,
                pointRadius: 6,
                pointHoverRadius: 8,
                pointBackgroundColor: 'rgba(75, 192, 192, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    font: {
                        size: 14,
                    }
                }
            },
            title: {
                display: true,
                text: 'Evolução de Casos por Ano',
                font: {
                    size: 16,
                    weight: 'bold'
                },
                padding: {
                    top: 10,
                    bottom: 20
                }
            },
            tooltip: {
                backgroundColor: 'rgba(255, 255, 255, 0.9)',
                titleColor: '#333',
                bodyColor: '#333',
                titleFont: {
                    size: 14,
                    weight: 'bold'
                },
                bodyFont: {
                    size: 13
                },
                padding: 12,
                boxPadding: 6,
                borderColor: 'rgba(75, 192, 192, 0.5)',
                borderWidth: 1,
                callbacks: {
                    title: function (tooltipItems) {
                        return `Ano: ${tooltipItems[0].label}`;
                    },
                    label: function (context) {
                        const value = context.raw;
                        return `Casos: ${value.toLocaleString('pt-BR')}`;
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(0, 0, 0, 0.05)',
                },
                ticks: {
                    font: {
                        size: 12
                    },
                    callback: function (value) {
                        return value.toLocaleString('pt-BR');
                    }
                },
                title: {
                    display: true,
                    text: 'Número de Casos',
                    font: {
                        size: 14,
                        weight: 'bold'
                    },
                    padding: {
                        bottom: 10
                    }
                }
            },
            x: {
                grid: {
                    color: 'rgba(0, 0, 0, 0.05)',
                },
                ticks: {
                    font: {
                        size: 12,
                        weight: 'bold'
                    }
                },
                title: {
                    display: true,
                    text: 'Ano',
                    font: {
                        size: 14,
                        weight: 'bold'
                    },
                    padding: {
                        top: 10
                    }
                }
            }
        },
        animation: {
            duration: 2000,
            easing: 'easeOutQuart'
        },
        elements: {
            line: {
                borderWidth: 3
            }
        }
    };

    return (
        <div className="w-full h-full overflow-hidden">
            <Line data={chartData} options={options} />
        </div>
    );
}