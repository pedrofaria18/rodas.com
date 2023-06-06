import { useEffect } from 'react';

import axios from 'axios';

import Header from './components/Header';

import ApplicationRoutes from './Routes';

function App() {
  useEffect(() => {
    axios.get('/api/ed/_search').then(res => {
      console.log(res.data)
    }).catch(err => {
      console.log(err)
    })
  }, [])

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
