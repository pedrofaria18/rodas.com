import { useEffect, useState } from 'react';

import { getCars } from '../../service';

import { Car as CarType } from '../../types/car';

import Car from '../Car';
import Loader from '../Loader';

export default function CarList() {
  const [cars, setCars] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function loadCars() {
      try {
        setIsLoading(true);

        const carsList = await getCars();

        setCars(carsList);
      } catch (error) {
        console.log(error);
      } finally {
        setIsLoading(false);
      }
    }

    loadCars();
  }, []);

  return (
    <div
      className="
        flex-wrap
        flex
        gap-4
        align-center
        px-6
      "
    >
      <Loader isLoading={isLoading} />

      {cars.map((car: CarType) => (
        <Car key={car.id} car={car} />
      ))}

      {cars.length === 0 && (
        <p
          className="
            text-center
            w-full
          "
        >
          Nenhum carro encontrado
        </p>
      )}
    </div>
  );
}
