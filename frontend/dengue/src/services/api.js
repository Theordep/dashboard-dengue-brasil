import axios from 'axios';

// Detectar se está em produção ou desenvolvimento
const isProduction = typeof window !== 'undefined' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1';
const API_URL = process.env.NEXT_PUBLIC_API_URL || (isProduction ? '/api' : 'http://localhost:8000/api');

// Configuração base do Axios
const api = axios.create({
    baseURL: API_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
});

// Serviço de API com métodos específicos
export const apiService = {
    // Verificação de saúde da API
    healthCheck: () => {
        return api.get('/health');
    },

    // Informações gerais da API
    getApiInfo: () => {
        return api.get('/info');
    },

    // Dados do dashboard
    getDashboardData: () => {
        return api.get('/dashboard');
    },

    // Dados de estatísticas por estado
    getEstadosData: () => {
        return api.get('/estados');
    },

    // Dados de estatísticas por ano
    getAnosData: () => {
        return api.get('/anos');
    },

    // Dados de sintomas mais comuns
    getSintomasData: () => {
        return api.get('/sintomas');
    },

    // Detalhes de Santa Catarina
    getSantaCatarinaData: () => {
        return api.get('/santa-catarina');
    },

    // Carregar estatísticas do arquivo JSON
    loadStatistics: () => {
        return api.post('/carregar-estatisticas');
    },

    // API Avançada

    // Dados de faixas etárias
    getFaixasEtarias: () => {
        return api.get('/avancado/faixas-etarias');
    },

    // Dados detalhados por gênero
    getGeneroDetalhado: () => {
        return api.get('/avancado/genero');
    },

    // Dados avançados de Santa Catarina
    getSantaCatarinaAvancado: () => {
        return api.get('/avancado/santa-catarina');
    },

    // Dados de sintomas por perfil
    getSintomasPorPerfil: () => {
        return api.get('/avancado/sintomas-por-perfil');
    },

    // Carregar estatísticas avançadas do arquivo JSON
    loadAdvancedStatistics: () => {
        return api.post('/avancado/carregar-estatisticas');
    }
};

export default api;