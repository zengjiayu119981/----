import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import inject from '@rollup/plugin-inject'
import { resolve } from 'path'


import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import {ElementPlusResolver} from 'unplugin-vue-components/resolvers'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    inject({ 
      $: "jquery",  // 这里会自动载入 node_modules 中的 jquery   jquery全局变量
      jQuery: "jquery",
      "windows.jQuery": "jquery"
    }),
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }), Components({
     resolvers: [ElementPlusResolver()],
    }),
  ],
  build: {
    assetsDir: 'static',
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        login: resolve(__dirname, 'login/index.html'),
        register: resolve(__dirname, 'register/index.html'),
      },
    },
  },
  server:{
    host: '0.0.0.0'	,
    proxy:{
      "/api":{
        target:"http://127.0.0.1:8000/",
        changeOrigin: true,
      }
    }
  }
})
