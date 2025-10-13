// Configuración
const API_BASE = '/api';

// Función para obtener el token de autenticación
function getAuthToken() {
    return localStorage.getItem('auth_token');
}

// Función para obtener headers de autenticación
function getAuthHeaders() {
    const token = getAuthToken();
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

// Cargar lista de torneos para inscripciones
async function loadInscripciones() {
    console.log('📝 Cargando torneos para inscripciones...');
    
    try {
        const response = await fetch(`${API_BASE}/torneos`, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                auth.redirectToLogin();
                return;
            }
            throw new Error(`Error ${response.status}`);
        }
        
        const torneos = await response.json();
        console.log('✅ Torneos cargados:', torneos.length);
        
        renderTorneosInscripcionList(torneos);
        
    } catch (error) {
        console.error('Error cargando torneos:', error);
        showNotification('Error al cargar torneos', 'error');
    }
}

// Renderizar lista de torneos para inscripción
function renderTorneosInscripcionList(torneos) {
    const container = document.getElementById('torneosInscripcionList');
    
    if (!container) {
        console.error('Contenedor de torneos no encontrado');
        return;
    }
    
    if (torneos.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <p>No hay torneos disponibles</p>
            </div>
        `;
        return;
    }
    
    const user = auth.getUser();
    const isDeportista = user && user.perfil === 'deportista';
    
    container.innerHTML = torneos.map(torneo => `
        <div class="torneo-card" data-id="${torneo.id}">
            <div class="torneo-header">
                <h3>${torneo.nombre}</h3>
                <span class="torneo-status status-${torneo.estado}">
                    ${torneo.estado}
                </span>
            </div>
            <div class="torneo-body">
                <div class="torneo-info">
                    <div class="info-item">
                        <i class="icon-calendar">📅</i>
                        <span>${formatDate(torneo.fecha || torneo.fecha_inicio)}</span>
                    </div>
                    <div class="info-item">
                        <i class="icon-court">🎾</i>
                        <span>${torneo.superficie || 'No especificada'}</span>
                    </div>
                    <div class="info-item">
                        <i class="icon-users">👥</i>
                        <span>${torneo.inscripciones_count || 0}/${torneo.max_participantes || 32} inscritos</span>
                    </div>
                </div>
            </div>
            <div class="torneo-actions">
                <button class="btn btn-sm ${isDeportista ? 'btn-primary' : 'btn-success'}" 
                        onclick="openInscripcionModal(${torneo.id})"
                        style="${isDeportista ? 'width: 100%;' : ''}">
                    ${isDeportista ? '✓ Inscribirme' : '👥 Gestionar Inscripciones'}
                </button>
            </div>
        </div>
    `).join('');
    
    console.log('✅ Torneos renderizados para inscripciones');
}

// Abrir modal de inscripción
window.openInscripcionModal = async function(torneoId) {
    const user = auth.getUser();
    
    // Si es deportista, inscribir directamente
    if (user.perfil === 'deportista') {
        if (confirm('¿Deseas inscribirte en este torneo?')) {
            await inscribirDeportista(torneoId, user.id);
        }
        return;
    }
    
    // Para profesores y administradores, mostrar modal con opciones
    const modal = document.getElementById('inscripcionModalTorneo');
    if (!modal) {
        createInscripcionModal();
    }
    
    await showInscripcionModal(torneoId);
}

// Crear modal de inscripción
function createInscripcionModal() {
    const modal = document.createElement('div');
    modal.id = 'inscripcionModalTorneo';
    modal.className = 'modal';
    modal.style.display = 'none';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="inscripcionModalTitle">Inscripciones del Torneo</h2>
                <button class="close-btn" onclick="closeInscripcionModal()">&times;</button>
            </div>
            
            <div class="modal-body">
                <!-- Lista de inscritos -->
                <div class="inscritos-section">
                    <h3>Deportistas Inscritos</h3>
                    <div id="inscritosList" class="inscritos-list">
                        <div class="loading">Cargando...</div>
                    </div>
                </div>
                
                <!-- Formulario para agregar -->
                <div class="agregar-section">
                    <h3>Agregar Deportista</h3>
                    <form id="inscripcionQuickForm">
                        <div class="form-group">
                            <select id="deportistaSelect" required>
                                <option value="">Seleccionar deportista...</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary">
                            Inscribir Deportista
                        </button>
                    </form>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Manejar submit del formulario
    document.getElementById('inscripcionQuickForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const torneoId = this.dataset.torneoId;
        const deportistaId = document.getElementById('deportistaSelect').value;
        
        if (!deportistaId) {
            alert('Selecciona un deportista');
            return;
        }
        
        await inscribirDeportista(torneoId, deportistaId);
    });
}

// Mostrar modal de inscripción
async function showInscripcionModal(torneoId) {
    const modal = document.getElementById('inscripcionModalTorneo');
    if (!modal) return;
    
    modal.style.display = 'block';
    
    // Cargar inscritos
    await loadInscritos(torneoId);
    
    // Cargar deportistas disponibles
    await loadDeportistasDisponibles(torneoId);
    
    // Guardar torneo ID en el formulario
    document.getElementById('inscripcionQuickForm').dataset.torneoId = torneoId;
}

// Cerrar modal de inscripción
window.closeInscripcionModal = function() {
    const modal = document.getElementById('inscripcionModalTorneo');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Cargar lista de inscritos
async function loadInscritos(torneoId) {
    try {
        const response = await fetch(`${API_BASE}/torneos/${torneoId}/inscripciones`, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) throw new Error('Error al cargar inscritos');
        
        const inscripciones = await response.json();
        const container = document.getElementById('inscritosList');
        
        if (inscripciones.length === 0) {
            container.innerHTML = '<p class="empty-message">No hay deportistas inscritos aún</p>';
            return;
        }
        
        container.innerHTML = inscripciones.map(insc => `
            <div class="inscrito-item">
                <span class="inscrito-nombre">${insc.deportista_nombre}</span>
                <span class="inscrito-estado ${insc.estado}">${insc.estado}</span>
                <button class="btn btn-sm btn-danger" 
                        onclick="eliminarInscripcion(${insc.id}, ${torneoId})">
                    🗑️
                </button>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Error cargando inscritos:', error);
    }
}

// Cargar deportistas disponibles
async function loadDeportistasDisponibles(torneoId) {
    try {
        const response = await fetch(`${API_BASE}/usuarios/deportistas`, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) throw new Error('Error al cargar deportistas');
        
        const deportistas = await response.json();
        const select = document.getElementById('deportistaSelect');
        
        select.innerHTML = '<option value="">Seleccionar deportista...</option>';
        deportistas.forEach(dep => {
            const option = document.createElement('option');
            option.value = dep.id;
            option.textContent = `${dep.nombre} ${dep.apellido}`;
            select.appendChild(option);
        });
        
    } catch (error) {
        console.error('Error cargando deportistas:', error);
    }
}

// Inscribir deportista
async function inscribirDeportista(torneoId, deportistaId) {
    try {
        const response = await fetch(`${API_BASE}/inscripciones`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({
                torneo_id: parseInt(torneoId),
                deportista_id: parseInt(deportistaId)
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Error al inscribir');
        }
        
        alert('✅ Inscripción realizada exitosamente');
        
        // Recargar inscritos si el modal está abierto
        const modal = document.getElementById('inscripcionModalTorneo');
        if (modal && modal.style.display === 'block') {
            await loadInscritos(torneoId);
            document.getElementById('deportistaSelect').value = '';
        }
        
        // Recargar lista de torneos para actualizar contador
        loadInscripciones();
        
    } catch (error) {
        console.error('Error inscribiendo:', error);
        alert('❌ Error: ' + error.message);
    }
}

// Eliminar inscripción
window.eliminarInscripcion = async function(inscripcionId, torneoId) {
    if (!confirm('¿Eliminar esta inscripción?')) return;
    
    try {
        const response = await fetch(`${API_BASE}/inscripciones/${inscripcionId}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        
        if (!response.ok) throw new Error('Error al eliminar');
        
        alert('✅ Inscripción eliminada');
        await loadInscritos(torneoId);
        loadInscripciones();
        
    } catch (error) {
        console.error('Error eliminando:', error);
        alert('❌ Error: ' + error.message);
    }
}

// Función auxiliar para formatear fecha
function formatDate(dateString) {
    if (!dateString) return 'No especificada';
    
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Mostrar notificación
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Exponer funciones globalmente
window.loadInscripciones = loadInscripciones;
window.openInscripcionModal = openInscripcionModal;
window.closeInscripcionModal = closeInscripcionModal;
window.eliminarInscripcion = eliminarInscripcion;
