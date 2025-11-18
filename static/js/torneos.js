// Funcionalidad de torneos
let currentEditingTorneoId = null;

// Cargar lista de torneos
async function loadTorneos() {
    const torneosList = document.getElementById('torneosList');
    if (!torneosList) {
        console.error('Elemento torneosList no encontrado');
        return;
    }
    
    torneosList.innerHTML = '<div class="loading">Cargando torneos...</div>';
    
    // Configurar UI según el perfil del usuario
    setupTorneosUI();
    
    try {
        const torneos = await api.getTorneos();
        renderTorneos(torneos);
    } catch (error) {
        console.error('Error cargando torneos:', error);
        torneosList.innerHTML = `<div class="error">Error al cargar torneos: ${error.message}</div>`;
    }
}

// Configurar UI de torneos según el perfil del usuario
function setupTorneosUI() {
    const user = auth.getUser();
    const headerActions = document.getElementById('torneos-header-actions');
    const subtitle = document.getElementById('torneos-subtitle');
    
    if (!user || !headerActions) return;
    
    const isDeportista = user.perfil === 'deportista';
    
    if (isDeportista) {
        // Deportistas: no muestran botón "Nuevo Torneo" y cambiar subtítulo
        headerActions.innerHTML = '';
        if (subtitle) {
            subtitle.textContent = 'Mis Torneos Inscritos';
        }
    } else {
        // Administradores y profesores: mostrar botón "Nuevo Torneo"
        headerActions.innerHTML = `
            <button class="btn btn-primary" onclick="openTorneoForm()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="12" y1="5" x2="12" y2="19"></line>
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                Nuevo Torneo
            </button>
        `;
        if (subtitle) {
            subtitle.textContent = 'Gestión de Torneos de Tenis';
        }
    }
}

// Renderizar lista de torneos
function renderTorneos(torneos) {
    const torneosList = document.getElementById('torneosList');
    
    if (torneos.length === 0) {
        torneosList.innerHTML = '<div class="empty-state">No hay torneos registrados</div>';
        return;
    }

    // Obtener perfil del usuario
    const user = auth.getUser();
    const isDeportista = user && user.perfil === 'deportista';

    torneosList.innerHTML = torneos.map(torneo => `
        <div class="torneo-card">
            <div class="torneo-header">
                <h3 class="torneo-nombre">${torneo.nombre}</h3>
                <div class="torneo-badges">
                    <span class="badge badge-${torneo.estado?.toLowerCase() || 'pendiente'}">${torneo.estado || 'Pendiente'}</span>
                    <span class="badge badge-nivel">${torneo.nivel}</span>
                </div>
            </div>
            
            <div class="torneo-details">
                <div class="detail-item">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                        <line x1="16" y1="2" x2="16" y2="6"/>
                        <line x1="8" y1="2" x2="8" y2="6"/>
                        <line x1="3" y1="10" x2="21" y2="10"/>
                    </svg>
                    <span>${torneo.fecha || 'Sin fecha'}</span>
                </div>
                
                <div class="detail-item">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                        <path d="M2 17l10 5 10-5M2 12l10 5 10-5"/>
                    </svg>
                    <span>${torneo.superficie || 'Sin superficie'}</span>
                </div>
                
                <div class="detail-item">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                        <circle cx="9" cy="7" r="4"/>
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                        <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                    </svg>
                    <span>${torneo.inscripciones_count || 0} inscritos</span>
                </div>
            </div>
            
            <div class="torneo-actions">
                <button class="btn btn-sm btn-primary" onclick="viewTorneo(${torneo.id})">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                        <circle cx="12" cy="12" r="3"/>
                    </svg>
                    Ver
                </button>
                ${!isDeportista ? `
                <button class="btn btn-sm btn-secondary" onclick="editTorneo(${torneo.id})">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                    </svg>
                    Editar
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteTorneo(${torneo.id})">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3,6 5,6 21,6"/>
                        <path d="M19,6v14a2,2 0 0,1 -2,2H7a2,2 0 0,1 -2,-2V6m3,0V4a2,2 0 0,1 2,-2h4a2,2 0 0,1 2,2v2"/>
                    </svg>
                    Eliminar
                </button>
                ` : ''}
            </div>
        </div>
    `).join('');
}

// Abrir formulario de torneo
function openTorneoForm(torneo = null) {
    const modal = document.getElementById('torneoFormModal');
    const title = document.getElementById('torneoFormTitle');
    const form = document.getElementById('torneoForm');
    
    if (!modal || !title || !form) {
        console.error('Elementos del modal de torneo no encontrados');
        return;
    }
    
    currentEditingTorneoId = torneo ? torneo.id : null;
    
    if (torneo) {
        title.textContent = 'Editar Torneo';
        document.getElementById('torneoNombre').value = torneo.nombre || '';
        document.getElementById('torneoTipo').value = torneo.tipo || '';
        document.getElementById('torneoSuperficie').value = torneo.superficie || '';
        document.getElementById('torneoFechaInicio').value = torneo.fecha_inicio || '';
        document.getElementById('torneoFechaFin').value = torneo.fecha_fin || '';
        document.getElementById('torneoEstado').value = torneo.estado || 'planificado';
        document.getElementById('torneoMaxParticipantes').value = torneo.max_participantes || 32;
        document.getElementById('torneoDescripcion').value = torneo.descripcion || '';
    } else {
        title.textContent = 'Crear Torneo';
        form.reset();
        // Valores por defecto
        document.getElementById('torneoEstado').value = 'planificado';
        document.getElementById('torneoMaxParticipantes').value = 32;
    }
    
    modal.style.display = 'flex';
}

// Cerrar formulario de torneo
function closeTorneoFormModal() {
    const modal = document.getElementById('torneoFormModal');
    if (modal) {
        modal.style.display = 'none';
    }
    currentEditingTorneoId = null;
}

// Editar torneo
async function editTorneo(torneoId) {
    try {
        const torneo = await api.getTorneo(torneoId);
        openTorneoForm(torneo);
    } catch (error) {
        console.error('Error cargando torneo:', error);
        alert(`Error al cargar torneo: ${error.message}`);
    }
}

// Eliminar torneo
async function deleteTorneo(torneoId) {
    if (!confirm('¿Estás seguro de que quieres eliminar este torneo?')) {
        return;
    }

    try {
        await api.deleteTorneo(torneoId);
        loadTorneos(); // Recargar la lista
        alert('Torneo eliminado exitosamente');
    } catch (error) {
        console.error('Error eliminando torneo:', error);
        alert(`Error al eliminar torneo: ${error.message}`);
    }
}

// Ver torneo (cuadro de tenis)
async function viewTorneo(torneoId) {
    try {
        const torneo = await api.getTorneo(torneoId);
        const inscripciones = await api.getInscripcionesByTorneo(torneoId);
        
        // Mostrar modal de cuadro de tenis
        showTennisBracket(torneo, inscripciones);
    } catch (error) {
        console.error('Error cargando torneo:', error);
        alert(`Error al cargar torneo: ${error.message}`);
    }
}

// Mostrar cuadro de tenis
function showTennisBracket(torneo, inscripciones) {
    const modal = document.getElementById('tennisBracketModal');
    const title = document.getElementById('bracketTitle');
    const container = document.getElementById('tennisBracketContainer');
    
    if (!modal || !title || !container) {
        console.error('Elementos del modal de bracket no encontrados');
        return;
    }
    
    title.textContent = `Cuadro de Tenis - ${torneo.nombre}`;
    
    // Generar cuadro de tenis
    container.innerHTML = generateTennisBracket(inscripciones);
    
    modal.style.display = 'flex';
}

// Generar cuadro de tenis
function generateTennisBracket(inscripciones) {
    if (inscripciones.length === 0) {
        return '<div class="empty-bracket">No hay inscripciones en este torneo</div>';
    }
    
    // Ordenar inscripciones por fecha de inscripción
    const sortedInscripciones = inscripciones.sort((a, b) => new Date(a.fecha_inscripcion) - new Date(b.fecha_inscripcion));
    
    // Calcular número de rondas necesarias
    const numRounds = Math.ceil(Math.log2(sortedInscripciones.length));
    const totalSlots = Math.pow(2, numRounds);
    
    let html = '<div class="tennis-bracket">';
    
    // Generar rondas
    for (let round = 0; round < numRounds; round++) {
        const roundName = getRoundName(round, numRounds);
        const slotsInRound = Math.pow(2, numRounds - round);
        
        html += `<div class="bracket-round">
            <h3 class="round-title">${roundName}</h3>
            <div class="round-matches">`;
        
        for (let slot = 0; slot < slotsInRound; slot++) {
            const isFirstRound = round === 0;
            const isLastRound = round === numRounds - 1;
            
            html += `<div class="match-slot ${isFirstRound ? 'first-round' : ''} ${isLastRound ? 'final' : ''}">
                <div class="player-slot">
                    ${getPlayerForSlot(sortedInscripciones, round, slot, totalSlots)}
                </div>
                ${!isLastRound ? '<div class="match-connector"></div>' : ''}
            </div>`;
        }
        
        html += '</div></div>';
    }
    
    html += '</div>';
    return html;
}

// Obtener nombre de la ronda
function getRoundName(round, totalRounds) {
    const roundNames = {
        0: 'Primera Ronda',
        1: 'Segunda Ronda',
        2: 'Cuartos de Final',
        3: 'Semifinales',
        4: 'Final'
    };
    
    return roundNames[round] || `Ronda ${round + 1}`;
}

// Obtener jugador para un slot específico
function getPlayerForSlot(inscripciones, round, slot, totalSlots) {
    if (round === 0) {
        // Primera ronda - mostrar inscripciones reales
        const playerIndex = slot * 2;
        if (playerIndex < inscripciones.length) {
            const player1 = inscripciones[playerIndex];
            const player2 = playerIndex + 1 < inscripciones.length ? inscripciones[playerIndex + 1] : null;
            
            let html = `<div class="player-name">${player1.deportista_nombre || 'Jugador'}</div>`;
            if (player2) {
                html += `<div class="vs">VS</div>`;
                html += `<div class="player-name">${player2.deportista_nombre || 'Jugador'}</div>`;
            } else {
                html += `<div class="bye">BYE</div>`;
            }
            return html;
        }
    }
    
    // Otras rondas - mostrar slots vacíos
    return '<div class="empty-slot">Por definir</div>';
}

// Cerrar modal de cuadro de tenis
function closeTennisBracketModal() {
    const modal = document.getElementById('tennisBracketModal');
    if (modal) {
        modal.style.display = 'none';
    }
}
