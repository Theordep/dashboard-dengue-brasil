'use client';

import { useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Sidebar({ isOpen, onClose }) {
    const pathname = usePathname();

    // Fechar sidebar ao clicar fora ou pressionar ESC
    useEffect(() => {
        if (isOpen) {
            document.body.style.overflow = 'hidden';

            const handleEscape = (e) => {
                if (e.key === 'Escape') {
                    onClose();
                }
            };

            window.addEventListener('keydown', handleEscape);
            return () => {
                window.removeEventListener('keydown', handleEscape);
                document.body.style.overflow = 'unset';
            };
        }
    }, [isOpen, onClose]);

    const menuItems = [
        { href: '/', label: 'Dashboard', icon: '📊' },
        { href: '/santa-catarina', label: 'Santa Catarina', icon: '🏖️' },
        { href: '/analise-avancada', label: 'Análise Avançada', icon: '🔬' },
        { href: '/sobre', label: 'Sobre', icon: 'ℹ️' },
    ];

    const handleLinkClick = () => {
        onClose();
    };

    return (
        <>
            {/* Overlay com efeito glass */}
            {isOpen && (
                <div
                    className="fixed inset-0 bg-white/10 backdrop-blur-sm z-40 transition-opacity duration-300 md:hidden"
                    onClick={onClose}
                    aria-hidden="true"
                />
            )}

            {/* Sidebar */}
            <aside
                className={`
                    fixed top-0 left-0 h-full w-64 bg-gradient-to-b from-blue-800 to-blue-900 text-white z-50
                    transform transition-transform duration-300 ease-in-out
                    md:hidden
                    ${isOpen ? 'translate-x-0' : '-translate-x-full'}
                `}
            >
                <div className="flex flex-col h-full">
                    {/* Header do Sidebar */}
                    <div className="flex items-center justify-between p-5 border-b border-blue-700">
                        <div className="flex items-center space-x-2">
                            <span className="text-2xl">🦟</span>
                            <h2 className="text-lg font-bold">Menu</h2>
                        </div>
                        <button
                            onClick={onClose}
                            className="p-2 rounded-lg hover:bg-blue-700 transition-colors focus:outline-none focus:ring-2 focus:ring-yellow-400"
                            aria-label="Fechar menu"
                        >
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
                        </button>
                    </div>

                    {/* Itens do Menu */}
                    <nav className="flex-1 overflow-y-auto py-4">
                        <ul className="space-y-2 px-4">
                            {menuItems.map((item) => {
                                const isActive = pathname === item.href;
                                return (
                                    <li key={item.href}>
                                        <Link
                                            href={item.href}
                                            onClick={handleLinkClick}
                                            className={`
                                                flex items-center space-x-3 px-4 py-3 rounded-lg
                                                transition-all duration-200
                                                ${isActive
                                                    ? 'bg-yellow-400 text-blue-900 font-bold shadow-lg border-2 border-yellow-300'
                                                    : 'text-white hover:bg-blue-700 hover:text-yellow-200'
                                                }
                                            `}
                                        >
                                            <span className="text-xl">{item.icon}</span>
                                            <span className="font-semibold text-lg">{item.label}</span>
                                            {isActive && (
                                                <span className="ml-auto w-2 h-2 bg-blue-900 rounded-full"></span>
                                            )}
                                        </Link>
                                    </li>
                                );
                            })}
                        </ul>
                    </nav>

                    {/* Footer do Sidebar */}
                    <div className="p-5 border-t border-blue-700">
                        <p className="text-sm text-blue-200 text-center">
                            Dashboard de Dengue
                        </p>
                        <p className="text-xs text-blue-300 text-center mt-1">
                            Análise epidemiológica
                        </p>
                    </div>
                </div>
            </aside>
        </>
    );
}

