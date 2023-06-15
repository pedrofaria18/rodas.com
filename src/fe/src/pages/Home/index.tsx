import CarList from '../../components/CarList';

export default function Home() {
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
      {/* <aside
        className="
         max-w-[294px]
        "
      >
        Filtros
      </aside> */}

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
