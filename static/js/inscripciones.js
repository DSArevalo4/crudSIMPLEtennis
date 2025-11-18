// Gestión de Inscripciones
let torneosParaInscripcion = [];
let deportistas = [];
let torneoSeleccionado = null;

async function setupInscripcionesUI() {
    const user = auth.getUser();
    if (!user) {
        console.error('Usuario no autenticado');
        return;
    }

    const subtitle = document.querySelector('#section-inscripciones .subtitle');

    if (!subtitle) {
        console.error('Elementos de UI de inscripciones no encontrados');
        return;
    }

    // Configurar UI según el rol
    if (user.perfil === 'deportista') {
        subtitle.textContent = 'Torneos Disponibles para Inscripción';
    } else if (user.perfil === 'administrador' || user.perfil === 'profesor') {
        subtitle.textContent = 'Gestión de Inscripciones a Torneos';
    }

    // Cargar datos iniciales
    await Promise.all([
        loadTorneosParaInscripcion(),
        loadDeportistas()
    ]);
    
    console.log('Inscripciones UI configurada. Torneos:', torneosParaInscripcion.length, 'Deportistas:', deportistas.length);
}

async function loadTorneosParaInscripcion() {
    try {
        const user = auth.getUser();
        console.log('Cargando torneos para:', user.perfil);
        
        // Para admin/profesor: cargar todos los torneos
        // Para deportista: cargar solo torneos disponibles (abiertos y no inscritos)
        const endpoint = user.perfil === 'deportista' 
            ? '/api/inscripciones/torneos-disponibles'
            : '/api/torneos';
        
        console.log('Endpoint a llamar:', endpoint);
        const response = await api.get(endpoint);
        console.log('Response status:', response.status, response.ok);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || 'Error al cargar torneos');
        }

        const allTorneos = await response.json();
        console.log('Torneos recibidos del backend:', allTorneos);
        
        // Filtrar solo torneos planificados
        torneosParaInscripcion = allTorneos.filter(t => t.estado === 'planificado');
        console.log('Torneos planificados filtrados:', torneosParaInscripcion);

        renderTorneosInscripcion();
    } catch (error) {
        console.error('Error cargando torneos:', error);
        showNotification('Error al cargar torneos: ' + error.message, 'error');
    }
}

async function loadDeportistas() {
    const user = auth.getUser();
    if (user.perfil === 'administrador' || user.perfil === 'profesor') {
        try {
            const response = await api.get('/api/usuarios/deportistas');
            if (!response.ok) {
                throw new Error('Error al cargar deportistas');
            }

            deportistas = await response.json();
            console.log('Deportistas cargados:', deportistas);
        } catch (error) {
            console.error('Error cargando deportistas:', error);
            showNotification('Error al cargar deportistas: ' + error.message, 'error');
        }
    }
}

function renderTorneosInscripcion() {
    const container = document.querySelector('#section-inscripciones .inscripciones-container');
    if (!container) {
        console.error('Container de inscripciones no encontrado');
        return;
    }

    const user = auth.getUser();
    console.log('Renderizando torneos. Total:', torneosParaInscripcion.length);

    if (!torneosParaInscripcion || torneosParaInscripcion.length === 0) {
        container.innerHTML = '<p class="no-data">No hay torneos planificados disponibles para inscripción</p>';
        return;
    }

    const html = `
        <div class="torneos-grid">
            ${torneosParaInscripcion.map(torneo => {
                const cuposDisponibles = torneo.cupos_disponibles !== undefined 
                    ? torneo.cupos_disponibles 
                    : (torneo.max_participantes || 32);
                
                return `
                    <div class="torneo-card-inscripcion">
                        <div class="torneo-card-header">
                            <h3>${torneo.nombre}</h3>
                            <span class="badge badge-${torneo.tipo === 'abierto' ? 'success' : 'secondary'}">
                                ${torneo.tipo || 'abierto'}
                            </span>
                        </div>
                        <div class="torneo-card-body">
                            <div class="torneo-info">
                                <p><strong>Superficie:</strong> ${torneo.superficie}</p>
                                <p><strong>Fecha Inicio:</strong> ${formatDateShort(torneo.fecha_inicio)}</p>
                                ${torneo.fecha_fin ? `<p><strong>Fecha Fin:</strong> ${formatDateShort(torneo.fecha_fin)}</p>` : ''}
                                <p><strong>Estado:</strong> 
                                    <span class="badge badge-${getEstadoTorneoBadgeClass(torneo.estado)}">
                                        ${torneo.estado || 'planificado'}
                                    </span>
                                </p>
                                <p><strong>Cupos Disponibles:</strong> ${cuposDisponibles} / ${torneo.max_participantes || 32}</p>
                                ${torneo.descripcion ? `<p class="torneo-descripcion">${torneo.descripcion}</p>` : ''}
                            </div>
                        </div>
                        <div class="torneo-card-footer">
                            ${user.perfil === 'deportista' ? `
                                <button class="btn-primary btn-block" onclick="inscribirmeATorneo(${torneo.id})">
                                    ➕ Inscribirme
                                </button>
                            ` : `
                                <button class="btn-primary btn-block" onclick="abrirModalInscribirDeportista(${torneo.id})">
                                    👥 Inscribir Deportistas
                                </button>
                            `}
                        </div>
                    </div>
                `;
            }).join('')}
        </div>
    `;

    container.innerHTML = html;
}

// Inscribir al deportista actual (deportista se inscribe a sí mismo)
async function inscribirmeATorneo(torneoId) {
    if (!confirm('¿Confirmas tu inscripción a este torneo?')) {
        return;
    }

    try {
        const user = auth.getUser();
        
        // Para deportistas, enviar solo torneo_id (el backend asigna automáticamente el deportista_id)
        const data = {
            torneo_id: torneoId
        };

        console.log('Datos de inscripción a enviar:', data);
        const response = await api.post('/api/inscripciones', data);
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error al crear inscripción');
        }

        const result = await response.json();
        console.log('Inscripción creada:', result);
        
        showNotification('¡Te has inscrito exitosamente al torneo!', 'success');
        await loadTorneosParaInscripcion();
    } catch (error) {
        console.error('Error inscribiendo:', error);
        showNotification(error.message, 'error');
    }
}

// Abrir modal para que admin/profesor seleccione deportista
async function abrirModalInscribirDeportista(torneoId) {
    // Asegurar que los deportistas estén cargados
    if (deportistas.length === 0) {
        await loadDeportistas();
    }

    torneoSeleccionado = torneoId;
    const modal = document.getElementById('inscripcionFormModal');
    const deportistaSelect = document.getElementById('inscripcion-deportista');
    const torneoInfo = document.getElementById('torneo-inscripcion-info');
    
    if (!modal || !deportistaSelect) {
        console.error('Modal de inscripción no encontrado');
        return;
    }

    // Buscar el torneo seleccionado
    const torneo = torneosParaInscripcion.find(t => t.id === torneoId);
    
    if (torneoInfo && torneo) {
        torneoInfo.innerHTML = `
            <div class="torneo-selected-info">
                <h4>${torneo.nombre}</h4>
                <p><strong>Tipo:</strong> ${torneo.tipo} | <strong>Superficie:</strong> ${torneo.superficie}</p>
            </div>
        `;
    }

    // Llenar deportistas
    deportistaSelect.innerHTML = '<option value="">Seleccione un deportista</option>';
    
    if (deportistas.length === 0) {
        deportistaSelect.innerHTML += '<option value="" disabled>No hay deportistas disponibles</option>';
    } else {
        deportistas.forEach(deportista => {
            const option = document.createElement('option');
            option.value = deportista.id;
            option.textContent = `${deportista.nombre} ${deportista.apellido}`;
            deportistaSelect.appendChild(option);
        });
    }

    modal.style.display = 'block';
}

function closeInscripcionModal() {
    const modal = document.getElementById('inscripcionFormModal');
    if (modal) {
        modal.style.display = 'none';
    }
    torneoSeleccionado = null;
}

async function saveInscripcionAdmin() {
    try {
        const deportistaId = document.getElementById('inscripcion-deportista')?.value;

        if (!deportistaId) {
            showNotification('Debe seleccionar un deportista', 'error');
            return;
        }

        if (!torneoSeleccionado) {
            showNotification('Error: No se ha seleccionado un torneo', 'error');
            return;
        }

        const data = {
            torneo_id: parseInt(torneoSeleccionado),
            deportista_id: parseInt(deportistaId)
        };

        const response = await api.post('/api/inscripciones', data);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error al crear inscripción');
        }

        showNotification('Deportista inscrito exitosamente', 'success');
        closeInscripcionModal();
        await loadTorneosParaInscripcion();
    } catch (error) {
        console.error('Error guardando inscripción:', error);
        showNotification(error.message, 'error');
    }
}

function getEstadoTorneoBadgeClass(estado) {
    const classes = {
        'planificado': 'warning',
        'en_curso': 'success',
        'finalizado': 'secondary'
    };
    return classes[estado] || 'secondary';
}

function formatDateShort(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function getEstadoBadgeClass(estado) {
    const classes = {
        'pendiente': 'warning',
        'aceptada': 'success',
        'rechazada': 'danger'
    };
    return classes[estado] || 'secondary';
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function showNotification(message, type = 'info') {
    // Reutilizar función de notificación si existe
    if (window.showNotification) {
        window.showNotification(message, type);
    } else {
        alert(message);
    }
}
