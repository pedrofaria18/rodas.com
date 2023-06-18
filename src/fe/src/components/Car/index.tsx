/* eslint-disable jsx-a11y/no-static-element-interactions */
/* eslint-disable jsx-a11y/click-events-have-key-events */
import PaintSVG from '../../assets/Paint.svg';
import FuelSVG from '../../assets/Fuel.svg';
import DoorSVG from '../../assets/Door.svg';
import CarShiftSVG from '../../assets/CarShift.svg';

import { Car as CarDTO } from '../../types/car';

type CarProps = {
  car: CarDTO;
};

export default function Car({ car }: CarProps) {
  const { title, image, price, edLink, kilometers, year, color, doors, fuelType, streamingType } = car;

  const formattedKilometers = kilometers ? new Intl.NumberFormat('pt-BR', {
    style: 'unit',
    unit: 'kilometer',
  }).format(kilometers) : ""

  return (
    <div
      className="
        flex
        flex-col
        w-[264px]
        pb-4
        cursor-pointer
      "
      onClick={() => window.open(edLink, '_blank')}
    >
      <img
        className="
          w-full
          h-[213px]
          rounded-t-lg
        "
        src={image}
        alt={title}
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
          <span>
            {formattedKilometers || "- km"}
          </span>
          <span> | </span>
          <span>
            {year || "Ano não informado"}
          </span>
        </p>
        <h1
          className="
                text-base
                font-bold
                text-gray-600
                truncate max-w-[30ch]
              "
        >
          {title}
        </h1>
        <div
          className="
            grid
            grid-cols-2
            grid-rows-2
            gap-4
          "
        >
          {color && (
              <div
              className="
                flex
                flex-row
                items-center
                gap-3
              "
            >
              <img src={PaintSVG} alt="Cor do carro" />
              <p
                className="
                  text-sm
                  font-medium
                  text-gray-400
                  "
              >
                {color}
              </p>
            </div>
          )}

          {doors && (
              <div
              className="
                flex
                flex-row
                items-center
                gap-3
              "
            >
              <img src={DoorSVG} alt="Quantidade de portas" />
              <p
                className="
                  text-sm
                  font-medium
                  text-gray-400
                  "
              >
                {doors}
              </p>
            </div>
          )}

          {fuelType && (
              <div
              className="
                flex
                flex-row
                items-center
                gap-3
              "
            >
              <img src={FuelSVG} alt="Tipo de combustível" />
              <p
                className="
                  text-sm
                  font-medium
                  text-gray-400
                  "
              >
                {fuelType}
              </p>
            </div>
          )}

          {streamingType && (
              <div
              className="
                flex
                flex-row
                items-center
                gap-3
              "
            >
              <img src={CarShiftSVG} alt="Câmbio do carro" />
              <p
                className="
                  text-sm
                  font-medium
                  text-gray-400
                  "
              >
                {streamingType}
              </p>
            </div>
          )}
        </div>
        <p
          className="
            text-[22px]
            font-semibold
            text-gray-500
          "
        >
          {price ? price : "Preço não informado"}
        </p>
      </div>
    </div>
  );
}
