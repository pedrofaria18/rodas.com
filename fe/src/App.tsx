import Header from './components/Header';

import ApplicationRoutes from './Routes';

function App() {
  return (
    <div
      className="
        bg-background
        min-h-screen
        
      "
    >
      <Header />

      <ApplicationRoutes />
    </div>
  );
}

export default App;
