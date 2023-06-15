/* eslint-disable react/jsx-no-constructed-context-values */
import {
  ReactNode,
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from 'react';

import { getCars } from '../service';

import { Car } from '../types/car';

interface ICarsData {
  cars: Car[];
  setCars: (cars: Car[]) => void;
  search: string;
  setSearch: (search: string) => void;
  isLoading: boolean;
  searchCars: () => void;
}

const CarsContext = createContext({} as ICarsData);

export default function CarsProvider({ children }: { children: ReactNode }) {
  const [cars, setCars] = useState<Car[]>([]);
  const [search, setSearch] = useState<string>('');

  const [isLoading, setIsLoading] = useState(false);

  const loadCars = useCallback(
    async (body?: Record<string, string>) => {
      try {
        setIsLoading(true);

        const carsList = body ? await getCars(body) : await getCars();

        setCars(carsList);
      } finally {
        setIsLoading(false);
      }
    },
    [setCars]
  );

  useEffect(() => {
    loadCars();
  }, [loadCars]);

  const searchCars = () => {
    loadCars({ global: search });
  };

  return (
    <CarsContext.Provider
      value={{ cars, setCars, search, setSearch, isLoading, searchCars }}
    >
      {children}
    </CarsContext.Provider>
  );
}

export const useCars = () => useContext(CarsContext);
