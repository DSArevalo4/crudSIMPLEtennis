const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001/api';

const handleResponse = async (response) => {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Error desconocido' }));
    throw new Error(error.message || `HTTP error! status: ${response.status}`);
  }
  return response.json();
};

export const inscripcionesAPI = {
  getAll: async () => {
    const response = await fetch(`${API_BASE_URL}/inscripciones`);
    return handleResponse(response);
  },

  getById: async (id) => {
    const response = await fetch(`${API_BASE_URL}/inscripciones/${id}`);
    return handleResponse(response);
  },

  create: async (data) => {
    const response = await fetch(`${API_BASE_URL}/inscripciones`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  update: async (id, data) => {
    const response = await fetch(`${API_BASE_URL}/inscripciones/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  delete: async (id) => {
    const response = await fetch(`${API_BASE_URL}/inscripciones/${id}`, {
      method: 'DELETE',
    });
    return handleResponse(response);
  },
};
