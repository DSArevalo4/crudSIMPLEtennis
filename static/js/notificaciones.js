// Gestión de Notificaciones
let notificacionesData = [];

async function setupNotificacionesUI() {
    console.log('🔔 setupNotificacionesUI() EJECUTÁNDOSE...');
    const user = auth.getUser();
    if (!user) {
        console.error('❌ Usuario no autenticado');
        return;
    }

    // Cargar notificaciones
    await loadNotificaciones();
    
    // Actualizar badge en el sidebar
    updateNotificacionesBadge();
}

async function loadNotificaciones() {
    const container = document.getElementById('notificacionesList');
    if (!container) return;

    container.innerHTML = '<div class="loading">Cargando notificaciones...</div>';

    try {
        const user = auth.getUser();
        const response = await api.request(`/api/notificaciones/deportista/${user.id}?limite=50`);
        
        notificacionesData = response;
        console.log('Notificaciones cargadas:', notificacionesData.length);
        
        renderNotificaciones();
    } catch (error) {
        console.error('Error cargando notificaciones:', error);
        container.innerHTML = `<p class="error-message">Error al cargar notificaciones: ${error.message}</p>`;
    }
}

function renderNotificaciones() {
    const container = document.getElementById('notificacionesList');
    if (!container) return;

    if (!notificacionesData || notificacionesData.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                    <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                </svg>
                <h3>No tienes notificaciones</h3>
                <p>Cuando tengas partidos programados aparecerán aquí</p>
            </div>
        `;
        return;
    }

    // Separar en leídas y no leídas
    const noLeidas = notificacionesData.filter(n => !n.leida);
    const leidas = notificacionesData.filter(n => n.leida);

    let html = '';

    if (noLeidas.length > 0) {
        html += '<h2 class="notificaciones-section-title">Nuevas</h2>';
        html += '<div class="notificaciones-grid">';
        noLeidas.forEach(notif => {
            html += renderNotificacionCard(notif, false);
        });
        html += '</div>';
    }

    if (leidas.length > 0) {
        html += '<h2 class="notificaciones-section-title">Anteriores</h2>';
        html += '<div class="notificaciones-grid">';
        leidas.forEach(notif => {
            html += renderNotificacionCard(notif, true);
        });
        html += '</div>';
    }

    container.innerHTML = html;
}

function renderNotificacionCard(notif, esLeida) {
    const iconos = {
        'partido_programado': '🎾',
        'victoria': '🏆',
        'derrota': '💪',
        'recordatorio': '⏰',
        'nueva_ronda': '🎯',
        'inscripcion_aceptada': '✅'
    };

    const colores = {
        'partido_programado': '#4169e1',
        'victoria': '#10b981',
        'derrota': '#f59e0b',
        'recordatorio': '#8b5cf6',
        'nueva_ronda': '#ec4899',
        'inscripcion_aceptada': '#10b981'
    };

    const icono = iconos[notif.tipo] || '📧';
    const color = colores[notif.tipo] || '#6b7280';
    const fechaRelativa = getRelativeTime(notif.fecha_creacion);

    return `
        <div class="notificacion-card ${esLeida ? 'leida' : 'no-leida'}" 
             onclick="marcarComoLeida(${notif.id})"
             style="border-left: 4px solid ${color}">
            <div class="notificacion-icono" style="background-color: ${color}20">
                <span style="font-size: 24px">${icono}</span>
            </div>
            <div class="notificacion-contenido">
                <h3 class="notificacion-titulo">${notif.titulo}</h3>
                <p class="notificacion-mensaje">${notif.mensaje}</p>
                <div class="notificacion-footer">
                    <span class="notificacion-fecha">${fechaRelativa}</span>
                    ${!esLeida ? '<span class="notificacion-badge">Nueva</span>' : ''}
                </div>
            </div>
        </div>
    `;
}

async function marcarComoLeida(notificacionId) {
    try {
        const user = auth.getUser();
        await api.request(`/api/notificaciones/${notificacionId}/leer`, {
            method: 'PUT',
            body: JSON.stringify({ deportista_id: user.id })
        });

        // Actualizar localmente
        const notif = notificacionesData.find(n => n.id === notificacionId);
        if (notif) {
            notif.leida = true;
        }

        renderNotificaciones();
        updateNotificacionesBadge();
    } catch (error) {
        console.error('Error marcando notificación como leída:', error);
    }
}

async function marcarTodasLeidas() {
    try {
        const user = auth.getUser();
        await api.request(`/api/notificaciones/deportista/${user.id}/leer-todas`, {
            method: 'PUT'
        });

        // Actualizar localmente
        notificacionesData.forEach(n => n.leida = true);

        renderNotificaciones();
        updateNotificacionesBadge();
        
        showNotification('Todas las notificaciones marcadas como leídas', 'success');
    } catch (error) {
        console.error('Error marcando todas como leídas:', error);
        showNotification('Error al marcar notificaciones', 'error');
    }
}

async function updateNotificacionesBadge() {
    try {
        const user = auth.getUser();
        const response = await api.request(`/api/notificaciones/deportista/${user.id}/no-leidas/count`);
        
        const badge = document.querySelector('.nav-item[data-section="notificaciones"] .badge');
        
        if (response.count > 0) {
            if (badge) {
                badge.textContent = response.count;
                badge.style.display = 'inline-block';
            } else {
                // Crear badge si no existe
                const navItem = document.querySelector('.nav-item[data-section="notificaciones"]');
                if (navItem) {
                    const newBadge = document.createElement('span');
                    newBadge.className = 'badge';
                    newBadge.textContent = response.count;
                    newBadge.style.cssText = 'background: #ef4444; color: white; border-radius: 12px; padding: 2px 8px; font-size: 12px; margin-left: 8px;';
                    navItem.appendChild(newBadge);
                }
            }
        } else if (badge) {
            badge.style.display = 'none';
        }
    } catch (error) {
        console.error('Error actualizando badge de notificaciones:', error);
    }
}

function getRelativeTime(dateString) {
    if (!dateString) return 'Ahora';
    
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Ahora';
    if (diffMins < 60) return `Hace ${diffMins} min`;
    if (diffHours < 24) return `Hace ${diffHours}h`;
    if (diffDays < 7) return `Hace ${diffDays}d`;
    
    return date.toLocaleDateString('es-ES', { day: '2-digit', month: 'short' });
}

function showNotification(message, type = 'info') {
    if (window.showNotification) {
        window.showNotification(message, type);
    } else {
        alert(message);
    }
}

// Actualizar badge al cargar el dashboard
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(updateNotificacionesBadge, 1000);
});
