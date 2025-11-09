import axios from 'axios';

// Use optional chaining and provide fallback
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // Add 30 second timeout
});

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export interface ResearchRequest {
  topic: string;
  use_wikipedia?: boolean;
  use_arxiv?: boolean;
  max_wikipedia_articles?: number;
  max_arxiv_papers?: number;
  data_source?: 'arxiv' | 'wikipedia';
  max_results?: number;
}

export interface ResearchResponse {
  status: string;
  message: string;
  report?: any;
}

export interface HealthResponse {
  status: string;
  message: string;
}

export interface ConfigResponse {
  api_key_configured: boolean;
  max_results: number;
  [key: string]: any;
}

export const researchAPI = {
  // Health check
  health: async (): Promise<HealthResponse> => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  },

  // Start research (alias for compatibility)
  research: async (data: ResearchRequest): Promise<ResearchResponse> => {
    try {
      const response = await api.post('/research', data);
      return response.data;
    } catch (error) {
      console.error('Research request failed:', error);
      throw error;
    }
  },

  // Start research
  startResearch: async (data: ResearchRequest): Promise<ResearchResponse> => {
    try {
      const response = await api.post('/research', data);
      return response.data;
    } catch (error) {
      console.error('Research request failed:', error);
      throw error;
    }
  },

  // Reinitialize system
  reinitialize: async (): Promise<{ status: string; message: string }> => {
    try {
      const response = await api.post('/reinitialize');
      return response.data;
    } catch (error) {
      console.error('Reinitialize failed:', error);
      throw error;
    }
  },

  // Get configuration
  getConfig: async (): Promise<ConfigResponse> => {
    try {
      const response = await api.get('/config');
      return response.data;
    } catch (error) {
      console.error('Get config failed:', error);
      throw error;
    }
  },
};

export default api;
