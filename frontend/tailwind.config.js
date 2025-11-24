/** @type {import('tailwindcss').Config} */
export default {
    darkMode: ["class"],
    content: [
        './pages/**/*.{js,jsx,ts,tsx}',
        './components/**/*.{js,jsx,ts,tsx}',
        './app/**/*.{js,jsx,ts,tsx}',
        './src/**/*.{js,jsx,ts,tsx}',
    ],
    theme: {
        extend: {
            colors: {
                background: '#0a0a0f', // Deepest Black
                foreground: '#ffffff',
                muted: '#A1A1AA',
                primary: {
                    DEFAULT: '#00f3ff', // Neon Cyan
                    foreground: '#000000',
                },
                secondary: {
                    DEFAULT: '#121218', // Panel Background
                    foreground: '#ffffff',
                },
                accent: {
                    cyan: '#00f3ff',
                    amber: '#ffaa00',
                    purple: '#bd00ff',
                },
                border: 'rgba(255, 255, 255, 0.08)',
                ring: 'rgba(255, 255, 255, 0.2)',
            },
            borderRadius: {
                lg: '11px',
                md: '8px',
                sm: '4px',
            },
        },
    },
    plugins: [],
}
