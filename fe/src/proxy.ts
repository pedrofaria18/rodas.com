import { createProxyMiddleware } from 'http-proxy-middleware'

export default function  (app: any) {
  app.use('/api', createProxyMiddleware({
    target: 'http://localhost:9200', // Insira a URL do seu servidor Elasticsearch aqui
    changeOrigin: true,
  })); // Defina o caminho de rota do proxy, por exemplo, '/api'
};