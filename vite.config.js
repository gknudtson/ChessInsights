import { defineConfig } from 'vite';

export default defineConfig({
    build: {
        outDir: 'src/chess_insights/api/static/dist',
        emptyOutDir: true,
        manifest: true,
        rollupOptions: {
            input: {
                game: 'frontend/js/game.js',
                play: 'frontend/js/play.js',
                demo: 'frontend/js/demo.js'
            },
            output: {
                entryFileNames: '[name]-[hash].js',
                assetFileNames: 'assets/[name]-[hash][extname]',
            }
        }
    }
});