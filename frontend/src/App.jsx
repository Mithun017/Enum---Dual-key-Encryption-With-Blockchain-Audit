import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Encryption from './components/Encryption';
import Decryption from './components/Decryption';
import Ledger from './components/Ledger';
import Alerts from './components/Alerts';
import SystemInfo from './components/SystemInfo';

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  if (!token) {
    return <Navigate to="/" replace />;
  }
  return children;
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        >
          <Route index element={<SystemInfo />} />
          <Route path="encrypt" element={<Encryption />} />
          <Route path="decrypt" element={<Decryption />} />
          <Route path="ledger" element={<Ledger />} />
          <Route path="alerts" element={<Alerts />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
