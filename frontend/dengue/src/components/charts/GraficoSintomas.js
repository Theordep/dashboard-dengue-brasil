'use client';

import { Bar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';

// Registrar componentes do Chart.js
ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

export default function GraficoSintomas({ data }) {
    if (!data) {
        return (
            <div className="w-full h-full flex items-center justify-center animate-pulse">
                <div className="w-full h-full bg-gray-200 rounded"></div>
            </div>
        );
    }

    // Converter objeto de sintomas para array
    const sintomasArray = Object.entries(data).map(([nome, dados]) => ({
        nome: nome.toUpperCase(),
        casos: dados.casos,
        percentual: dados.percentual
    }));

    // Ordenar por número de casos
    sintomasArray.sort((a, b) => b.casos - a.casos);

    const chartData = {
        labels: sintomasArray.map(item => item.nome),
        datasets: [
            {
                label: 'Percentual de Casos (%)',
                data: sintomasArray.map(item => item.percentual.toFixed(1)),
                backgroundColor: [
                    'rgba(153, 102, 255, 0.8)',
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(255, 159, 64, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                ],
                borderColor: [
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                ],
                borderWidth: 1,
                borderRadius: 5,
            },
        ],
    };

    const options = {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    font: {
                        size: 14
                    }
                }
            },
            title: {
                display: true,
                text: 'Sintomas Mais Comuns',
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
                borderColor: 'rgba(0, 0, 0, 0.1)',
                borderWidth: 1,
                callbacks: {
                    title: function (tooltipItems) {
                        return `Sintoma: ${tooltipItems[0].label}`;
                    },
                    label: function (context) {
                        const value = context.raw;
                        const sintoma = sintomasArray[context.dataIndex];
                        return [
                            `Percentual: ${value}%`,
                            `Casos: ${sintoma.casos.toLocaleString('pt-BR')}`
                        ];
                    }
                }
            }
        },
        scales: {
            x: {
                beginAtZero: true,
                max: 100,
                grid: {
                    color: 'rgba(0, 0, 0, 0.05)',
                },
                title: {
                    display: true,
                    text: 'Percentual (%)',
                    font: {
                        size: 14,
                        weight: 'bold'
                    }
                },
                ticks: {
                    font: {
                        size: 12
                    }
                }
            },
            y: {
                grid: {
                    display: false
                },
                ticks: {
                    font: {
                        size: 12,
                        weight: 'bold'
                    }
                }
            }
        },
        animation: {
            duration: 2000,
            easing: 'easeOutQuart'
        }
    };

    return (
        <div className="w-full h-full overflow-hidden">
            <Bar data={chartData} options={options} />
        </div>
    );
}