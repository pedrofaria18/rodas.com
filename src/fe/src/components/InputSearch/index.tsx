export default function InputSearch() {
  return (
    <div className="relative">
      <input
        className="
        w-[500px]
        py-2 pr-10 pl-4 rounded-lg
        text-base
        text-gray-400
        focus:outline-none focus:border-transparent"
        type="text"
        placeholder="Faça sua busca aqui"
      />
      <button className="absolute inset-y-0 right-0 px-3 flex items-center bg-transparent focus:outline-none">
        <svg
          className="h-5 w-5 text-gray-400"
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="2"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path d="M21 21l-4.35-4.35m-.61-7.61C15.28 6.28 12.7 5 10 5 5.58 5 2 8.58 2 13s3.58 8 8 8 8-3.58 8-8c0-2.7-1.28-5.28-3.35-6.96" />
        </svg>
      </button>
    </div>
  );
}
