import { defineConfig } from 'vite';

export default defineConfig({
    build: {
        outDir: 'src/chess_insights/api/static/dist',
        emptyOutDir: true,
        rollupOptions: {
            input: {
                game: 'frontend/game.js',
                play: 'frontend/play.js'
            },
            output: {
                entryFileNames: '[name].js',
                assetFileNames: '[name][extname]'
            }
        }
    }
});