import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    // Same "/api" path as production: the code never needs a different base URL
    proxy: { "/api": "http://localhost:8000" },
  },
});