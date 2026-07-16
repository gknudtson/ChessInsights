import { defineConfig } from 'vite';

export default defineConfig({
    build: {
        outDir: 'src/chess_insights/api/static/dist',
        emptyOutDir: true,
        manifest: true,
        rollupOptions: {
            input: {
                main:'frontend/js/main.js',
                contentStyles:'frontend/js/contentStyles.js',
                game: 'frontend/js/game.js',
                play: 'frontend/js/play.js',
            },
            output: {
                entryFileNames: '[name]-[hash].js',
                assetFileNames: 'assets/[name]-[hash][extname]',
            }
        }
    }
});