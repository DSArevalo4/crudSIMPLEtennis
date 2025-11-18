// Gestión de Inscripciones
let inscripciones = [];
let torneosDisponibles = [];
let deportistas = [];
let currentInscripcion = null;

async function setupInscripcionesUI() {
    const user = auth.getUser();
    if (!user) {
        console.error('Usuario no autenticado');
        return;
    }

    const headerActions = document.querySelector('#section-inscripciones .header-actions');
    const subtitle = document.querySelector('#section-inscripciones .subtitle');

    if (!headerActions || !subtitle) {
        console.error('Elementos de UI de inscripciones no encontrados');
        return;
    }

    // Configurar UI según el rol
    if (user.perfil === 'deportista') {
        // Deportistas solo pueden inscribirse a sí mismos
        headerActions.innerHTML = `
            <button class="btn-primary" onclick="openInscripcionFormAsync()">
                <i class="icon">➕</i> Nueva Inscripción
            </button>
        `;
        subtitle.textContent = 'Mis Inscripciones';
    } else if (user.perfil === 'administrador' || user.perfil === 'profesor') {
        // Admin y profesores pueden inscribir a cualquier deportista
        headerActions.innerHTML = `
            <button class="btn-primary" onclick="openInscripcionFormAsync()">
                <i class="icon">➕</i> Nueva Inscripción
            </button>
        `;
        subtitle.textContent = 'Gestión de Inscripciones';
    }

    // Agregar filtros solo si no existen
    let filterSection = document.querySelector('#section-inscripciones .filter-section');
    if (!filterSection) {
        filterSection = document.createElement('div');
        filterSection.className = 'filter-section';
        filterSection.innerHTML = `
            <div class="filter-group">
                <label for="filter-estado">Estado:</label>
                <select id="filter-estado" onchange="loadInscripciones()">
                    <option value="">Todos</option>
                    <option value="pendiente">Pendiente</option>
                    <option value="aceptada">Aceptada</option>
                    <option value="rechazada">Rechazada</option>
                </select>
            </div>
            <div class="filter-group">
                <label for="filter-torneo">Torneo:</label>
                <select id="filter-torneo" onchange="loadInscripciones()">
                    <option value="">Todos</option>
                </select>
            </div>
        `;

        const container = document.querySelector('#section-inscripciones .inscripciones-container');
        if (container) {
            container.insertBefore(filterSection, container.firstChild);
        }
    }

    // Cargar datos iniciales
    await Promise.all([
        loadInscripciones(),
        loadTorneosDisponibles(),
        loadDeportistas()
    ]);
    
    console.log('Inscripciones UI configurada. Torneos:', torneosDisponibles.length, 'Deportistas:', deportistas.length);
}

async function loadInscripciones() {
    try {
        const filterEstado = document.getElementById('filter-estado')?.value || '';
        const filterTorneo = document.getElementById('filter-torneo')?.value || '';

        let url = '/api/inscripciones?';
        if (filterEstado) url += `estado=${filterEstado}&`;
        if (filterTorneo) url += `torneo_id=${filterTorneo}&`;

        const response = await api.get(url);
        if (!response.ok) {
            throw new Error('Error al cargar inscripciones');
        }

        inscripciones = await response.json();
        renderInscripciones();
    } catch (error) {
        console.error('Error cargando inscripciones:', error);
        showNotification('Error al cargar inscripciones: ' + error.message, 'error');
    }
}

async function loadTorneosDisponibles() {
    try {
        const response = await api.get('/api/inscripciones/torneos-disponibles');
        if (!response.ok) {
            throw new Error('Error al cargar torneos');
        }

        torneosDisponibles = await response.json();
        console.log('Torneos disponibles cargados:', torneosDisponibles);

        // Actualizar select de filtro
        const filterTorneo = document.getElementById('filter-torneo');
        if (filterTorneo) {
            // Mantener opción "Todos"
            filterTorneo.innerHTML = '<option value="">Todos</option>';
            torneosDisponibles.forEach(torneo => {
                const option = document.createElement('option');
                option.value = torneo.id;
                option.textContent = torneo.nombre;
                filterTorneo.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error cargando torneos disponibles:', error);
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

function renderInscripciones() {
    const container = document.querySelector('#section-inscripciones .inscripciones-container');
    if (!container) return;

    const user = auth.getUser();

    // Buscar o crear la tabla
    let tableContainer = container.querySelector('.table-container');
    if (!tableContainer) {
        tableContainer = document.createElement('div');
        tableContainer.className = 'table-container';
        container.appendChild(tableContainer);
    }

    if (!inscripciones || inscripciones.length === 0) {
        tableContainer.innerHTML = '<p class="no-data">No hay inscripciones registradas</p>';
        return;
    }

    const html = `
        <table class="data-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Torneo</th>
                    <th>Deportista</th>
                    <th>Fecha Inscripción</th>
                    <th>Estado</th>
                    ${user.perfil !== 'deportista' ? '<th>Acciones</th>' : ''}
                </tr>
            </thead>
            <tbody>
                ${inscripciones.map(inscripcion => `
                    <tr>
                        <td>${inscripcion.id}</td>
                        <td>${inscripcion.torneo_nombre || 'N/A'}</td>
                        <td>${inscripcion.deportista_nombre || 'N/A'}</td>
                        <td>${formatDate(inscripcion.fecha_inscripcion)}</td>
                        <td>
                            <span class="badge badge-${getEstadoBadgeClass(inscripcion.estado)}">
                                ${inscripcion.estado}
                            </span>
                        </td>
                        ${user.perfil !== 'deportista' ? `
                            <td class="action-buttons">
                                ${inscripcion.estado === 'pendiente' ? `
                                    <button class="btn-success btn-sm" onclick="updateEstado(${inscripcion.id}, 'aceptada')" title="Aceptar">
                                        ✓
                                    </button>
                                    <button class="btn-danger btn-sm" onclick="updateEstado(${inscripcion.id}, 'rechazada')" title="Rechazar">
                                        ✗
                                    </button>
                                ` : ''}
                                <button class="btn-danger btn-sm" onclick="deleteInscripcion(${inscripcion.id})" title="Eliminar">
                                    🗑️
                                </button>
                            </td>
                        ` : ''}
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;

    tableContainer.innerHTML = html;
}

// Función asíncrona para abrir el formulario
async function openInscripcionFormAsync() {
    // Asegurar que los datos estén cargados
    if (torneosDisponibles.length === 0 || deportistas.length === 0) {
        console.log('Cargando datos antes de abrir modal...');
        await Promise.all([
            loadTorneosDisponibles(),
            loadDeportistas()
        ]);
    }
    
    openInscripcionForm();
}

function openInscripcionForm() {
    const user = auth.getUser();
    const modal = document.getElementById('inscripcionFormModal');
    if (!modal) {
        console.error('Modal de inscripción no encontrado');
        return;
    }

    console.log('Abriendo modal. Torneos disponibles:', torneosDisponibles.length, 'Deportistas:', deportistas.length);

    currentInscripcion = null;
    
    // Configurar formulario según el rol
    const deportistaGroup = document.getElementById('deportista-group');
    const torneoSelect = document.getElementById('inscripcion-torneo');
    const deportistaSelect = document.getElementById('inscripcion-deportista');

    if (user.perfil === 'deportista') {
        // Deportista: ocultar selector de deportista, solo selecciona torneo
        if (deportistaGroup) deportistaGroup.style.display = 'none';
        
        // Quitar required del selector de deportista
        if (deportistaSelect) {
            deportistaSelect.removeAttribute('required');
        }
        
        // Llenar torneos disponibles (solo abiertos)
        if (torneoSelect) {
            torneoSelect.innerHTML = '<option value="">Seleccione un torneo</option>';
            const torneosDisponiblesDeportista = torneosDisponibles.filter(t => !t.ya_inscrito && t.cupos_disponibles > 0);
            
            if (torneosDisponiblesDeportista.length === 0) {
                torneoSelect.innerHTML += '<option value="" disabled>No hay torneos disponibles</option>';
            } else {
                torneosDisponiblesDeportista.forEach(torneo => {
                    const option = document.createElement('option');
                    option.value = torneo.id;
                    option.textContent = `${torneo.nombre} (${torneo.cupos_disponibles} cupos disponibles)`;
                    torneoSelect.appendChild(option);
                });
            }
        }
    } else {
        // Admin/Profesor: mostrar selector de deportista
        if (deportistaGroup) deportistaGroup.style.display = 'block';
        
        // Agregar required al selector de deportista
        if (deportistaSelect) {
            deportistaSelect.setAttribute('required', 'required');
        }
        
        // Llenar torneos disponibles
        if (torneoSelect) {
            torneoSelect.innerHTML = '<option value="">Seleccione un torneo</option>';
            
            if (torneosDisponibles.length === 0) {
                torneoSelect.innerHTML += '<option value="" disabled>No hay torneos disponibles</option>';
            } else {
                torneosDisponibles.forEach(torneo => {
                    const option = document.createElement('option');
                    option.value = torneo.id;
                    option.textContent = `${torneo.nombre} - ${torneo.tipo} (${torneo.cupos_disponibles} cupos disponibles)`;
                    torneoSelect.appendChild(option);
                });
            }
        }

        // Llenar deportistas
        if (deportistaSelect) {
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
        }
    }

    modal.style.display = 'block';
}

function closeInscripcionModal() {
    const modal = document.getElementById('inscripcionFormModal');
    if (modal) {
        modal.style.display = 'none';
    }
    currentInscripcion = null;
}

async function saveInscripcion() {
    try {
        const user = auth.getUser();
        const torneoId = document.getElementById('inscripcion-torneo')?.value;
        let deportistaId = null;

        if (user.perfil === 'deportista') {
            // El deportista se inscribe a sí mismo
            deportistaId = user.id;
        } else {
            // Admin/Profesor selecciona el deportista
            deportistaId = document.getElementById('inscripcion-deportista')?.value;
        }

        if (!torneoId) {
            showNotification('Debe seleccionar un torneo', 'error');
            return;
        }

        if (!deportistaId) {
            showNotification('Debe seleccionar un deportista', 'error');
            return;
        }

        const data = {
            torneo_id: parseInt(torneoId),
            deportista_id: parseInt(deportistaId)
        };

        const response = await api.post('/api/inscripciones', data);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error al crear inscripción');
        }

        showNotification('Inscripción creada exitosamente', 'success');
        closeInscripcionModal();
        await Promise.all([
            loadInscripciones(),
            loadTorneosDisponibles()
        ]);
    } catch (error) {
        console.error('Error guardando inscripción:', error);
        showNotification(error.message, 'error');
    }
}

async function updateEstado(inscripcionId, nuevoEstado) {
    if (!confirm(`¿Está seguro de ${nuevoEstado === 'aceptada' ? 'aceptar' : 'rechazar'} esta inscripción?`)) {
        return;
    }

    try {
        const response = await api.put(`/api/inscripciones/${inscripcionId}`, {
            estado: nuevoEstado
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error al actualizar inscripción');
        }

        showNotification(`Inscripción ${nuevoEstado} exitosamente`, 'success');
        await loadInscripciones();
    } catch (error) {
        console.error('Error actualizando estado:', error);
        showNotification(error.message, 'error');
    }
}

async function deleteInscripcion(inscripcionId) {
    if (!confirm('¿Está seguro de eliminar esta inscripción?')) {
        return;
    }

    try {
        const response = await api.delete(`/api/inscripciones/${inscripcionId}`);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error al eliminar inscripción');
        }

        showNotification('Inscripción eliminada exitosamente', 'success');
        await Promise.all([
            loadInscripciones(),
            loadTorneosDisponibles()
        ]);
    } catch (error) {
        console.error('Error eliminando inscripción:', error);
        showNotification(error.message, 'error');
    }
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
