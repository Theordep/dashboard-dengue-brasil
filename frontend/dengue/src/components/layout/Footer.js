export default function Footer() {
    return (
        <footer className="bg-gray-100 text-gray-600 py-4 sm:py-6 border-t border-gray-200">
            <div className="container mx-auto px-4">
                <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                    <div className="text-center md:text-left">
                        <p className="text-xs sm:text-sm">
                            Dashboard de Dengue © {new Date().getFullYear()} - Projeto Python Dengue
                        </p>
                    </div>

                    <div className="flex flex-wrap justify-center gap-4 sm:gap-6">
                        <a
                            href="https://github.com"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-xs sm:text-sm hover:text-blue-600 transition-colors"
                        >
                            GitHub
                        </a>
                        <a
                            href="https://datasus.gov.br"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-xs sm:text-sm hover:text-blue-600 transition-colors"
                        >
                            DATASUS
                        </a>
                        <a
                            href="/sobre"
                            className="text-xs sm:text-sm hover:text-blue-600 transition-colors"
                        >
                            Sobre o projeto
                        </a>
                    </div>
                </div>
            </div>
        </footer>
    );
}