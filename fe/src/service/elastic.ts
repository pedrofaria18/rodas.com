import axios from 'axios';

const elasticURL = 'http://localhost:9200';

export async function search() {
  const response = await axios.post(`${elasticURL}/ed/_search`, {
    params: {},
  });

  console.log(response);
}
