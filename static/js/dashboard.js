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
    } catch (error) {
      console.error('Error loading dashboard stats:', error)
      // Load default stats if API fails
      loadDefaultStats()
    }
  }

  // Update stats display
  function updateStats(stats) {
    document.getElementById('activeTournaments').textContent = stats.activeTournaments || 0
    document.getElementById('totalMatches').textContent = stats.totalMatches || 0
    document.getElementById('participationRate').textContent = `${stats.participationRate || 0}%`
    document.getElementById('totalPlayers').textContent = stats.totalPlayers || 0
    document.getElementById('pendingInscriptions').textContent = stats.pendingInscriptions || 0
    document.getElementById('completionRate').textContent = `${stats.completionRate || 0}%`
    document.getElementById('avgMatchDuration').textContent = stats.avgMatchDuration || 0
    
    // Update user stats
    userTournaments.textContent = stats.userTournaments || 0
    userMatches.textContent = stats.userMatches || 0
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
