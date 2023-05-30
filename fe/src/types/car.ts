export interface Car {
  id: number;
  name: string;
  image: string;
  location: string;
  kilometers: number;
  year: number;
  price: number;
  link: string;
  about: {
    color: string;
    fuelType: string;
    doors: number;
    streamingType: string;
  };
}
