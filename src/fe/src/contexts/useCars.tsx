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
    async (body?: any) => {
      try {
        setIsLoading(true);

        const carsList = body ? await getCars(body) : await getCars({
          "match_all": {}
        });

        setCars(carsList);
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  useEffect(() => {
    loadCars();
  }, [loadCars]);

  const searchCars = () => {
    setCars([])

    if (search) {
      loadCars({ "match": {
        global: search
      }});
    } else {
      loadCars({
        "match_all": {}
      });
    }
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
