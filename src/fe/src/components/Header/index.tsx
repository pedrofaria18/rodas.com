import LogoSecondarySVG from '../../assets/LogoSecondary.svg';

import InputSearch from '../InputSearch';

export default function Header() {
  return (
    <header
      className="
        w-full 
        h-[67.33px]
        bg-blue-dark
        flex
      "
    >
      <div
        className="
          w-full
          max-w-[1215px]
          mx-auto
          flex
          items-center
        "
      >
        <img
          src={LogoSecondarySVG}
          alt="Logo Aldo Imóveis"
          className="w-[200px] mr-48"
        />

        <InputSearch />
      </div>
    </header>
  );
}
