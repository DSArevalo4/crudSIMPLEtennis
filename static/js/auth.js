// Authentication utilities
const AUTH_TOKEN_KEY = "auth_token"
const USER_DATA_KEY = "user_data"
const TOKEN_EXPIRY_KEY = "token_expiry"

class AuthService {
  constructor() {
    this.token = localStorage.getItem(AUTH_TOKEN_KEY)
    this.user = JSON.parse(localStorage.getItem(USER_DATA_KEY) || "null")
    this.tokenExpiry = localStorage.getItem(TOKEN_EXPIRY_KEY)
    this.pauseValidation = false
    this.initSecurity()
  }

  initSecurity() {
    // Solo aplicar seguridad si NO estamos en la página de login
    if (window.location.pathname === '/login' || window.location.pathname === '/') {
      return
    }
    
    // Verificar token periódicamente
    this.startTokenValidation()
    
    // Limpiar datos al cerrar ventana/pestaña
    this.setupCleanup()
  }

  startTokenValidation() {
    // Verificar token cada 5 minutos
    setInterval(() => {
      this.validateToken()
    }, 5 * 60 * 1000) // 5 minutos

    // Verificar inmediatamente solo si no estamos en la página principal
    if (window.location.pathname !== '/') {
      this.validateToken()
    }
  }

  async validateToken() {
    // No validar token en la página de login
    if (window.location.pathname === '/login' || window.location.pathname === '/') {
      return true
    }

    if (!this.token) {
      // Solo redirigir si no estamos en la página principal
      if (window.location.pathname !== '/') {
        this.redirectToLogin()
      }
      return false
    }

    // Verificar expiración local
    if (this.tokenExpiry && new Date() > new Date(this.tokenExpiry)) {
      this.clearAuth()
      this.redirectToLogin()
      return false
    }

    try {
      // Verificar token con el servidor
      const response = await fetch('/api/auth/verify-token', {
        headers: {
          'Authorization': `Bearer ${this.token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        // Solo limpiar auth si es un error de autenticación real
        if (response.status === 401 || response.status === 403) {
          this.clearAuth()
          this.redirectToLogin()
        }
        return false
      }

      return true
    } catch (error) {
      console.error('Error validando token:', error)
      // No redirigir en caso de error de red
      // Solo retornar false para que se mantenga la sesión local
      return false
    }
  }

  setupCleanup() {
    // Detectar cuando la pestaña se vuelve inactiva
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        this.pauseValidation = true
      } else {
        this.pauseValidation = false
        this.validateToken()
      }
    })
  }

  isAuthenticated() {
    if (!this.token) return false
    
    // Verificar expiración local
    if (this.tokenExpiry && new Date() > new Date(this.tokenExpiry)) {
      this.clearAuth()
      return false
    }
    
    return true
  }

  // Nueva función para verificar autenticación sin redirección
  isAuthenticatedSilent() {
    if (!this.token) return false
    
    // Verificar expiración local
    if (this.tokenExpiry && new Date() > new Date(this.tokenExpiry)) {
      return false
    }
    
    return true
  }

  getToken() {
    return this.token
  }

  getUser() {
    return this.user
  }

  setAuth(token, user) {
    this.token = token
    this.user = user
    
    // Calcular expiración (8 horas desde ahora)
    const expiry = new Date()
    expiry.setHours(expiry.getHours() + 8)
    
    localStorage.setItem(AUTH_TOKEN_KEY, token)
    localStorage.setItem(USER_DATA_KEY, JSON.stringify(user))
    localStorage.setItem(TOKEN_EXPIRY_KEY, expiry.toISOString())
    
    this.tokenExpiry = expiry.toISOString()
    
    // Redirigir al dashboard
    window.location.href = "/dashboard"
  }

  redirectToDashboard() {
    window.location.href = "/dashboard"
  }

  clearAuth() {
    this.token = null
    this.user = null
    this.tokenExpiry = null
    localStorage.removeItem(AUTH_TOKEN_KEY)
    localStorage.removeItem(USER_DATA_KEY)
    localStorage.removeItem(TOKEN_EXPIRY_KEY)
  }

  logout() {
    this.clearAuth()
    this.redirectToLogin()
  }

  redirectToLogin() {
    window.location.href = "/login"
  }

  requireAuth() {
    // No requerir autenticación en la página de login
    if (window.location.pathname === '/login' || window.location.pathname === '/') {
      return true
    }
    
    if (!this.isAuthenticatedSilent()) {
      this.redirectToLogin()
      return false
    }
    return true
  }

  // Método helper para agregar el token a las peticiones fetch
  async fetchWithAuth(url, options = {}) {
    if (!this.token) {
      throw new Error('No hay token de autenticación')
    }

    const headers = {
      ...options.headers,
      'Authorization': `Bearer ${this.token}`,
      'Content-Type': 'application/json'
    }

    const response = await fetch(url, {
      ...options,
      headers
    })

    // Si el token expiró, limpiar y redirigir
    if (response.status === 401) {
      this.clearAuth()
      this.redirectToLogin()
      throw new Error('Sesión expirada')
    }

    return response
  }
}

// Create global auth instance
const auth = new AuthService()
