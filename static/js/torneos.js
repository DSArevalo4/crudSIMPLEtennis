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

// Cargar lista de torneos
async function loadTorneos() {
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
        renderTorneosList(torneos);
        
    } catch (error) {
        console.error('Error cargando torneos:', error);
        showNotification('Error al cargar torneos', 'error');
    }
}

// Renderizar lista de torneos
function renderTorneosList(torneos) {
    const container = document.getElementById('torneosList');
    
    if (!container) {
        console.error('Contenedor de torneos no encontrado');
        return;
    }
    
    if (torneos.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <p>No hay torneos disponibles</p>
                <button class="btn btn-primary" onclick="openTorneoForm()">
                    Crear Primer Torneo
                </button>
            </div>
        `;
        return;
    }
    
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
                        <i class="icon-calendar"></i>
                        <span>${formatDate(torneo.fecha || torneo.fecha_inicio)}</span>
                    </div>
                    <div class="info-item">
                        <i class="icon-court"></i>
                        <span>${torneo.superficie || 'No especificada'}</span>
                    </div>
                    <div class="info-item">
                        <i class="icon-users"></i>
                        <span>${torneo.inscripciones_count || 0}/${torneo.max_participantes || 32}</span>
                    </div>
                </div>
            </div>
            <div class="torneo-actions">
                <button class="btn btn-sm btn-secondary" onclick="viewTorneo(${torneo.id})">
                    Ver
                </button>
                <button class="btn btn-sm btn-primary" onclick="editTorneo(${torneo.id})">
                    Editar
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteTorneo(${torneo.id})">
                    Eliminar
                </button>
            </div>
        </div>
    `).join('');
}

// Abrir formulario de torneo
// Verificar permisos antes de mostrar el formulario
function openTorneoForm(torneoId = null) {
    const modal = document.getElementById('torneoFormModal');
    const form = document.getElementById('torneoForm');
    const title = document.getElementById('torneoFormTitle');
    
    if (!modal || !form) {
        console.error('Modal o formulario no encontrado');
        return;
    }
    
    // Verificar permisos del usuario
    const user = auth.getUser();
    if (user && user.perfil && !['profesor', 'administrador'].includes(user.perfil)) {
        showNotification('Solo profesores y administradores pueden crear torneos', 'error');
        return;
    }
    
    // Limpiar formulario
    form.reset();
    
    if (torneoId) {
        // Modo edición
        title.textContent = 'Editar Torneo';
        loadTorneoData(torneoId);
    } else {
        // Modo creación
        title.textContent = 'Crear Torneo';
        // Establecer valores por defecto
        document.getElementById('torneoSuperficie').value = 'Dura';
        document.getElementById('torneoNivel').value = 'Intermedio';
        document.getElementById('torneoTipo').value = 'abierto';
    }
    
    modal.style.display = 'block';
}

// Cargar datos de torneo para edición
async function loadTorneoData(torneoId) {
    try {
        const response = await fetch(`${API_BASE}/torneos/${torneoId}`, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Error al cargar torneo');
        }
        
        const torneo = await response.json();
        
        // Llenar formulario con datos
        document.getElementById('torneoNombre').value = torneo.nombre || '';
        document.getElementById('torneoSuperficie').value = torneo.superficie || 'Dura';
        document.getElementById('torneoNivel').value = torneo.nivel || 'Intermedio';
        document.getElementById('torneoTipo').value = torneo.tipo || 'abierto';
        document.getElementById('torneoFecha').value = torneo.fecha || torneo.fecha_inicio || '';
        document.getElementById('torneoHora').value = torneo.hora || '';
        document.getElementById('torneoDescripcion').value = torneo.descripcion || '';
        
        // Guardar ID para actualización
        document.getElementById('torneoForm').dataset.torneoId = torneoId;
        
    } catch (error) {
        console.error('Error cargando datos del torneo:', error);
        showNotification('Error al cargar datos del torneo', 'error');
    }
}

// Cerrar formulario de torneo
function closeTorneoFormModal() {
    const modal = document.getElementById('torneoFormModal');
    if (modal) {
        modal.style.display = 'none';
    }
    
    const form = document.getElementById('torneoForm');
    if (form) {
        form.reset();
        delete form.dataset.torneoId;
    }
}

// Manejar submit del formulario
async function handleTorneoFormSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const torneoId = form.dataset.torneoId;
    
    // Obtener datos del formulario - AGREGAR CAMPO TIPO
    const formData = {
        nombre: document.getElementById('torneoNombre').value.trim(),
        superficie: document.getElementById('torneoSuperficie').value,
        nivel: document.getElementById('torneoNivel').value,
        tipo: document.getElementById('torneoTipo').value,  // ← NUEVO CAMPO
        fecha_inicio: document.getElementById('torneoFecha').value,
        hora: document.getElementById('torneoHora').value,
        descripcion: document.getElementById('torneoDescripcion').value.trim()
    };
    
    console.log('📤 Enviando datos:', formData);
    
    // Validar datos
    if (!formData.nombre) {
        showNotification('El nombre es obligatorio', 'error');
        return;
    }
    
    if (!formData.fecha_inicio) {
        showNotification('La fecha es obligatoria', 'error');
        return;
    }
    
    if (!formData.superficie) {
        showNotification('La superficie es obligatoria', 'error');
        return;
    }
    
    if (!formData.nivel) {
        showNotification('El nivel es obligatorio', 'error');
        return;
    }
    
    if (!formData.tipo) {
        showNotification('El tipo es obligatorio', 'error');
        return;
    }
    
    // Deshabilitar botón durante envío
    submitBtn.disabled = true;
    submitBtn.textContent = torneoId ? 'Actualizando...' : 'Creando...';
    
    try {
        const url = torneoId ? `${API_BASE}/torneos/${torneoId}` : `${API_BASE}/torneos`;
        const method = torneoId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: getAuthHeaders(),
            body: JSON.stringify(formData)
        });
        
        console.log('📥 Respuesta:', response.status, response.statusText);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Error ${response.status}`);
        }
        
        const result = await response.json();
        console.log('✅ Torneo guardado:', result);
        
        showNotification(
            torneoId ? 'Torneo actualizado exitosamente' : 'Torneo creado exitosamente',
            'success'
        );
        
        closeTorneoFormModal();
        loadTorneos(); // Recargar lista
        
    } catch (error) {
        console.error('❌ Error:', error);
        showNotification(`Error: ${error.message}`, 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Guardar';
    }
}

// Ver torneo (abrir cuadro de tenis)
async function viewTorneo(torneoId) {
    try {
        const response = await fetch(`${API_BASE}/torneos/${torneoId}/inscripciones`, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Error al cargar inscripciones');
        }
        
        const inscripciones = await response.json();
        openTennisBracketModal(torneoId, inscripciones);
        
    } catch (error) {
        console.error('Error cargando inscripciones:', error);
        showNotification('Error al cargar inscripciones', 'error');
    }
}

// Editar torneo
function editTorneo(torneoId) {
    openTorneoForm(torneoId);
}

// Eliminar torneo
async function deleteTorneo(torneoId) {
    if (!confirm('¿Estás seguro de que deseas eliminar este torneo?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/torneos/${torneoId}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Error al eliminar torneo');
        }
        
        showNotification('Torneo eliminado exitosamente', 'success');
        loadTorneos(); // Recargar lista
        
    } catch (error) {
        console.error('Error eliminando torneo:', error);
        showNotification('Error al eliminar torneo', 'error');
    }
}

// Abrir modal de cuadro de tenis
function openTennisBracketModal(torneoId, inscripciones) {
    const modal = document.getElementById('tennisBracketModal');
    const container = document.getElementById('tennisBracketContainer');
    
    if (!modal || !container) {
        console.error('Modal o contenedor no encontrado');
        return;
    }
    
    // Generar cuadro de tenis
    generateTennisBracket(container, inscripciones);
    
    modal.style.display = 'block';
}

// Cerrar modal de cuadro de tenis
function closeTennisBracketModal() {
    const modal = document.getElementById('tennisBracketModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Generar cuadro de tenis
function generateTennisBracket(container, inscripciones) {
    if (inscripciones.length === 0) {
        container.innerHTML = '<p class="empty-state">No hay inscripciones para este torneo</p>';
        return;
    }
    
    // Calcular número de rondas
    const numPlayers = inscripciones.length;
    const numRounds = Math.ceil(Math.log2(numPlayers));
    
    let bracketHTML = '<div class="tennis-bracket">';
    
    // Generar rondas
    for (let round = 0; round < numRounds; round++) {
        const matchesInRound = Math.pow(2, numRounds - round - 1);
        bracketHTML += `<div class="bracket-round">`;
        bracketHTML += `<h4>Ronda ${round + 1}</h4>`;
        
        for (let match = 0; match < matchesInRound; match++) {
            const player1Index = match * 2;
            const player2Index = match * 2 + 1;
            
            const player1 = inscripciones[player1Index];
            const player2 = inscripciones[player2Index];
            
            bracketHTML += `
                <div class="match-slot">
                    <div class="player-slot ${player1 ? '' : 'bye'}">
                        ${player1 ? player1.deportista_nombre : 'BYE'}
                    </div>
                    <div class="player-slot ${player2 ? '' : 'bye'}">
                        ${player2 ? player2.deportista_nombre : 'BYE'}
                    </div>
                </div>
            `;
        }
        
        bracketHTML += '</div>';
    }
    
    bracketHTML += '</div>';
    container.innerHTML = bracketHTML;
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
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Agregar al body
    document.body.appendChild(notification);
    
    // Mostrar
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Ocultar y eliminar
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Configurar formulario
    const form = document.getElementById('torneoForm');
    if (form) {
        form.addEventListener('submit', handleTorneoFormSubmit);
    }
    
    // Cargar torneos si estamos en la página correcta
    if (window.location.pathname.includes('torneos') || document.getElementById('torneosList')) {
        loadTorneos();
    }
    
    // Configurar cierre de modales al hacer clic fuera
    window.addEventListener('click', function(event) {
        const torneoModal = document.getElementById('torneoFormModal');
        const bracketModal = document.getElementById('tennisBracketModal');
        
        if (event.target === torneoModal) {
            closeTorneoFormModal();
        }
        
        if (event.target === bracketModal) {
            closeTennisBracketModal();
        }
    });
});

// Exponer funciones globalmente
window.loadTorneos = loadTorneos;
window.openTorneoForm = openTorneoForm;
window.closeTorneoFormModal = closeTorneoFormModal;
window.viewTorneo = viewTorneo;
window.editTorneo = editTorneo;
window.deleteTorneo = deleteTorneo;
window.closeTennisBracketModal = closeTennisBracketModal;
