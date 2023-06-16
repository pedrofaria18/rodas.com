/* eslint-disable @typescript-eslint/naming-convention */
/* eslint-disable no-underscore-dangle */
import axios from 'axios';

import formatCarsObject from '../utils/formatCarsObject';

const api = axios.create({
  baseURL: 'http://localhost:3000',
});

export const getCars = async (body: any) => {
  const response = await api.post('/cars', {
    size: 48,
    query: body
  });

  return formatCarsObject(response.data);
};

export const searchCars = async (search: string) => {
  const response = await api.post('/cars/search', { search });

  return formatCarsObject(response.data);
};
