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

export default function GraficoGenero({ data }) {
    if (!data || !data.distribuicao_por_faixa) {
        return (
            <div className="h-80 bg-white rounded-lg shadow-md p-4 animate-pulse">
                <div className="h-full bg-gray-200 rounded"></div>
            </div>
        );
    }

    const distribuicao = data.distribuicao_por_faixa;
    const faixas = Object.keys(distribuicao);

    // Extrair dados para feminino e masculino
    const dadosFeminino = faixas.map(faixa => distribuicao[faixa]?.feminino || 0);
    const dadosMasculino = faixas.map(faixa => distribuicao[faixa]?.masculino || 0);

    // Verificar se há valores muito discrepantes que justificam escala logarítmica
    const todosValores = [...dadosFeminino, ...dadosMasculino];
    const valoresPositivos = todosValores.filter(v => v > 0);
    const maxValue = valoresPositivos.length > 0 ? Math.max(...valoresPositivos) : 1;
    const minValue = valoresPositivos.length > 0 ? Math.min(...valoresPositivos) : 1;
    const useLogScale = valoresPositivos.length > 0 && maxValue > 0 && minValue > 0 && maxValue / minValue > 100;

    const chartData = {
        labels: faixas,
        datasets: [
            {
                label: 'Feminino',
                data: dadosFeminino,
                backgroundColor: 'rgba(255, 99, 132, 0.8)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1,
            },
            {
                label: 'Masculino',
                data: dadosMasculino,
                backgroundColor: 'rgba(53, 162, 235, 0.8)',
                borderColor: 'rgba(53, 162, 235, 1)',
                borderWidth: 1,
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
                text: 'Distribuição por Gênero e Faixa Etária',
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
                        const value = context.raw || 0;
                        label += typeof value === 'number' ? value.toLocaleString('pt-BR') : '0';
                        return label;
                    }
                }
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Faixa Etária',
                    font: {
                        size: 12,
                        weight: 'bold'
                    }
                }
            },
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