import { defineConfig } from "vitest/config";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import path from "path";

export default defineConfig({
  resolve: {
    alias: {
      $lib: path.resolve(__dirname, "./src/lib"),
      "$app/stores": path.resolve(__dirname, "src/test-app-stores.ts"),
    },
  },
  plugins: [svelte({})],
  define: {
    "import.meta.env.VITE_API_URL": JSON.stringify("/api"),
  },
  test: {
    environment: "jsdom",
    environmentOptions: {
      jsdom: {
        url: "http://localhost/",
      },
    },
    setupFiles: ["./src/test-setup.ts"],
    globals: true,
  },
});
