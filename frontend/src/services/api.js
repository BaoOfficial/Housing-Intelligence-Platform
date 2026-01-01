import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Chat API
export const chatAPI = {
  sendMessage: async (message, conversationId = null) => {
    const response = await api.post('/api/v1/chat/message', {
      message,
      conversation_id: conversationId,
    });
    return response.data;
  },
};

// Properties API
export const propertiesAPI = {
  getProperties: async (filters = {}) => {
    const params = new URLSearchParams();

    if (filters.area) params.append('area', filters.area);
    if (filters.property_type) params.append('property_type', filters.property_type);
    if (filters.min_bedrooms) params.append('min_bedrooms', filters.min_bedrooms);
    if (filters.max_bedrooms) params.append('max_bedrooms', filters.max_bedrooms);
    if (filters.min_rent) params.append('min_rent', filters.min_rent);
    if (filters.max_rent) params.append('max_rent', filters.max_rent);
    if (filters.page) params.append('page', filters.page);
    if (filters.limit) params.append('limit', filters.limit);

    const response = await api.get(`/api/v1/properties?${params.toString()}`);
    return response.data;
  },

  getPropertyById: async (id) => {
    const response = await api.get(`/api/v1/properties/${id}`);
    return response.data;
  },
};

export default api;
