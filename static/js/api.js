// API service for communicating with Flask backend
class ApiService {
  constructor() {
    this.baseURL = CONFIG.API_URL
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    const token = auth.getToken()
    
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
      }
    }

    const config = {
      ...defaultOptions,
      ...options,
      headers: {
        ...defaultOptions.headers,
        ...options.headers
      }
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  // Auth endpoints
  async login(email, password) {
    return this.request(CONFIG.ENDPOINTS.LOGIN, {
      method: 'POST',
      body: JSON.stringify({ email, password })
    })
  }

  async register(userData) {
    return this.request(CONFIG.ENDPOINTS.REGISTER, {
      method: 'POST',
      body: JSON.stringify(userData)
    })
  }

  // Tournament endpoints
  async getTorneos() {
    return this.request(CONFIG.ENDPOINTS.TORNEOS)
  }

  async createTorneo(torneoData) {
    return this.request(CONFIG.ENDPOINTS.TORNEOS, {
      method: 'POST',
      body: JSON.stringify(torneoData)
    })
  }

  async updateTorneo(id, torneoData) {
    return this.request(`${CONFIG.ENDPOINTS.TORNEOS}/${id}`, {
      method: 'PUT',
      body: JSON.stringify(torneoData)
    })
  }

  async deleteTorneo(id) {
    return this.request(`${CONFIG.ENDPOINTS.TORNEOS}/${id}`, {
      method: 'DELETE'
    })
  }

  // User endpoints
  async getUsuarios() {
    return this.request(CONFIG.ENDPOINTS.USUARIOS)
  }

  async createUsuario(usuarioData) {
    return this.request(CONFIG.ENDPOINTS.USUARIOS, {
      method: 'POST',
      body: JSON.stringify(usuarioData)
    })
  }

  // Match endpoints
  async getPartidos() {
    return this.request(CONFIG.ENDPOINTS.PARTIDOS)
  }

  async createPartido(partidoData) {
    return this.request(CONFIG.ENDPOINTS.PARTIDOS, {
      method: 'POST',
      body: JSON.stringify(partidoData)
    })
  }

  // Inscription endpoints
  async getInscripciones() {
    return this.request(CONFIG.ENDPOINTS.INSCRIPCIONES)
  }

  async createInscripcion(inscripcionData) {
    return this.request(CONFIG.ENDPOINTS.INSCRIPCIONES, {
      method: 'POST',
      body: JSON.stringify(inscripcionData)
    })
  }

  // Dashboard stats
  async getDashboardStats() {
    return this.request('/api/dashboard/stats')
  }
}

// Create global API instance
const api = new ApiService()
