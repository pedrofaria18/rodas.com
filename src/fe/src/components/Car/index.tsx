import PaintSVG from '../../assets/Paint.svg';
import FuelSVG from '../../assets/Fuel.svg';
import DoorSVG from '../../assets/Door.svg';
import CarShiftSVG from '../../assets/CarShift.svg';

import { Car as CarDTO } from '../../types/car';

type CarProps = {
  car: CarDTO;
};

export default function Car({ car }: CarProps) {
  const { name, image, kilometers, year, about, price, location } = car;

  const formattedKilometers = new Intl.NumberFormat('pt-BR', {
    style: 'unit',
    unit: 'kilometer',
  }).format(kilometers);

  const formattedPrice = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(price);

  const items = [
    {
      icon: PaintSVG,
      iconAlt: 'Ícone de cor',
      title: about.color,
    },
    {
      icon: DoorSVG,
      iconAlt: 'Ícone de porta',
      title: about.doors,
    },
    {
      icon: FuelSVG,
      iconAlt: 'Ícone de combustível',
      title: about.fuelType,
    },

    {
      icon: CarShiftSVG,
      iconAlt: 'Ícone de tipo de transmissão',
      title: about.streamingType,
    },
  ];

  return (
    <div
      className="
        flex
        flex-col
        w-[264px]
        pb-4
      "
    >
      <img
        className="
          w-full
          h-[213px]
          rounded-t-lg
        "
        src={image}
        alt={name}
      />
      <div
        className="
          flex
          flex-col
          gap-4
          p-4
          border-b-[1px]
          border-l-[1px]
          border-r-[1px]
          border-gray-100
          rounded-b-lg

        "
      >
        <p
          className="
            text-sm
            font-medium
            text-gray-500
            "
        >
          {formattedKilometers} | {year}
        </p>
        <h1
          className="
                text-base
                font-bold
                text-gray-600
              "
        >
          {name}
        </h1>
        <div
          className="
            grid
            grid-cols-2
            grid-rows-2
            gap-4
          "
        >
          {items.map((item) => (
            <div
              className="
                flex
                flex-row
                items-center
                gap-3
              "
              key={item.title}
            >
              <img src={item.icon} alt={item.iconAlt} />
              <p
                className="
                  text-sm
                  font-medium
                  text-gray-400
                "
              >
                {item.title}
              </p>
            </div>
          ))}
        </div>
        <p
          className="
            text-[22px]
            font-semibold
            text-gray-500
          "
        >
          {formattedPrice}
        </p>
        <p
          className="
            text-xs
            font-normal
            text-gray-300
          "
        >
          {location}
        </p>
      </div>
    </div>
  );
}
