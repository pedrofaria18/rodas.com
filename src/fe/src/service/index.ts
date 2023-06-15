import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:3000',
});

export const getCars = async () => {
  const response = await api.get('/cars');

  const listCars = response.data.map((info: any) => {
    const {
      title, price, image, ed_link
    } = info["_source"]

    return {
      title, price, image, ed_link
    }
  })
  return listCars;
};
