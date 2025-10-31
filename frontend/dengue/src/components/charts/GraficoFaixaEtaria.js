'use client';

import { Bar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    LogarithmicScale,
    BarElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    LogarithmicScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

export default function GraficoFaixaEtaria({ data }) {
    if (!data || !data.faixas || !data.casos) {
        return (
            <div className="h-80 bg-white rounded-lg shadow-md p-4 animate-pulse">
                <div className="h-full bg-gray-200 rounded"></div>
            </div>
        );
    }

    // Verificar se há valores muito discrepantes que justificam escala logarítmica
    const maxValue = Math.max(...data.casos);
    const minValue = Math.min(...data.casos.filter(v => v > 0));
    const useLogScale = maxValue / minValue > 100;

    const chartData = {
        labels: data.faixas,
        datasets: [
            {
                label: 'Número de Casos',
                data: data.casos,
                backgroundColor: 'rgba(53, 162, 235, 0.8)',
                borderColor: 'rgba(53, 162, 235, 1)',
                borderWidth: 1,
            },
            {
                label: 'Letalidade (%)',
                data: data.letalidade,
                backgroundColor: 'rgba(255, 99, 132, 0.8)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1,
                yAxisID: 'y1',
            }
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
                        size: 12
                    }
                }
            },
            title: {
                display: true,
                text: 'Casos e Letalidade por Faixa Etária',
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
                callbacks: {
                    label: function (context) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        if (context.dataset.yAxisID === 'y1') {
                            label += context.raw.toFixed(2) + '%';
                        } else {
                            label += context.raw.toLocaleString('pt-BR');
                        }
                        return label;
                    }
                }
            }
        },
        scales: {
            y: {
                type: useLogScale ? 'logarithmic' : 'linear',
                beginAtZero: false,
                title: {
                    display: true,
                    text: 'Número de Casos (escala ' + (useLogScale ? 'logarítmica' : 'linear') + ')',
                    font: {
                        size: 12,
                        weight: 'bold'
                    }
                },
                ticks: {
                    callback: function (value) {
                        return value.toLocaleString('pt-BR');
                    }
                }
            },
            y1: {
                beginAtZero: true,
                position: 'right',
                title: {
                    display: true,
                    text: 'Letalidade (%)',
                    font: {
                        size: 12,
                        weight: 'bold'
                    }
                },
                grid: {
                    drawOnChartArea: false,
                },
                ticks: {
                    callback: function (value) {
                        return value.toFixed(2) + '%';
                    }
                }
            }
        }
    };

    return (
        <div className="h-80 bg-white rounded-lg shadow-md p-4">
            <Bar data={chartData} options={options} />
            {useLogScale && (
                <div className="mt-2 text-xs text-gray-500 italic text-center">
                    * Escala logarítmica aplicada devido à grande diferença entre valores
                </div>
            )}
        </div>
    );
}