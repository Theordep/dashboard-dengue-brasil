'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import Sidebar from './Sidebar';

export default function Header() {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const pathname = usePathname();

    const menuItems = [
        { href: '/', label: 'Dashboard', icon: '📊' },
        { href: '/santa-catarina', label: 'Santa Catarina', icon: '🏖️' },
        { href: '/analise-avancada', label: 'Análise Avançada', icon: '🔬' },
        { href: '/sobre', label: 'Sobre', icon: 'ℹ️' },
    ];

    return (
        <>
            <header className="bg-gradient-to-r from-blue-700 to-blue-900 text-white shadow-lg sticky top-0 z-30">
                <div className="container mx-auto px-4 py-4">
                    <div className="flex justify-between items-center">
                        {/* Logo e Título */}
                        <Link href="/" className="flex items-center min-w-0 flex-1">
                            <div className="flex flex-col min-w-0">
                                <div className="flex items-center space-x-2 sm:space-x-3">
                                    <span className="text-2xl sm:text-3xl flex-shrink-0">🦟</span>
                                    <div className="min-w-0">
                                        <h1 className="text-base sm:text-xl md:text-2xl font-bold tracking-wide text-white drop-shadow-md truncate">
                                            Dashboard de Dengue
                                        </h1>
                                        <p className="text-xs sm:text-sm text-blue-100 truncate hidden sm:block">
                                            Análise epidemiológica com dados do DATASUS
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </Link>

                        {/* Menu Desktop */}
                        <nav className="hidden md:flex space-x-4 lg:space-x-6">
                            {menuItems.map((item) => {
                                const isActive = pathname === item.href;
                                return (
                                    <Link
                                        key={item.href}
                                        href={item.href}
                                        className={`
                                            text-white font-medium text-base lg:text-lg
                                            transition-colors duration-200
                                            relative
                                            ${isActive
                                                ? 'text-yellow-300'
                                                : 'hover:text-yellow-300'
                                            }
                                        `}
                                    >
                                        <span className="hidden lg:inline mr-2">{item.icon}</span>
                                        {item.label}
                                        {isActive && (
                                            <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-yellow-300 rounded"></span>
                                        )}
                                    </Link>
                                );
                            })}
                        </nav>

                        {/* Botão Menu Mobile */}
                        <button
                            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                            className="md:hidden p-2 rounded-lg hover:bg-blue-800 transition-colors focus:outline-none focus:ring-2 focus:ring-yellow-400 ml-3 flex-shrink-0"
                            aria-label="Abrir menu"
                            aria-expanded={isSidebarOpen}
                        >
                            {isSidebarOpen ? (
                                <svg
                                    className="w-6 h-6"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M6 18L18 6M6 6l12 12"
                                    />
                                </svg>
                            ) : (
                                <svg
                                    className="w-6 h-6"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M4 6h16M4 12h16M4 18h16"
                                    />
                                </svg>
                            )}
                        </button>
                    </div>
                </div>
            </header>

            {/* Sidebar Mobile */}
            <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />
        </>
    );
}
