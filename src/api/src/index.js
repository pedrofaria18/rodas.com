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

app.get('/cars', async (req, res) => {
  try {
    const response = await axios.post('http://localhost:9200/ed/_search', {
      query: {
        match_all: {},
      },
    });

    res.json(response.data.hits.hits)
  } catch (error) {
    console.error(error);
  }
})

// Inicia o servidor
app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`);
});

async function getCars() {
  try {
    const response = await axios.post('http://localhost:9200/ed/_search', {
      query: {
        match_all: {},
      },
    });

    console.log(response.data.hits.hits);
  } catch (error) {
    console.error(error);
  }
}

getCars();