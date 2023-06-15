import Header from './components/Header';
import CarsProvider from './contexts/useCars';

import ApplicationRoutes from './Routes';

function App() {
  return (
    <div
      className="
        bg-background
        min-h-screen
        
      "
    >
      <CarsProvider>
        <Header />

        <ApplicationRoutes />
      </CarsProvider>
    </div>
  );
}

export default App;
