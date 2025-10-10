// Authentication utilities
const AUTH_TOKEN_KEY = "auth_token"
const USER_DATA_KEY = "user_data"

class AuthService {
  constructor() {
    this.token = localStorage.getItem(AUTH_TOKEN_KEY)
    this.user = JSON.parse(localStorage.getItem(USER_DATA_KEY) || "null")
  }

  isAuthenticated() {
    return !!this.token
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
    localStorage.setItem(AUTH_TOKEN_KEY, token)
    localStorage.setItem(USER_DATA_KEY, JSON.stringify(user))
  }

  clearAuth() {
    this.token = null
    this.user = null
    localStorage.removeItem(AUTH_TOKEN_KEY)
    localStorage.removeItem(USER_DATA_KEY)
  }

  logout() {
    this.clearAuth()
    window.location.href = "/login"
  }

  requireAuth() {
    if (!this.isAuthenticated()) {
      window.location.href = "/login"
      return false
    }
    return true
  }
}

// Create global auth instance
const auth = new AuthService()
