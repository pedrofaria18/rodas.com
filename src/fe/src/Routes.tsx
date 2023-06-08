import { Route, Routes } from 'react-router-dom';

import Home from './pages/Home';

export default function ApplicationRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
    </Routes>
  );
}
