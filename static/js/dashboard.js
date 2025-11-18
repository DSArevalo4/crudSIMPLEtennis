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
      const stats = await api.getDashboardStats()
      updateStats(stats)
      
      // Actualizar próximo partido
      updateNextMatch(stats.nextMatch)
      
      // Actualizar gráfico con datos reales
      updateChart(stats.monthlyStats)
      
      // Actualizar estadísticas globales
      updateGlobalStats(stats.globalStats)
      
      // Actualizar rankings
      updateRankings(stats.rankings)
      
    } catch (error) {
      console.error('Error loading dashboard stats:', error)
      // Load default stats if API fails
      loadDefaultStats()
    }
  }

  // Update stats display
  function updateStats(stats) {
    // Estadísticas del usuario
    if (stats.globalStats) {
      userTournaments.textContent = stats.globalStats.torneos || 0
      userMatches.textContent = stats.globalStats.totalPartidos || 0
    }
    
    // Mantener estadísticas generales si existen
    if (stats.activeTournaments !== undefined) {
      document.getElementById('activeTournaments').textContent = stats.activeTournaments || 0
      document.getElementById('totalMatches').textContent = stats.totalMatches || 0
      document.getElementById('participationRate').textContent = `${stats.participationRate || 0}%`
      document.getElementById('totalPlayers').textContent = stats.totalPlayers || 0
      document.getElementById('pendingInscriptions').textContent = stats.pendingInscriptions || 0
      document.getElementById('completionRate').textContent = `${stats.completionRate || 0}%`
      document.getElementById('avgMatchDuration').textContent = stats.avgMatchDuration || 0
    }
  }
  
  // Actualizar próximo partido
  function updateNextMatch(nextMatch) {
    const container = document.querySelector('.next-match-container')
    if (!container) return
    
    if (!nextMatch) {
      container.innerHTML = '<p class="no-match">No tienes partidos programados</p>'
      return
    }
    
    const fecha = nextMatch.fecha ? new Date(nextMatch.fecha).toLocaleDateString('es-ES', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    }) : 'Fecha por definir'
    
    container.innerHTML = `
      <div class="next-match-card">
        <div class="match-info">
          <span class="match-tournament">${nextMatch.torneo}</span>
          <span class="match-round">${nextMatch.ronda || 'Primera Ronda'}</span>
        </div>
        <div class="match-players">
          <div class="player-vs">
            <span class="vs-text">VS</span>
          </div>
          <div class="rival-info">
            <span class="rival-name">${nextMatch.rival.nombre}</span>
            ${nextMatch.rival.pais ? `<span class="rival-country">${nextMatch.rival.pais}</span>` : ''}
          </div>
        </div>
        <div class="match-date">
          📅 ${fecha}
        </div>
      </div>
    `
  }
  
  // Actualizar gráfico con datos reales
  function updateChart(monthlyStats) {
    if (!monthlyStats || monthlyStats.length === 0) {
      return
    }
    
    const ctx = document.getElementById('activityChart')
    if (!ctx) return

    const labels = monthlyStats.map(m => m.mes)
    const partidos = monthlyStats.map(m => m.partidos)
    const victorias = monthlyStats.map(m => m.victorias)

    new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Partidos Jugados',
          data: partidos,
          borderColor: '#4169e1',
          backgroundColor: 'rgba(65, 105, 225, 0.1)',
          tension: 0.4
        }, {
          label: 'Victorias',
          data: victorias,
          borderColor: '#10b981',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          tension: 0.4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'bottom'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            }
          },
          x: {
            grid: {
              display: false
            }
          }
        }
      }
    })
  }
  
  // Actualizar estadísticas globales
  function updateGlobalStats(globalStats) {
    if (!globalStats) return
    
    const container = document.querySelector('.global-stats-container')
    if (!container) return
    
    const winRate = globalStats.winRate || 0
    const victorias = globalStats.victorias || 0
    const derrotas = globalStats.derrotas || 0
    const total = globalStats.totalPartidos || 0
    
    container.innerHTML = `
      <div class="stats-chart">
        <canvas id="globalStatsChart"></canvas>
      </div>
      <div class="stats-summary">
        <div class="stat-item">
          <span class="stat-label">Victorias</span>
          <span class="stat-value win">${victorias}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Derrotas</span>
          <span class="stat-value loss">${derrotas}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Win Rate</span>
          <span class="stat-value">${winRate}%</span>
        </div>
      </div>
    `
    
    // Crear gráfico de dona
    const chartCtx = document.getElementById('globalStatsChart')
    if (chartCtx) {
      new Chart(chartCtx, {
        type: 'doughnut',
        data: {
          labels: ['Victorias', 'Derrotas'],
          datasets: [{
            data: [victorias, derrotas],
            backgroundColor: ['#10b981', '#ef4444'],
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            }
          }
        }
      })
    }
  }
  
  // Actualizar rankings
  function updateRankings(rankings) {
    if (!rankings) return
    
    const container = document.querySelector('.rankings-container')
    if (!container) return
    
    container.innerHTML = `
      <div class="ranking-card">
        <h4>Ranking General</h4>
        <div class="ranking-position">#${rankings.general}</div>
        <span class="ranking-total">de ${rankings.totalJugadores}</span>
      </div>
      <div class="ranking-card">
        <h4>Singles</h4>
        <div class="ranking-position">#${rankings.singles}</div>
      </div>
      <div class="ranking-card">
        <h4>Doubles</h4>
        <div class="ranking-position">#${rankings.doubles}</div>
      </div>
    `
  }

  // Load default stats when API is not available
  function loadDefaultStats() {
    const defaultStats = {
      activeTournaments: 3,
      totalMatches: 24,
      participationRate: 75,
      totalPlayers: 45,
      pendingInscriptions: 8,
      completionRate: 85,
      avgMatchDuration: 45,
      userTournaments: 2,
      userMatches: 12
    }
    updateStats(defaultStats)
  }

  // Initialize chart
  function initChart() {
    const ctx = document.getElementById('activityChart')
    if (!ctx) return

    new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        datasets: [{
          label: 'Torneos Activos',
          data: [2, 3, 2, 4, 3, 5],
          borderColor: '#4169e1',
          backgroundColor: 'rgba(65, 105, 225, 0.1)',
          tension: 0.4
        }, {
          label: 'Partidos Jugados',
          data: [12, 18, 15, 22, 20, 28],
          borderColor: '#ff8c42',
          backgroundColor: 'rgba(255, 140, 66, 0.1)',
          tension: 0.4
        }, {
          label: 'Inscripciones',
          data: [8, 12, 10, 15, 18, 22],
          borderColor: '#10b981',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          tension: 0.4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            }
          },
          x: {
            grid: {
              display: false
            }
          }
        }
      }
    })
  }

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
    initChart()
    setDefaultDates()
  }

  // Start the dashboard
  initDashboard()
})

