// Gestor de URLs para evitar parpadeo y mantener URLs limpias
class URLManager {
  constructor() {
    this.init()
  }

  init() {
    // Limpiar URL inmediatamente al cargar
    this.cleanUrlImmediately()
    
    // Configurar listeners para mantener URLs limpias
    this.setupUrlListeners()
  }

  cleanUrlImmediately() {
    // Limpiar URL inmediatamente para evitar parpadeo
    const currentPath = window.location.pathname
    
    if (currentPath === '/dashboard' || currentPath === '/login') {
      // Usar replaceState para no crear entrada en el historial
      history.replaceState(null, null, '/')
    }
  }

  setupUrlListeners() {
    // Prevenir cambios de URL que muestren rutas internas
    window.addEventListener('popstate', (event) => {
      this.handlePopState(event)
    })

    // Interceptar navegación programática
    this.interceptNavigation()
  }

  handlePopState(event) {
    const currentPath = window.location.pathname
    
    // Si la URL muestra rutas internas, limpiarla
    if (currentPath === '/dashboard' || currentPath === '/login') {
      history.replaceState(null, null, '/')
    }
  }

  interceptNavigation() {
    // Interceptar window.location.href
    const originalLocation = window.location
    const originalHref = Object.getOwnPropertyDescriptor(originalLocation, 'href')
    
    Object.defineProperty(window.location, 'href', {
      get: originalHref.get,
      set: (url) => {
        // Limpiar URL antes de navegar
        const cleanUrl = this.cleanUrl(url)
        originalHref.set.call(originalLocation, cleanUrl)
      }
    })
  }

  cleanUrl(url) {
    // Limpiar URL para que no muestre rutas internas
    if (url.includes('/dashboard')) {
      return url.replace('/dashboard', '/')
    }
    if (url.includes('/login')) {
      return url.replace('/login', '/')
    }
    return url
  }

  // Método para navegar con URL limpia
  navigateTo(url) {
    const cleanUrl = this.cleanUrl(url)
    history.replaceState(null, null, '/')
    window.location.href = cleanUrl
  }
}

// Crear instancia global
const urlManager = new URLManager()
