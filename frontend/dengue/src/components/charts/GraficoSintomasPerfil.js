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
    if (!data || !data.por_faixa_etaria || !data.por_faixa_etaria[faixaEtaria]) {
        return (
            <div className="h-80 bg-white rounded-lg shadow-md p-4 animate-pulse">
                <div className="h-full bg-gray-200 rounded"></div>
            </div>
        );
    }

    const sintomasFaixa = data.por_faixa_etaria[faixaEtaria];

    // Extrair sintomas e percentuais
    const sintomas = Object.keys(sintomasFaixa).map(s => s.charAt(0).toUpperCase() + s.slice(1));
    const percentuais = Object.values(sintomasFaixa).map(v => v.percentual);

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
                        return `${context.label}: ${context.raw.toFixed(2)}%`;
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
