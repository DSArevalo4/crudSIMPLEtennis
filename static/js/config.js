// Configuración de la aplicación
const CONFIG = {
  // Cambia esta URL según donde esté corriendo tu backend Flask
  API_URL: window.location.origin, // Usar la misma URL del navegador

  // Endpoints de la API
  ENDPOINTS: {
    LOGIN: "/api/auth/login",
    REGISTER: "/api/auth/register",
    TORNEOS: "/api/torneo",
    PARTIDOS: "/api/partido",
    USUARIOS: "/api/usuarios",
    INSCRIPCIONES: "/api/inscripcion",
    CUADRO: "/api/cuadro",
    NOTIFICACIONES: "/api/notificacion",
  },

  // Configuración de autenticación
  AUTH: {
    TOKEN_KEY: "tennis_auth_token",
    USER_KEY: "tennis_user_data",
  },
}

// Exportar configuración
if (typeof module !== "undefined" && module.exports) {
  module.exports = CONFIG
}
