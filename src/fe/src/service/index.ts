import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:3000',
});

export const getCars = async () => {
  const response = await api.get('/cars');
  return response.data;
};
