import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueJsx from "@vitejs/plugin-vue-jsx";
import sass from "vite-plugin-sass-dts";
import autoprefixer from "autoprefixer";
import path from "path";
import { glob } from "glob";

export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
    sass({
      enabledMode: ["development", "production"],
    }),
  ],
  css: {
    postcss: {
      plugins: [autoprefixer({})],
    },
  },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  root: path.join(__dirname, "src"),
  build: {
    outDir: path.join(__dirname, "dist"),
    emptyOutDir: true,
    rollupOptions: {
      input: glob.sync("src/*.html"),
      output: {
        assetFileNames: ({ name }) => {
          const ext = path.extname(name).slice(1);

          if (/js|css/i.test(ext)) {
            return `assets/[name]-[hash][extname]`;
          }

          return `res/[name][extname]`;
        },
        // chunkFileNames: "static/assets/[name]-[hash].js",
        // entryFileNames: "static/assets/[name]-[hash].js",
      },
    },
  },
  experimental: {
    renderBuiltUrl(filename, { type }) {
      if (type === "public" || type === "asset") {
        return "/static/" + filename;
      }
      return filename;
    },
  },
});
