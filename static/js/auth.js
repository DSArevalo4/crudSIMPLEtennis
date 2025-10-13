// Authentication utilities
const AUTH_TOKEN_KEY = 'auth_token'
const USER_DATA_KEY = 'user_data'
const TOKEN_EXPIRY_KEY = 'token_expiry'

class Auth {
  constructor() {
    this.token = localStorage.getItem(AUTH_TOKEN_KEY)
    this.user = this.loadUser()
    this.tokenExpiry = localStorage.getItem(TOKEN_EXPIRY_KEY)
  }

  loadUser() {
    const userData = localStorage.getItem(USER_DATA_KEY)
    if (userData) {
      try {
        return JSON.parse(userData)
      } catch (e) {
        return null
      }
    }
    return null
  }

  setAuth(token, user) {
    this.token = token
    this.user = user
    
    // Calcular fecha de expiración (8 horas)
    const expiryDate = new Date()
    expiryDate.setHours(expiryDate.getHours() + 8)
    this.tokenExpiry = expiryDate.toISOString()
    
    // Guardar en localStorage
    localStorage.setItem(AUTH_TOKEN_KEY, token)
    localStorage.setItem(USER_DATA_KEY, JSON.stringify(user))
    localStorage.setItem(TOKEN_EXPIRY_KEY, this.tokenExpiry)
  }

  clearAuth() {
    this.token = null
    this.user = null
    this.tokenExpiry = null
    
    localStorage.removeItem(AUTH_TOKEN_KEY)
    localStorage.removeItem(USER_DATA_KEY)
    localStorage.removeItem(TOKEN_EXPIRY_KEY)
  }

  isAuthenticated() {
    if (!this.token) {
      return false
    }
    
    // Verificar si el token ha expirado
    if (this.tokenExpiry) {
      const now = new Date()
      const expiry = new Date(this.tokenExpiry)
      if (now > expiry) {
        this.clearAuth()
        return false
      }
    }
    
    return true
  }

  getUser() {
    return this.user
  }

  getToken() {
    return this.token
  }

  logout() {
    console.log('🚪 Cerrando sesión...')
    this.clearAuth()
    console.log('✅ Sesión cerrada')
    window.location.href = '/login'
  }

  redirectToLogin() {
    window.location.href = '/login'
  }

  redirectToDashboard() {
    window.location.href = '/dashboard'
  }
}

// Instancia global
const auth = new Auth()
