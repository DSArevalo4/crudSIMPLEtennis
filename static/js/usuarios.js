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

// Cargar lista de usuarios
async function loadUsuarios() {
    try {
        const perfil = document.getElementById('filterPerfil')?.value || '';
        const activo = document.getElementById('filterActivo')?.value || '';
        const search = document.getElementById('searchUsuarios')?.value || '';
        
        const response = await fetch(`${API_BASE}/usuarios`, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                auth.redirectToLogin();
                return;
            }
            throw new Error(`Error ${response.status}`);
        }
        
        let usuarios = await response.json();
        
        // Aplicar filtros
        if (perfil) {
            usuarios = usuarios.filter(u => u.perfil === perfil);
        }
        
        if (activo) {
            const isActive = activo === 'true';
            usuarios = usuarios.filter(u => u.activo === isActive);
        }
        
        if (search) {
            const searchLower = search.toLowerCase();
            usuarios = usuarios.filter(u => 
                u.nombre.toLowerCase().includes(searchLower) ||
                u.apellido.toLowerCase().includes(searchLower) ||
                u.email.toLowerCase().includes(searchLower) ||
                u.username.toLowerCase().includes(searchLower)
            );
        }
        
        renderUsuariosList(usuarios);
        
    } catch (error) {
        console.error('Error cargando usuarios:', error);
        showNotification('Error al cargar usuarios', 'error');
    }
}

// Renderizar lista de usuarios
function renderUsuariosList(usuarios) {
    const container = document.getElementById('usuariosList');
    
    if (!container) {
        console.error('Contenedor de usuarios no encontrado');
        return;
    }
    
    if (usuarios.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <p>No hay usuarios que mostrar</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = usuarios.map(usuario => `
        <div class="usuario-card" data-id="${usuario.id}">
            <div class="usuario-avatar">
                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=${usuario.username}" alt="${usuario.nombre}">
            </div>
            <div class="usuario-info">
                <h3>${usuario.nombre} ${usuario.apellido}</h3>
                <p class="usuario-email">${usuario.email}</p>
                <p class="usuario-username">@${usuario.username}</p>
                <div class="usuario-badges">
                    <span class="badge badge-${usuario.perfil}">${usuario.perfil}</span>
                    <span class="badge badge-${usuario.activo ? 'active' : 'inactive'}">
                        ${usuario.activo ? 'Activo' : 'Inactivo'}
                    </span>
                </div>
            </div>
            <div class="usuario-actions">
                <button class="btn btn-sm btn-primary" onclick="editUsuario(${usuario.id})" title="Editar">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                    </svg>
                </button>
                <button class="btn btn-sm ${usuario.activo ? 'btn-warning' : 'btn-success'}" 
                        onclick="toggleUsuarioStatus(${usuario.id}, ${!usuario.activo})" 
                        title="${usuario.activo ? 'Desactivar' : 'Activar'}">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        ${usuario.activo ? 
                            '<path d="M18 6L6 18M6 6l12 12"/>' : 
                            '<polyline points="20 6 9 17 4 12"></polyline>'}
                    </svg>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteUsuario(${usuario.id})" title="Eliminar">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                </button>
            </div>
        </div>
    `).join('');
}

// Abrir formulario de usuario
function openUsuarioForm(usuarioId = null) {
    const modal = document.getElementById('usuarioFormModal');
    const form = document.getElementById('usuarioForm');
    const title = document.getElementById('usuarioFormTitle');
    const passwordGroup = document.getElementById('passwordGroup');
    const passwordInput = document.getElementById('usuarioPassword');
    
    if (!modal || !form) {
        console.error('Modal o formulario no encontrado');
        return;
    }
    
    // Limpiar formulario
    form.reset();
    delete form.dataset.usuarioId;
    
    if (usuarioId) {
        // Modo edición
        title.textContent = 'Editar Usuario';
        passwordGroup.style.display = 'none';
        passwordInput.removeAttribute('required');
        loadUsuarioData(usuarioId);
    } else {
        // Modo creación
        title.textContent = 'Crear Usuario';
        passwordGroup.style.display = 'block';
        passwordInput.setAttribute('required', 'required');
    }
    
    modal.style.display = 'block';
}

// Cargar datos de usuario para edición
async function loadUsuarioData(usuarioId) {
    try {
        const response = await fetch(`${API_BASE}/usuarios/${usuarioId}`, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Error al cargar usuario');
        }
        
        const usuario = await response.json();
        
        // Llenar formulario con datos
        document.getElementById('usuarioNombre').value = usuario.nombre || '';
        document.getElementById('usuarioApellido').value = usuario.apellido || '';
        document.getElementById('usuarioEmail').value = usuario.email || '';
        document.getElementById('usuarioTelefono').value = usuario.telefono || '';
        document.getElementById('usuarioUsername').value = usuario.username || '';
        document.getElementById('usuarioPerfil').value = usuario.perfil || '';
        document.getElementById('usuarioActivo').checked = usuario.activo;
        
        // Guardar ID para actualización
        document.getElementById('usuarioForm').dataset.usuarioId = usuarioId;
        
    } catch (error) {
        console.error('Error cargando datos del usuario:', error);
        showNotification('Error al cargar datos del usuario', 'error');
    }
}

// Cerrar formulario de usuario
function closeUsuarioFormModal() {
    const modal = document.getElementById('usuarioFormModal');
    if (modal) {
        modal.style.display = 'none';
    }
    
    const form = document.getElementById('usuarioForm');
    if (form) {
        form.reset();
        delete form.dataset.usuarioId;
    }
}

// Manejar submit del formulario
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('usuarioForm');
    if (form) {
        form.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            const submitBtn = form.querySelector('button[type="submit"]');
            const usuarioId = form.dataset.usuarioId;
            
            // Obtener datos del formulario
            const formData = {
                nombre: document.getElementById('usuarioNombre').value.trim(),
                apellido: document.getElementById('usuarioApellido').value.trim(),
                email: document.getElementById('usuarioEmail').value.trim(),
                telefono: document.getElementById('usuarioTelefono').value.trim(),
                username: document.getElementById('usuarioUsername').value.trim(),
                perfil: document.getElementById('usuarioPerfil').value,
                activo: document.getElementById('usuarioActivo').checked
            };
            
            // Solo incluir password si es creación o si se cambió
            const password = document.getElementById('usuarioPassword').value;
            if (password) {
                formData.password = password;
            }
            
            console.log('📤 Enviando datos:', formData);
            
            // Validar datos
            if (!formData.nombre || !formData.apellido || !formData.email || !formData.username || !formData.perfil) {
                showNotification('Todos los campos obligatorios deben estar completos', 'error');
                return;
            }
            
            // Deshabilitar botón durante envío
            submitBtn.disabled = true;
            submitBtn.textContent = usuarioId ? 'Actualizando...' : 'Creando...';
            
            try {
                const url = usuarioId ? `${API_BASE}/usuarios/${usuarioId}` : `${API_BASE}/usuarios`;
                const method = usuarioId ? 'PUT' : 'POST';
                
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
                console.log('✅ Usuario guardado:', result);
                
                showNotification(
                    usuarioId ? 'Usuario actualizado exitosamente' : 'Usuario creado exitosamente',
                    'success'
                );
                
                closeUsuarioFormModal();
                loadUsuarios(); // Recargar lista
                
            } catch (error) {
                console.error('❌ Error:', error);
                showNotification(`Error: ${error.message}`, 'error');
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Guardar';
            }
        });
    }
});

// Editar usuario
function editUsuario(usuarioId) {
    openUsuarioForm(usuarioId);
}

// Toggle estado de usuario
async function toggleUsuarioStatus(usuarioId, newStatus) {
    try {
        const response = await fetch(`${API_BASE}/usuarios/${usuarioId}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify({ activo: newStatus })
        });
        
        if (!response.ok) {
            throw new Error('Error al cambiar estado del usuario');
        }
        
        showNotification(
            `Usuario ${newStatus ? 'activado' : 'desactivado'} exitosamente`,
            'success'
        );
        
        loadUsuarios(); // Recargar lista
        
    } catch (error) {
        console.error('Error cambiando estado:', error);
        showNotification('Error al cambiar estado del usuario', 'error');
    }
}

// Eliminar usuario
async function deleteUsuario(usuarioId) {
    if (!confirm('¿Estás seguro de que deseas eliminar este usuario?\n\nEsta acción no se puede deshacer.')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/usuarios/${usuarioId}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Error al eliminar usuario');
        }
        
        showNotification('Usuario eliminado exitosamente', 'success');
        loadUsuarios(); // Recargar lista
        
    } catch (error) {
        console.error('Error eliminando usuario:', error);
        showNotification('Error al eliminar usuario: ' + error.message, 'error');
    }
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

// Exponer funciones globalmente
window.loadUsuarios = loadUsuarios;
window.openUsuarioForm = openUsuarioForm;
window.closeUsuarioFormModal = closeUsuarioFormModal;
window.editUsuario = editUsuario;
window.toggleUsuarioStatus = toggleUsuarioStatus;
window.deleteUsuario = deleteUsuario;
