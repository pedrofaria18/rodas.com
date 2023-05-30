import CarList from '../../components/CarList';
import { search } from '../../service/elastic';

export default function Home() {
  search();
  return (
    <div
      className="
      flex
      flex-row
      gap-4
      max-w-[1215px]
      m-auto
      pt-8
    "
    >
      <aside
        className="
         max-w-[294px]
        "
      >
        Filtros
      </aside>

      <main
        className="
        flex-1
        "
      >
        <CarList />
      </main>
    </div>
  );
}
