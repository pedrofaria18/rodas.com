const express = require('express');
const axios = require('axios');

const cors = require('./middlewares/cors');

const app = express();
const port = 3000;

app.use(express.json());
app.use(cors);

// Rota para realizar uma solicitação ao backend
app.get('/api/backend', async (req, res) => {
  try {
    const response = await axios.get('http://localhost:9200/');

    res.json(response.data);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Erro ao realizar a solicitação ao backend.' });
  }
});

app.get('/cars', (req, res) => {
  res.json([
    {
      id: 1,
      name: 'Mercedes-Benz Classe C C-200 AVANTGARDE 2.0 TB 16V 184CV AUT.',
      year: 2019,
      location: 'São Paulo Zona Sul - São Paulo',
      price: 124900,
      kilometers: 89410,
      image:
        'https://http2.mlstatic.com/D_NQ_NP_753339-MLB69496967212_052023-O.webp',
      link: 'https://carro.mercadolivre.com.br/MLB-3646064094-mercedes-benz-c-200-avantgarde-20-tb-16v-184cv-aut-gasol-_JM#position=1&search_layout=grid&type=item&tracking_id=275c3a8f-d24f-4b99-b2ad-fea1bc5312ea',
      about: {
        color: 'Prateado',
        fuelType: 'Gasolina',
        doors: 4,
        streamingType: 'Automático',
      },
    },
    {
      id: 2,
      name: 'Mercedes-Benz Classe C C-200 AVANTGARDE 2.0 TB 16V 184CV AUT.',
      year: 2019,
      location: 'São Paulo Zona Sul - São Paulo',
      price: 124900,
      kilometers: 89410,
      image:
        'https://http2.mlstatic.com/D_NQ_NP_753339-MLB69496967212_052023-O.webp',
      link: 'https://carro.mercadolivre.com.br/MLB-3646064094-mercedes-benz-c-200-avantgarde-20-tb-16v-184cv-aut-gasol-_JM#position=1&search_layout=grid&type=item&tracking_id=275c3a8f-d24f-4b99-b2ad-fea1bc5312ea',
      about: {
        color: 'Prateado',
        fuelType: 'Gasolina',
        doors: 4,
        streamingType: 'Automático',
      },
    },
    {
      id: 3,
      name: 'Mercedes-Benz Classe C C-200 AVANTGARDE 2.0 TB 16V 184CV AUT.',
      year: 2019,
      location: 'São Paulo Zona Sul - São Paulo',
      price: 124900,
      kilometers: 89410,
      image:
        'https://http2.mlstatic.com/D_NQ_NP_753339-MLB69496967212_052023-O.webp',
      link: 'https://carro.mercadolivre.com.br/MLB-3646064094-mercedes-benz-c-200-avantgarde-20-tb-16v-184cv-aut-gasol-_JM#position=1&search_layout=grid&type=item&tracking_id=275c3a8f-d24f-4b99-b2ad-fea1bc5312ea',
      about: {
        color: 'Prateado',
        fuelType: 'Gasolina',
        doors: 4,
        streamingType: 'Automático',
      },
    },
    {
      id: 4,
      name: 'Mercedes-Benz Classe C C-200 AVANTGARDE 2.0 TB 16V 184CV AUT.',
      year: 2019,
      location: 'São Paulo Zona Sul - São Paulo',
      price: 124900,
      kilometers: 89410,
      image:
        'https://http2.mlstatic.com/D_NQ_NP_753339-MLB69496967212_052023-O.webp',
      link: 'https://carro.mercadolivre.com.br/MLB-3646064094-mercedes-benz-c-200-avantgarde-20-tb-16v-184cv-aut-gasol-_JM#position=1&search_layout=grid&type=item&tracking_id=275c3a8f-d24f-4b99-b2ad-fea1bc5312ea',
      about: {
        color: 'Prateado',
        fuelType: 'Gasolina',
        doors: 4,
        streamingType: 'Automático',
      },
    },
    {
      id: 5,
      name: 'Mercedes-Benz Classe C C-200 AVANTGARDE 2.0 TB 16V 184CV AUT.',
      year: 2019,
      location: 'São Paulo Zona Sul - São Paulo',
      price: 124900,
      kilometers: 89410,
      image:
        'https://http2.mlstatic.com/D_NQ_NP_753339-MLB69496967212_052023-O.webp',
      link: 'https://carro.mercadolivre.com.br/MLB-3646064094-mercedes-benz-c-200-avantgarde-20-tb-16v-184cv-aut-gasol-_JM#position=1&search_layout=grid&type=item&tracking_id=275c3a8f-d24f-4b99-b2ad-fea1bc5312ea',
      about: {
        color: 'Prateado',
        fuelType: 'Gasolina',
        doors: 4,
        streamingType: 'Automático',
      },
    },
  ])
})

// Inicia o servidor
app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`);
});
