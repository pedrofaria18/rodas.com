import { cars } from '../../mocks/cars';
import Car from '../Car';

export default function CarList() {
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
      {cars.map((car) => (
        <Car key={car.id} car={car} />
      ))}
    </div>
  );
}
