import { useCars } from '../../contexts/useCars';
import { Car as CarType } from '../../types/car';

import Car from '../Car';
import Loader from '../Loader';

export default function CarList() {
  const { cars, isLoading } = useCars();

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
        <Car key={car.title} car={car} />
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
