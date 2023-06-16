/* eslint-disable @typescript-eslint/naming-convention */

import { Car } from '../types/car';

/* eslint-disable no-underscore-dangle */
export default function formatCarsObject(cars: any) {
  const listCars: Car[] = cars.map((info: any) => {
    const { title, price, image, ed_link, ano, color, doors, fuelType, streamingType, kilometers } = info._source;

    return {
      title,
      price,
      image,
      edLink: ed_link,
      year: ano,
      color,
      doors,
      fuelType,
      streamingType,
      kilometers,
    };
  });

  return listCars;
}
