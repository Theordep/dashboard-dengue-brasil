'use client';

import { Radar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend
} from 'chart.js';

ChartJS.register(
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend
);

export default function GraficoSintomasPerfil({ data, faixaEtaria }) {
    if (!data || !data.por_faixa_etaria || !faixaEtaria || !data.por_faixa_etaria[faixaEtaria]) {
        return (
            <div className="h-80 bg-white rounded-lg shadow-md p-4 flex items-center justify-center">
                <div className="text-center text-gray-500">
                    <p className="text-lg font-medium">
                        {!data || !data.por_faixa_etaria
                            ? 'Dados não disponíveis'
                            : !faixaEtaria
                                ? 'Selecione uma faixa etária'
                                : 'Dados não disponíveis para esta faixa etária'}
                    </p>
                </div>
            </div>
        );
    }

    const sintomasFaixa = data.por_faixa_etaria[faixaEtaria];

    // Extrair sintomas e percentuais
    const sintomas = Object.keys(sintomasFaixa).map(s => s.charAt(0).toUpperCase() + s.slice(1));
    const percentuais = Object.values(sintomasFaixa).map(v => {
        const percentual = v?.percentual;
        return typeof percentual === 'number' ? percentual : 0;
    });

    const chartData = {
        labels: sintomas,
        datasets: [
            {
                label: `Faixa ${faixaEtaria} anos`,
                data: percentuais,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(255, 99, 132, 1)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(255, 99, 132, 1)',
                pointRadius: 4,
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
                text: `Sintomas na Faixa Etária ${faixaEtaria}`,
                font: {
                    size: 16,
                    weight: 'bold'
                }
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        const value = context.raw || 0;
                        return `${context.label}: ${typeof value === 'number' ? value.toFixed(2) : '0.00'}%`;
                    }
                }
            }
        },
        scales: {
            r: {
                angleLines: {
                    display: true
                },
                suggestedMin: 0,
                suggestedMax: 100,
                ticks: {
                    callback: function (value) {
                        return value + '%';
                    }
                }
            }
        }
    };

    return (
        <div className="h-80 bg-white rounded-lg shadow-md p-4">
            <Radar data={chartData} options={options} />
        </div>
    );
}
