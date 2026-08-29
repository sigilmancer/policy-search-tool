// @ts-check
import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  integrations: [svelte()],
  
  site: 'https://sigilmancer.github.io', 
  base: '/policy-search-tool', 

  vite: {
    plugins: [tailwindcss()]
  }
});
