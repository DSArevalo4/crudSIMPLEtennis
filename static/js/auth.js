// Authentication utilities
const AUTH_TOKEN_KEY = "auth_token"
const USER_DATA_KEY = "user_data"
const TOKEN_EXPIRY_KEY = "token_expiry"

class AuthService {
  constructor() {
    this.token = localStorage.getItem(AUTH_TOKEN_KEY)
    this.user = JSON.parse(localStorage.getItem(USER_DATA_KEY) || "null")
    this.tokenExpiry = localStorage.getItem(TOKEN_EXPIRY_KEY)
    this.initSecurity()
  }

  initSecurity() {
    // Solo aplicar seguridad si NO estamos en la página de login
    if (window.location.pathname === '/login' || window.location.pathname === '/') {
      return // No aplicar seguridad en la página de login
    }
    
    // Limpiar URL para que no muestre /dashboard
    this.cleanUrl()
    
    // Prevenir navegación hacia atrás
    this.preventBackNavigation()
    
    // Verificar token periódicamente
    this.startTokenValidation()
    
    // Limpiar datos al cerrar ventana/pestaña
    this.setupCleanup()
  }

  cleanUrl() {
    // Limpiar la URL para que no muestre /dashboard
    if (window.location.pathname === '/dashboard') {
      history.replaceState(null, null, '/')
    }
  }

  preventBackNavigation() {
    // Prevenir el botón atrás del navegador
    window.addEventListener('popstate', (event) => {
      if (this.isAuthenticated()) {
        // Si está autenticado, prevenir navegación hacia atrás
        history.pushState(null, null, '/')
        event.preventDefault()
      }
    })

    // Agregar estado inicial al historial con URL limpia
    if (this.isAuthenticated()) {
      history.pushState(null, null, '/')
    }
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
    // Limpiar datos al cerrar ventana/pestaña
    window.addEventListener('beforeunload', () => {
      // Solo limpiar si el usuario cierra completamente la ventana
      if (event.type === 'beforeunload') {
        this.clearAuth()
      }
    })

    // Detectar cuando la pestaña se vuelve inactiva
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        // Pausar validaciones cuando la pestaña no está activa
        this.pauseValidation = true
      } else {
        // Reanudar validaciones cuando la pestaña vuelve a estar activa
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
    
    // Redirigir al dashboard con URL limpia
    this.redirectToDashboard()
  }

  redirectToDashboard() {
    // Redirigir al dashboard con URL limpia
    history.replaceState(null, null, '/')
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
    // Limpiar historial y redirigir
    history.replaceState(null, null, '/')
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
}

// Create global auth instance
const auth = new AuthService()
