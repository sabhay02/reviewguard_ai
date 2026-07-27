import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import ReportView from './pages/ReportView';
import ScannerPage from './pages/ScannerPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/scan" element={<ScannerPage />} />
        <Route path="/report/:id" element={<ReportView />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
