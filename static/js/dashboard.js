// Dashboard functionality
document.addEventListener('DOMContentLoaded', function() {
  // Check authentication
  if (!auth.requireAuth()) {
    return
  }

  const logoutBtn = document.getElementById('logoutBtn')
  const userAvatar = document.getElementById('userAvatar')
  const userName = document.getElementById('userName')
  const userEmail = document.getElementById('userEmail')
  const userBadge = document.getElementById('userBadge')
  const userTournaments = document.getElementById('userTournaments')
  const userMatches = document.getElementById('userMatches')

  // Logout functionality
  if (logoutBtn) {
    logoutBtn.addEventListener('click', function(e) {
      e.preventDefault()
      auth.logout()
    })
  }

  // Load user data
  function loadUserData() {
    const user = auth.getUser()
    if (user) {
      userName.textContent = `${user.nombre} ${user.apellido}`
      userEmail.textContent = user.email
      
      // Set user badge based on profile
      const badgeText = user.perfil === 'administrador' ? 'Administrador' : 
                       user.perfil === 'profesor' ? 'Profesor' : 'Deportista'
      userBadge.textContent = badgeText
      
      // Update avatar
      userAvatar.src = `https://api.dicebear.com/7.x/avataaars/svg?seed=${user.username}`
    }
  }

  // Load dashboard stats
  async function loadDashboardStats() {
    try {
      console.log('Cargando estadísticas del dashboard...')
      const response = await api.request('/api/dashboard/stats', 'GET')
      console.log('Respuesta recibida:', response)
      
      if (response.success && response.data) {
        const stats = response.data
        console.log('Datos parseados:', stats)
        
        // Actualizar estadísticas del usuario en el header
        if (stats.user) {
          userName.textContent = `${stats.user.nombre} ${stats.user.apellido}`
          userEmail.textContent = stats.user.email
        }
        
        // Actualizar próximo partido
        updateNextMatch(stats.nextMatch)
        
        // Actualizar estadísticas del sistema
        updateSystemStats(stats.systemStats)
      } else {
        console.error('Error en la respuesta:', response.message)
      }
    } catch (error) {
      console.error('Error loading dashboard stats:', error)
    }
  }

  // Actualizar estadísticas del sistema
  function updateSystemStats(systemStats) {
    console.log('updateSystemStats llamado con:', systemStats)
    
    if (!systemStats) {
      console.warn('systemStats es null o undefined')
      return
    }
    
    // Torneos Activos
    const torneosActivosEl = document.getElementById('activeTournaments')
    if (torneosActivosEl) {
      torneosActivosEl.textContent = systemStats.torneosActivos || 0
      console.log('Torneos activos:', systemStats.torneosActivos)
      createSparkline('torneosSparkline', [1, 2, 1, 3, 2, systemStats.torneosActivos || 0], '#ff8c42')
    }
    
    // Partidos Jugados
    const partidosEl = document.getElementById('matchesPlayed')
    if (partidosEl) {
      partidosEl.textContent = systemStats.partidosJugados || 0
      console.log('Partidos jugados:', systemStats.partidosJugados)
      const val = systemStats.partidosJugados || 0
      createSparkline('partidosSparkline', [Math.max(0, val-4), Math.max(0, val-3), Math.max(0, val-2), Math.max(0, val-1), val, val], '#4169e1')
    }
    
    // Actividad de Torneos (torneos del mes)
    const actividadEl = document.getElementById('tournamentActivity')
    if (actividadEl) {
      actividadEl.textContent = systemStats.torneosMes || 0
      console.log('Torneos del mes:', systemStats.torneosMes)
    }
    
    // Deportistas Registrados
    const deportistasEl = document.getElementById('registeredPlayers')
    if (deportistasEl) {
      deportistasEl.textContent = systemStats.totalDeportistas || 0
      console.log('Total deportistas:', systemStats.totalDeportistas)
      const val = systemStats.totalDeportistas || 0
      createSparkline('deportistasSparkline', [Math.max(0, val-3), Math.max(0, val-2), Math.max(0, val-1), val, val, val+1], '#ffd700')
    }
    
    // Tasa de Participación
    const tasaEl = document.getElementById('participationRate')
    if (tasaEl) {
      tasaEl.textContent = `${systemStats.tasaParticipacion || 0}%`
      console.log('Tasa participación:', systemStats.tasaParticipacion)
      const tasa = systemStats.tasaParticipacion || 0
      createSparkline('participacionSparkline', [Math.max(0, tasa-15), Math.max(0, tasa-10), Math.max(0, tasa-5), tasa, tasa, tasa], '#10b981')
    }
    
    // Subtexto de participación
    const subtextEl = document.getElementById('participationSubtext')
    if (subtextEl) {
      const deportistas_activos = Math.round((systemStats.totalDeportistas || 0) * (systemStats.tasaParticipacion || 0) / 100)
      subtextEl.textContent = `${deportistas_activos} de ${systemStats.totalDeportistas || 0}`
    }
  }
  
  // Crear gráfico sparkline
  function createSparkline(canvasId, data, color) {
    const canvas = document.getElementById(canvasId)
    if (!canvas) return
    
    const ctx = canvas.getContext('2d')
    const width = canvas.width
    const height = canvas.height
    
    // Limpiar canvas
    ctx.clearRect(0, 0, width, height)
    
    // Encontrar min y max
    const max = Math.max(...data, 1)
    const min = Math.min(...data, 0)
    const range = max - min || 1
    
    // Calcular puntos
    const points = data.map((value, index) => ({
      x: (index / (data.length - 1)) * width,
      y: height - ((value - min) / range) * (height - 4) - 2
    }))
    
    // Dibujar área bajo la línea
    ctx.beginPath()
    ctx.moveTo(points[0].x, height)
    points.forEach(point => ctx.lineTo(point.x, point.y))
    ctx.lineTo(points[points.length - 1].x, height)
    ctx.closePath()
    
    const gradient = ctx.createLinearGradient(0, 0, 0, height)
    gradient.addColorStop(0, color + '40')
    gradient.addColorStop(1, color + '00')
    ctx.fillStyle = gradient
    ctx.fill()
    
    // Dibujar línea
    ctx.beginPath()
    ctx.moveTo(points[0].x, points[0].y)
    points.forEach(point => ctx.lineTo(point.x, point.y))
    ctx.strokeStyle = color
    ctx.lineWidth = 2
    ctx.stroke()
  }
  
  // Actualizar próximo partido
  function updateNextMatch(nextMatch) {
    const container = document.querySelector('.next-match-container')
    if (!container) return
    
    if (!nextMatch) {
      container.innerHTML = '<div class="next-match-card"><p style="text-align: center; color: #666;">No tienes partidos programados</p></div>'
      return
    }
    
    const fecha = nextMatch.fecha ? new Date(nextMatch.fecha).toLocaleDateString('es-ES', {
      day: '2-digit',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }) : 'Fecha por definir'
    
    container.innerHTML = `
      <div class="next-match-card">
        <div class="match-header">
          <span class="tournament-badge">${nextMatch.torneo}</span>
          <span class="round-badge">${nextMatch.ronda || 'Por definir'}</span>
        </div>
        <div class="match-opponent">
          <div class="opponent-flag">${nextMatch.rival.pais || '🌍'}</div>
          <div class="opponent-info">
            <h4>${nextMatch.rival.nombre}</h4>
            <p class="match-date">${fecha}</p>
          </div>
        </div>
      </div>
    `
  }
  
  // Actualizar gráfico con datos reales (eliminado - no se usa)
  
  // Actualizar estadísticas globales (eliminado - no se usa)
  
  // Actualizar rankings (eliminado - no se usa)

  // Set date inputs to current month
  function setDefaultDates() {
    const now = new Date()
    const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1)
    const endOfMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0)
    
    document.getElementById('startDate').value = startOfMonth.toISOString().split('T')[0]
    document.getElementById('endDate').value = endOfMonth.toISOString().split('T')[0]
  }

  // Initialize dashboard
  function initDashboard() {
    loadUserData()
    loadDashboardStats()
    setDefaultDates()
  }

  // Start the dashboard
  initDashboard()
})

