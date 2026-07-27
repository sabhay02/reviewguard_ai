import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import axios from 'axios'
import './index.css'
import App from './App.jsx'

// Global Axios Interceptor for API Authentication
axios.interceptors.request.use((config) => {
  console.log("Loaded API Key from env:", import.meta.env.VITE_API_KEY);
  const apiKey = import.meta.env.VITE_API_KEY || 'dev-secret-key';
  config.headers['X-API-Key'] = apiKey;
  return config;
});

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
