// Funcionalidad de torneos
let currentEditingTorneoId = null;
let currentTorneoEnCuadro = null; // Guardar el torneo actual del cuadro

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
async function showTennisBracket(torneo, inscripciones) {
    const modal = document.getElementById('tennisBracketModal');
    const title = document.getElementById('bracketTitle');
    const container = document.getElementById('tennisBracketContainer');
    
    if (!modal || !title || !container) {
        console.error('Elementos del modal de bracket no encontrados');
        return;
    }
    
    // Guardar torneo actual
    currentTorneoEnCuadro = { torneo, inscripciones };
    
    title.textContent = `Cuadro de Tenis - ${torneo.nombre}`;
    
    // Cargar partidos del torneo
    try {
        const partidos = await api.request(`/api/torneos/${torneo.id}/partidos`);
        console.log('Partidos del torneo:', partidos);
        
        // Generar cuadro de tenis con los partidos
        container.innerHTML = generateTennisBracket(inscripciones, partidos);
    } catch (error) {
        console.error('Error cargando partidos del torneo:', error);
        // Si falla, mostrar cuadro básico sin partidos
        container.innerHTML = generateTennisBracket(inscripciones, []);
    }
    
    modal.style.display = 'flex';
}

// Función global para recargar el cuadro actual
window.recargarCuadroActual = async function() {
    if (currentTorneoEnCuadro) {
        console.log('Recargando cuadro del torneo:', currentTorneoEnCuadro.torneo.nombre);
        await showTennisBracket(currentTorneoEnCuadro.torneo, currentTorneoEnCuadro.inscripciones);
    }
};

// Generar cuadro de tenis
function generateTennisBracket(inscripciones, partidos = []) {
    if (inscripciones.length === 0) {
        return '<div class="empty-bracket">No hay inscripciones en este torneo</div>';
    }
    
    // Agrupar partidos por ronda
    const partidosPorRonda = {};
    partidos.forEach(partido => {
        const rondaNum = partido.numero_ronda || 1;
        if (!partidosPorRonda[rondaNum]) {
            partidosPorRonda[rondaNum] = [];
        }
        partidosPorRonda[rondaNum].push(partido);
    });
    
    console.log('Partidos por ronda:', partidosPorRonda);
    
    // Calcular número de rondas necesarias
    const numRounds = Math.ceil(Math.log2(inscripciones.length));
    
    let html = '<div class="tennis-bracket">';
    
    // Generar rondas
    for (let round = 0; round < numRounds; round++) {
        const roundName = getRoundName(round, numRounds);
        const rondaNum = round + 1;
        const partidosRonda = partidosPorRonda[rondaNum] || [];
        
        html += `<div class="bracket-round">
            <h3 class="round-title">${roundName}</h3>
            <div class="round-matches">`;
        
        // Mostrar partidos de esta ronda
        if (partidosRonda.length > 0) {
            partidosRonda.forEach(partido => {
                html += renderPartidoEnCuadro(partido);
            });
        } else {
            // Mostrar slots vacíos si no hay partidos aún
            const numPartidos = Math.pow(2, numRounds - round - 1);
            for (let i = 0; i < numPartidos; i++) {
                html += `<div class="match-slot">
                    <div class="player-slot">Por definir</div>
                    <div class="vs-text">vs</div>
                    <div class="player-slot">Por definir</div>
                </div>`;
            }
        }
        
        html += '</div></div>';
    }
    
    html += '</div>';
    return html;
}

// Renderizar un partido en el cuadro
function renderPartidoEnCuadro(partido) {
    const deportista1 = partido.deportista1_nombre || 'Por definir';
    const deportista2 = partido.deportista2_nombre || 'Por definir';
    const ganadorId = partido.ganador_id;
    const estado = partido.estado || 'programado';
    
    const esGanador1 = ganadorId === partido.deportista1_id;
    const esGanador2 = ganadorId === partido.deportista2_id;
    
    // Obtener sets ganados del resultado
    let sets1 = '-';
    let sets2 = '-';
    
    if (partido.resultado && estado === 'finalizado') {
        try {
            const resultado = typeof partido.resultado === 'string' ? JSON.parse(partido.resultado) : partido.resultado;
            if (resultado.sets && Array.isArray(resultado.sets)) {
                let setsGanados1 = 0;
                let setsGanados2 = 0;
                resultado.sets.forEach(set => {
                    if (set.jugador1 > set.jugador2) setsGanados1++;
                    if (set.jugador2 > set.jugador1) setsGanados2++;
                });
                sets1 = setsGanados1;
                sets2 = setsGanados2;
            }
        } catch (e) {
            console.error('Error parseando resultado:', e);
        }
    }
    
    const fecha = partido.fecha_partido ? new Date(partido.fecha_partido).toLocaleDateString('es-ES', { 
        day: '2-digit', 
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }) : '';
    
    return `
        <div class="bracket-match ${estado}">
            <div class="match-header">
                ${estado === 'finalizado' ? '<span class="match-status finalized">✓</span>' : ''}
                ${fecha ? `<span class="match-date">${fecha}</span>` : ''}
            </div>
            <div class="match-players">
                <div class="player-row ${esGanador1 ? 'winner' : ''} ${estado === 'finalizado' && !esGanador1 ? 'loser' : ''}">
                    <div class="player-info">
                        ${esGanador1 ? '<span class="trophy-icon">🏆</span>' : ''}
                        <span class="player-name">${deportista1}</span>
                    </div>
                    <div class="player-score ${esGanador1 ? 'winner-score' : ''}">${sets1}</div>
                </div>
                <div class="player-row ${esGanador2 ? 'winner' : ''} ${estado === 'finalizado' && !esGanador2 ? 'loser' : ''}">
                    <div class="player-info">
                        ${esGanador2 ? '<span class="trophy-icon">🏆</span>' : ''}
                        <span class="player-name">${deportista2}</span>
                    </div>
                    <div class="player-score ${esGanador2 ? 'winner-score' : ''}">${sets2}</div>
                </div>
            </div>
            ${partido.resultado_detalle && estado === 'finalizado' ? `
                <div class="match-details">${partido.resultado_detalle}</div>
            ` : ''}
        </div>
    `;
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
