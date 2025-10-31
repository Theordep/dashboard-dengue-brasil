export default function EstatisticasGerais({ data }) {
    if (!data) {
        return (
            <div className="p-4 bg-white rounded-lg shadow-md animate-pulse">
                <div className="h-8 bg-gray-200 rounded mb-4"></div>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    {[...Array(4)].map((_, i) => (
                        <div key={i} className="h-32 bg-gray-200 rounded"></div>
                    ))}
                </div>
            </div>
        );
    }

    const formatNumber = (num) => {
        return num ? num.toLocaleString('pt-BR') : 'N/A';
    };

    const formatDate = (dateString) => {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleDateString('pt-BR');
    };

    return (
        <div className="p-3 sm:p-4 bg-white rounded-lg shadow-md">
            <h2 className="text-lg sm:text-xl font-bold mb-3 sm:mb-4 text-gray-800">Estatísticas Gerais</h2>

            <div className="grid grid-cols-2 md:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
                {/* Total de Casos */}
                <div className="bg-gradient-to-r from-red-500 to-red-700 text-white p-3 sm:p-4 rounded-lg shadow-md">
                    <div className="text-center">
                        <h3 className="text-xs sm:text-sm font-medium opacity-80">Total de Casos</h3>
                        <p className="text-xl sm:text-2xl md:text-3xl font-bold mt-1 sm:mt-2">{formatNumber(data.total_casos)}</p>
                    </div>
                </div>

                {/* Estados Únicos */}
                <div className="bg-gradient-to-r from-blue-500 to-blue-700 text-white p-3 sm:p-4 rounded-lg shadow-md">
                    <div className="text-center">
                        <h3 className="text-xs sm:text-sm font-medium opacity-80">Estados Afetados</h3>
                        <p className="text-xl sm:text-2xl md:text-3xl font-bold mt-1 sm:mt-2">{data.estados_unicos || 'N/A'}</p>
                    </div>
                </div>

                {/* Período Início */}
                <div className="bg-gradient-to-r from-green-500 to-green-700 text-white p-3 sm:p-4 rounded-lg shadow-md">
                    <div className="text-center">
                        <h3 className="text-xs sm:text-sm font-medium opacity-80">Início do Período</h3>
                        <p className="text-lg sm:text-xl md:text-2xl font-bold mt-1 sm:mt-2 break-words">{formatDate(data.periodo_inicio)}</p>
                    </div>
                </div>

                {/* Período Fim */}
                <div className="bg-gradient-to-r from-orange-500 to-orange-700 text-white p-3 sm:p-4 rounded-lg shadow-md">
                    <div className="text-center">
                        <h3 className="text-xs sm:text-sm font-medium opacity-80">Fim do Período</h3>
                        <p className="text-lg sm:text-xl md:text-2xl font-bold mt-1 sm:mt-2 break-words">{formatDate(data.periodo_fim)}</p>
                    </div>
                </div>
            </div>
        </div>
    );
}