// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

const isGhPages = process.env.GH_PAGES === 'true';

export default defineConfig({
  site: isGhPages ? 'https://kishore-prakash.github.io' : 'https://kishoreprakash.in',
  base: isGhPages ? '/Portfolio' : '/',
  trailingSlash: 'ignore',
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
  build: {
    inlineStylesheets: 'auto',
  },
});
