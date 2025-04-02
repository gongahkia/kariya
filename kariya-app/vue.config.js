const { defineConfig } = require('@vue/cli-service')

module.exports = {
  transpileDependencies: true,
  outputDir: '../backend/static',
  assetsDir: 'static',
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
}