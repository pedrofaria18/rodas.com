const express = require('express');
const axios = require('axios');

const cors = require('./middlewares/cors');

const app = express();
const port = 3000;

app.use(express.json());
app.use(cors);

app.post('/cars', async (req, res) => {
  try {
    const response = await axios.post('http://localhost:9200/ed/_search', req.body);

    res.json(response.data.hits.hits)
  } catch (error) {
    console.error(error);
  }
})

app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`);
});