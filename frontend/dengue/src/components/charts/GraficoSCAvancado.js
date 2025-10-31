'use client';

import { Bar, Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend,
    Filler
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

export function GraficoMunicipiosSC({ data }) {
    if (!data || !data.municipios || !data.municipios.nomes || !data.municipios.casos) {
        return (
            <div className="h-80 bg-white rounded-lg shadow-md p-4 animate-pulse">
                <div className="h-full bg-gray-200 rounded"></div>
            </div>
        );
    }

    const chartData = {
        labels: data.municipios.nomes,
        datasets: [
            {
                label: 'Casos por Município',
                data: data.municipios.casos,
                backgroundColor: 'rgba(75, 192, 192, 0.8)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
            }
        ],
    };

    const options = {
        indexAxis: 'y',  // Gráfico horizontal
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Top 10 Municípios de Santa Catarina',
                font: {
                    size: 16,
                    weight: 'bold'
                }
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        label += context.raw.toLocaleString('pt-BR');
                        return label;
                    }
                }
            }
        },
        scales: {
            x: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Número de Casos',
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
            y: {
                title: {
                    display: true,
                    text: 'Município',
                    font: {
                        size: 12,
                        weight: 'bold'
                    }
                }
            }
        }
    };

    return (
        <div className="h-80 bg-white rounded-lg shadow-md p-4">
            <Bar data={chartData} options={options} />
        </div>
    );
}

export function GraficoCrescimentoSC({ data }) {
    if (!data || !data.analise_temporal || !data.analise_temporal.meses || !data.analise_temporal.crescimento_percentual) {
        return (
            <div className="h-80 bg-white rounded-lg shadow-md p-4 animate-pulse">
                <div className="h-full bg-gray-200 rounded"></div>
            </div>
        );
    }

    const meses = data.analise_temporal.meses.map(m => {
        const nomesMeses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
        return nomesMeses[m - 1];
    });

    const crescimento = data.analise_temporal.crescimento_percentual;

    const chartData = {
        labels: meses,
        datasets: [
            {
                label: 'Crescimento Mensal (%)',
                data: crescimento,
                fill: {
                    target: 'origin',
                    above: 'rgba(255, 99, 132, 0.2)',
                    below: 'rgba(54, 162, 235, 0.2)',
                },
                backgroundColor: function (context) {
                    const value = context.dataset.data[context.dataIndex];
                    return value >= 0 ? 'rgba(75, 192, 192, 1)' : 'rgba(255, 99, 132, 1)';
                },
                borderColor: function (context) {
                    const value = context.dataset.data[context.dataIndex];
                    return value >= 0 ? 'rgba(75, 192, 192, 1)' : 'rgba(255, 99, 132, 1)';
                },
                borderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7,
            }
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Crescimento Percentual Mensal',
                font: {
                    size: 16,
                    weight: 'bold'
                }
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        label += context.raw.toFixed(2) + '%';
                        return label;
                    }
                }
            }
        },
        scales: {
            y: {
                title: {
                    display: true,
                    text: 'Crescimento (%)',
                    font: {
                        size: 12,
                        weight: 'bold'
                    }
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
            <Line data={chartData} options={options} />
        </div>
    );
}
