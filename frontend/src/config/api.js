// Central API configuration
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Add API key globally to all requests
axios.interceptors.request.use((config) => {
  // Use env var or default development key
  config.headers['X-API-Key'] = import.meta.env.VITE_API_KEY || 'rg_sec_9f8d7c6b5a41234567890abcdef';
  return config;
});

export default API_BASE;
