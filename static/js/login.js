// Login page functionality
document.addEventListener('DOMContentLoaded', function() {
  const loginForm = document.getElementById('loginForm')
  const registerForm = document.getElementById('registerForm')
  const loginBtn = document.getElementById('loginBtn')
  const registerBtn = document.getElementById('registerBtn')
  const toggleLoginBtn = document.getElementById('toggleLogin')
  const toggleRegisterBtn = document.getElementById('toggleRegister')
  const toggleToLogin = document.getElementById('toggleToLogin')
  const toggleToRegister = document.getElementById('toggleToRegister')
  const errorMessage = document.getElementById('errorMessage')
  const successMessage = document.getElementById('successMessage')
  const regErrorMessage = document.getElementById('regErrorMessage')
  const regSuccessMessage = document.getElementById('regSuccessMessage')

  // Toggle between login and register forms
  function toggleForms(showLogin) {
    if (showLogin) {
      loginForm.classList.add('active')
      registerForm.classList.remove('active')
      toggleToRegister.style.display = 'block'
      toggleToLogin.style.display = 'none'
    } else {
      loginForm.classList.remove('active')
      registerForm.classList.add('active')
      toggleToRegister.style.display = 'none'
      toggleToLogin.style.display = 'block'
    }
    clearMessages()
  }

  function clearMessages() {
    if (errorMessage) errorMessage.style.display = 'none'
    if (successMessage) successMessage.style.display = 'none'
    if (regErrorMessage) regErrorMessage.style.display = 'none'
    if (regSuccessMessage) regSuccessMessage.style.display = 'none'
  }

  function showError(message, isRegister = false) {
    const msgElement = isRegister ? regErrorMessage : errorMessage
    if (msgElement) {
      msgElement.textContent = message
      msgElement.style.display = 'block'
    }
  }

  function showSuccess(message, isRegister = false) {
    const msgElement = isRegister ? regSuccessMessage : successMessage
    if (msgElement) {
      msgElement.textContent = message
      msgElement.style.display = 'block'
    }
  }

  function setLoading(button, isLoading) {
    const text = button.querySelector('span:not(.loader)')
    const loader = button.querySelector('.loader')
    
    if (isLoading) {
      button.disabled = true
      if (text) text.style.display = 'none'
      if (loader) loader.style.display = 'inline-block'
    } else {
      button.disabled = false
      if (text) text.style.display = 'inline'
      if (loader) loader.style.display = 'none'
    }
  }

  // Login form submission
  if (loginForm) {
    loginForm.addEventListener('submit', async function(e) {
      e.preventDefault()
      clearMessages()

      const email = document.getElementById('email').value
      const password = document.getElementById('password').value

      if (!email || !password) {
        showError('Por favor completa todos los campos')
        return
      }

      try {
        setLoading(loginBtn, true)
        const response = await api.login(email, password)
        
        if (response.token && response.user) {
          auth.setAuth(response.token, response.user)
          showSuccess('Inicio de sesión exitoso')
          
          // Redirect to dashboard after short delay
          setTimeout(() => {
            window.location.href = '/dashboard'
          }, 1000)
        } else {
          showError('Credenciales inválidas')
        }
      } catch (error) {
        showError(error.message || 'Error al iniciar sesión')
      } finally {
        setLoading(loginBtn, false)
      }
    })
  }

  // Register form submission
  if (registerForm) {
    registerForm.addEventListener('submit', async function(e) {
      e.preventDefault()
      clearMessages()

      const userData = {
        nombre: document.getElementById('regNombre').value,
        apellido: document.getElementById('regApellido').value,
        email: document.getElementById('regEmail').value,
        telefono: document.getElementById('regTelefono').value,
        username: document.getElementById('regUsername').value,
        password: document.getElementById('regPassword').value,
        perfil: 'deportista' // Solo deportistas pueden registrarse
      }

      // Validate required fields
      const requiredFields = ['nombre', 'apellido', 'email', 'username', 'password']
      const missingFields = requiredFields.filter(field => !userData[field])
      
      if (missingFields.length > 0) {
        showError('Por favor completa todos los campos obligatorios', true)
        return
      }

      // Validate password confirmation
      const confirmPassword = document.getElementById('confirmPassword').value
      if (userData.password !== confirmPassword) {
        showError('Las contraseñas no coinciden', true)
        return
      }

      try {
        setLoading(registerBtn, true)
        const response = await api.register(userData)
        
        if (response.message || response.id) {
          showSuccess('Usuario registrado exitosamente. Ahora puedes iniciar sesión.', true)
          // Switch to login form after successful registration
          setTimeout(() => {
            toggleForms(true)
            document.getElementById('email').value = userData.email
          }, 2000)
        } else {
          showError('Error al registrar usuario', true)
        }
      } catch (error) {
        showError(error.message || 'Error al registrar usuario', true)
      } finally {
        setLoading(registerBtn, false)
      }
    })
  }

  // Toggle buttons
  if (toggleLoginBtn) {
    toggleLoginBtn.addEventListener('click', () => toggleForms(true))
  }

  if (toggleRegisterBtn) {
    toggleRegisterBtn.addEventListener('click', () => toggleForms(false))
  }

  // Initialize with login form
  toggleForms(true)
})
