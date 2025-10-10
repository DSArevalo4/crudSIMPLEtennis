// Configuración de seguridad específica para la página de login
// Este archivo se carga solo en la página de login para evitar bucles

// Versión simplificada del objeto auth para la página de login
const AUTH_TOKEN_KEY = "auth_token"
const USER_DATA_KEY = "user_data"
const TOKEN_EXPIRY_KEY = "token_expiry"

// Objeto auth simplificado para la página de login
const auth = {
    token: localStorage.getItem(AUTH_TOKEN_KEY),
    user: JSON.parse(localStorage.getItem(USER_DATA_KEY) || "null"),
    tokenExpiry: localStorage.getItem(TOKEN_EXPIRY_KEY),

    isAuthenticated() {
        if (!this.token) return false
        
        // Verificar expiración local
        if (this.tokenExpiry && new Date() > new Date(this.tokenExpiry)) {
            this.clearAuth()
            return false
        }
        
        return true
    },

    getToken() {
        return this.token
    },

    getUser() {
        return this.user
    },

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
    },

    redirectToDashboard() {
        // Redirigir al dashboard con URL limpia
        history.replaceState(null, null, '/')
        window.location.href = "/dashboard"
    },

    clearAuth() {
        this.token = null
        this.user = null
        this.tokenExpiry = null
        localStorage.removeItem(AUTH_TOKEN_KEY)
        localStorage.removeItem(USER_DATA_KEY)
        localStorage.removeItem(TOKEN_EXPIRY_KEY)
    },

    logout() {
        this.clearAuth()
        window.location.href = "/login"
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Verificar si ya hay un token válido
    if (auth.isAuthenticated()) {
        // Token válido, redirigir al dashboard
        window.location.href = '/dashboard';
        return;
    }
    
    // Configurar protección básica para la página de login
    setupLoginProtection();
});

function setupLoginProtection() {
    // Limpiar URL para que no muestre /login
    if (window.location.pathname === '/login') {
        history.replaceState(null, null, '/');
    }
    
    // Prevenir acceso directo a URLs protegidas desde la página de login
    window.addEventListener('beforeunload', function() {
        // No limpiar datos aquí para mantener la sesión si el usuario navega
    });
    
    // Detectar intentos de navegación hacia atrás desde el login
    window.addEventListener('popstate', function(event) {
        // Si el usuario intenta navegar hacia atrás desde el login,
        // redirigir a la página principal
        if (window.location.pathname !== '/login' && window.location.pathname !== '/') {
            history.replaceState(null, null, '/');
            window.location.href = '/login';
        }
    });
    
    // Agregar estado inicial al historial con URL limpia
    history.pushState(null, null, '/');
}
