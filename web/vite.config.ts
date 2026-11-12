import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";

// The build goes straight into app/static, which FastAPI serves. `npm run dev` proxies the API to uvicorn on :8000.
export default defineConfig({
  plugins: [react(), tailwindcss()],
  // assetsInlineLimit 0: no data: URLs, so the CSP can stay font-src 'self'.
  build: { outDir: "../app/static", emptyOutDir: true, assetsInlineLimit: 0 },
  server: { proxy: { "/turn": "http://127.0.0.1:8000", "/ws": { target: "ws://127.0.0.1:8000", ws: true } } },
});
