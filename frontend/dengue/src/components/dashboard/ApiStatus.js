'use client';

import { useState, useEffect } from 'react';
import { apiService } from '@/services/api';

export default function ApiStatus() {
    const [status, setStatus] = useState({
        isLoading: true,
        isConnected: false,
        error: null,
        info: null
    });

    useEffect(() => {
        const checkApiStatus = async () => {
            try {
                const response = await apiService.healthCheck();
                setStatus({
                    isLoading: false,
                    isConnected: true,
                    error: null,
                    info: response.data
                });
            } catch (error) {
                setStatus({
                    isLoading: false,
                    isConnected: false,
                    error: error.message || 'Erro ao conectar com a API',
                    info: null
                });
            }
        };

        checkApiStatus();
    }, []);

    // Se estiver carregando ou conectado, não mostra nada
    if (status.isLoading || status.isConnected) {
        return null;
    }

    // Apenas mostra o alerta se houver erro de conexão
    if (!status.isConnected) {
        return (
            <div className="bg-red-100 border-l-4 border-red-500 p-4 rounded-r-lg shadow-md">
                <div className="flex">
                    <div className="flex-shrink-0">
                        <svg className="h-5 w-5 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                    <div className="ml-3">
                        <p className="text-sm font-medium text-red-800">
                            Erro de conexão com a API
                        </p>
                        <p className="text-sm text-red-700 mt-1">
                            {status.error}. Verifique se o servidor Django está rodando na porta 8000.
                        </p>
                        <div className="mt-3">
                            <button
                                onClick={() => window.location.reload()}
                                className="bg-red-500 hover:bg-red-600 text-white text-xs px-3 py-1 rounded-md transition-colors"
                            >
                                Tentar novamente
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return null;
}