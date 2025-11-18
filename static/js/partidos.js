// Gestión de Partidos
let partidos = [];
let torneos = [];
let deportistas = [];
let currentPartido = null;

async function setupPartidosUI() {
    const user = auth.getUser();
    if (!user) {
        console.error('Usuario no autenticado');
        return;
    }

    const headerActions = document.querySelector('#section-partidos .header-right');
    const subtitle = document.querySelector('#section-partidos .subtitle');

    if (!headerActions || !subtitle) {
        console.error('Elementos de UI de partidos no encontrados');
        return;
    }

    // Configurar UI según el rol
    if (user.perfil === 'deportista') {
        // Deportistas solo ven partidos
        headerActions.style.display = 'none';
        subtitle.textContent = 'Mis Partidos y Resultados';
    } else if (user.perfil === 'administrador' || user.perfil === 'profesor') {
        // Admin y profesores pueden crear partidos
        subtitle.textContent = 'Gestión de Partidos y Resultados';
    }

    // Cargar datos iniciales
    await loadPartidos();
    
    console.log('Partidos UI configurada. Total partidos:', partidos.length);
}

async function loadPartidos() {
    try {
        const user = auth.getUser();
        let endpoint = '/api/partidos';
        
        // Si es deportista, cargar solo sus partidos
        if (user.perfil === 'deportista') {
            endpoint = `/api/partidos/deportista/${user.id}`;
        }
        
        console.log('Cargando partidos desde:', endpoint);
        const response = await api.get(endpoint);
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || 'Error al cargar partidos');
        }

        partidos = await response.json();
        console.log('Partidos cargados:', partidos);
        
        renderPartidos();
    } catch (error) {
        console.error('Error cargando partidos:', error);
        showNotification('Error al cargar partidos: ' + error.message, 'error');
    }
}

function renderPartidos() {
    const container = document.querySelector('#section-partidos .partidos-container');
    if (!container) {
        console.error('Container de partidos no encontrado');
        return;
    }

    const user = auth.getUser();
    console.log('Renderizando partidos. Total:', partidos.length);

    if (!partidos || partidos.length === 0) {
        container.innerHTML = '<p class="no-data">No hay partidos registrados</p>';
        return;
    }

    // Agrupar partidos por torneo
    const partidosPorTorneo = {};
    partidos.forEach(partido => {
        const torneoNombre = partido.torneo_nombre || 'Sin torneo';
        if (!partidosPorTorneo[torneoNombre]) {
            partidosPorTorneo[torneoNombre] = [];
        }
        partidosPorTorneo[torneoNombre].push(partido);
    });

    const html = `
        <div class="partidos-wrapper">
            ${Object.entries(partidosPorTorneo).map(([torneoNombre, partidosList]) => `
                <div class="torneo-partidos-section">
                    <h2 class="torneo-section-title">
                        <span class="tournament-icon">🎾</span>
                        ${torneoNombre}
                    </h2>
                    <div class="partidos-grid">
                        ${partidosList.map(partido => renderPartidoCard(partido, user)).join('')}
                    </div>
                </div>
            `).join('')}
        </div>
    `;

    container.innerHTML = html;
}

function renderPartidoCard(partido, user) {
    const deportista1Nombre = partido.deportista1_nombre || 'TBD';
    const deportista2Nombre = partido.deportista2_nombre || 'TBD';
    
    // Determinar sets ganados desde el resultado JSON
    let sets1 = 0;
    let sets2 = 0;
    
    if (partido.resultado) {
        try {
            const resultado = typeof partido.resultado === 'string' ? JSON.parse(partido.resultado) : partido.resultado;
            if (resultado.sets && Array.isArray(resultado.sets)) {
                resultado.sets.forEach(set => {
                    if (set.jugador1 > set.jugador2) sets1++;
                    if (set.jugador2 > set.jugador1) sets2++;
                });
            }
        } catch (e) {
            console.error('Error parseando resultado:', e);
        }
    }
    
    // Determinar ganador
    const ganadorId = partido.ganador_id;
    const deportista1Ganador = ganadorId === partido.deportista1_id;
    const deportista2Ganador = ganadorId === partido.deportista2_id;
    
    // Determinar estado del partido
    const estado = partido.estado || 'programado';
    const estadoBadgeClass = {
        'programado': 'badge-warning',
        'en_curso': 'badge-info',
        'finalizado': 'badge-success',
        'cancelado': 'badge-danger'
    }[estado] || 'badge-secondary';

    return `
        <div class="partido-card ${estado === 'finalizado' ? 'partido-finalizado' : ''}">
            <div class="partido-card-header">
                <div class="partido-info">
                    <span class="partido-ronda">${partido.ronda || 'Ronda 1'}</span>
                    <span class="badge ${estadoBadgeClass}">${estado}</span>
                </div>
                ${partido.fecha_partido ? `
                    <div class="partido-fecha">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                            <line x1="16" y1="2" x2="16" y2="6"></line>
                            <line x1="8" y1="2" x2="8" y2="6"></line>
                            <line x1="3" y1="10" x2="21" y2="10"></line>
                        </svg>
                        ${formatDateShort(partido.fecha_partido)}
                    </div>
                ` : ''}
            </div>
            
            <div class="partido-card-body">
                <div class="partido-matchup">
                    <div class="jugador ${deportista1Ganador ? 'jugador-ganador' : ''} ${estado === 'programado' ? 'jugador-programado' : ''}">
                        <div class="jugador-info">
                            <div class="jugador-avatar">${deportista1Nombre.charAt(0).toUpperCase()}</div>
                            <span class="jugador-nombre">${deportista1Nombre}</span>
                        </div>
                        <div class="jugador-score">
                            ${estado !== 'programado' ? `<span class="sets-count">${sets1}</span>` : ''}
                        </div>
                    </div>
                    
                    <div class="vs-divider">
                        <span>VS</span>
                    </div>
                    
                    <div class="jugador ${deportista2Ganador ? 'jugador-ganador' : ''} ${estado === 'programado' ? 'jugador-programado' : ''}">
                        <div class="jugador-info">
                            <div class="jugador-avatar">${deportista2Nombre.charAt(0).toUpperCase()}</div>
                            <span class="jugador-nombre">${deportista2Nombre}</span>
                        </div>
                        <div class="jugador-score">
                            ${estado !== 'programado' ? `<span class="sets-count">${sets2}</span>` : ''}
                        </div>
                    </div>
                </div>
                
                ${partido.resultado_detalle ? `
                    <div class="partido-detalle">
                        <small>${partido.resultado_detalle}</small>
                    </div>
                ` : ''}
            </div>
            
            ${(user.perfil === 'administrador' || user.perfil === 'profesor') && estado !== 'finalizado' ? `
                <div class="partido-card-footer">
                    <button class="btn-sm btn-primary" onclick="openEditPartido(${partido.id})">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                        </svg>
                        Registrar Resultado
                    </button>
                    <button class="btn-sm btn-danger" onclick="deletePartido(${partido.id})">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        </svg>
                        Eliminar
                    </button>
                </div>
            ` : ''}
        </div>
    `;
}

async function openEditPartido(partidoId) {
    const partido = partidos.find(p => p.id === partidoId);
    if (!partido) {
        showNotification('Partido no encontrado', 'error');
        return;
    }

    currentPartido = partido;
    
    // Crear modal para registrar resultado
    const modalHtml = `
        <div id="resultadoPartidoModal" class="modal" style="display: block;">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>Registrar Resultado</h2>
                    <button class="close-btn" onclick="closeResultadoModal()">&times;</button>
                </div>
                
                <div class="modal-body">
                    <div class="partido-resumen">
                        <h3>${partido.deportista1_nombre} vs ${partido.deportista2_nombre}</h3>
                        <p>${partido.torneo_nombre} - ${partido.ronda || 'Ronda 1'}</p>
                    </div>
                    
                    <form id="resultadoForm" onsubmit="event.preventDefault(); saveResultado();">
                        <div class="form-row">
                            <div class="form-group">
                                <label for="sets-deportista1">Sets ganados - ${partido.deportista1_nombre}</label>
                                <input type="number" id="sets-deportista1" min="0" max="5" value="${partido.sets_ganados_deportista1 || 0}" required>
                            </div>
                            
                            <div class="form-group">
                                <label for="sets-deportista2">Sets ganados - ${partido.deportista2_nombre}</label>
                                <input type="number" id="sets-deportista2" min="0" max="5" value="${partido.sets_ganados_deportista2 || 0}" required>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label for="resultado-detalle">Detalle del Resultado (Opcional)</label>
                            <input type="text" id="resultado-detalle" placeholder="Ej: 6-4, 6-3, 7-5" value="${partido.resultado_detalle || ''}">
                        </div>
                        
                        <div class="form-group">
                            <label for="estado-partido">Estado</label>
                            <select id="estado-partido" required>
                                <option value="programado" ${partido.estado === 'programado' ? 'selected' : ''}>Programado</option>
                                <option value="en_curso" ${partido.estado === 'en_curso' ? 'selected' : ''}>En Curso</option>
                                <option value="finalizado" ${partido.estado === 'finalizado' ? 'selected' : ''}>Finalizado</option>
                                <option value="cancelado" ${partido.estado === 'cancelado' ? 'selected' : ''}>Cancelado</option>
                            </select>
                        </div>
                        
                        <div class="form-actions">
                            <button type="button" class="btn btn-secondary" onclick="closeResultadoModal()">Cancelar</button>
                            <button type="submit" class="btn btn-primary">Guardar Resultado</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    `;
    
    // Agregar modal al DOM
    const existingModal = document.getElementById('resultadoPartidoModal');
    if (existingModal) {
        existingModal.remove();
    }
    document.body.insertAdjacentHTML('beforeend', modalHtml);
}

function closeResultadoModal() {
    const modal = document.getElementById('resultadoPartidoModal');
    if (modal) {
        modal.remove();
    }
    currentPartido = null;
}

async function saveResultado() {
    if (!currentPartido) {
        showNotification('Error: No hay partido seleccionado', 'error');
        return;
    }

    try {
        const sets1 = parseInt(document.getElementById('sets-deportista1').value);
        const sets2 = parseInt(document.getElementById('sets-deportista2').value);
        const detalle = document.getElementById('resultado-detalle').value;

        // Validar que se ingresaron los sets
        if (isNaN(sets1) || isNaN(sets2)) {
            showNotification('Por favor ingrese los sets ganados', 'error');
            return;
        }

        // Determinar ganador
        let ganadorId = null;
        if (sets1 > sets2) {
            ganadorId = currentPartido.deportista1_id;
        } else if (sets2 > sets1) {
            ganadorId = currentPartido.deportista2_id;
        } else {
            showNotification('Debe haber un ganador (sets diferentes)', 'error');
            return;
        }

        // Construir resultado JSON con estructura de sets
        const resultado = {
            sets: [
                { jugador1: sets1, jugador2: sets2 }
            ],
            detalle: detalle
        };

        const data = {
            ganador_id: ganadorId,
            resultado: resultado
        };

        console.log('Registrando resultado:', data);
        
        // Usar el endpoint específico para registrar resultados
        const response = await api.post(`/api/partidos/${currentPartido.id}/resultado`, data);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error al registrar resultado');
        }

        const result = await response.json();
        console.log('Resultado registrado:', result);
        
        // Mostrar mensaje con información del siguiente partido
        let mensaje = '✅ Resultado registrado exitosamente';
        if (result.siguiente_partido) {
            const siguientePartido = result.siguiente_partido;
            const rival = siguientePartido.deportista2_nombre || 'Por definir';
            mensaje += `\n\n🎾 Siguiente partido creado:\n${siguientePartido.ronda}\nRival: ${rival}`;
        }
        
        showNotification(mensaje, 'success');
        closeResultadoModal();
        await loadPartidos();
    } catch (error) {
        console.error('Error registrando resultado:', error);
        showNotification(error.message, 'error');
    }
}


async function deletePartido(partidoId) {
    if (!confirm('¿Está seguro de eliminar este partido?')) {
        return;
    }

    try {
        const response = await api.delete(`/api/partidos/${partidoId}`);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error al eliminar partido');
        }

        showNotification('Partido eliminado exitosamente', 'success');
        await loadPartidos();
    } catch (error) {
        console.error('Error eliminando partido:', error);
        showNotification(error.message, 'error');
    }
}

function formatDateShort(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: 'short'
    });
}

function showNotification(message, type = 'info') {
    if (window.showNotification) {
        window.showNotification(message, type);
    } else {
        alert(message);
    }
}
