document.addEventListener('DOMContentLoaded', () => {
  const registerForm = document.getElementById('registerForm');
  const submitBtn = document.getElementById('submitBtn');
  const btnSpinner = document.getElementById('btnSpinner');
  const btnText = document.getElementById('btnText');
  const btnIcon = document.getElementById('btnIcon');

  const firstNameInput = document.getElementById('first_name');
  const lastNameInput = document.getElementById('last_name');
  const emailInput = document.getElementById('email');
  const ageInput = document.getElementById('age');
  const passwordInput = document.getElementById('password');
  const confirmPasswordInput = document.getElementById('confirm_password');

  const togglePasswordBtns = document.querySelectorAll('.toggle-password');

  // SVG Icons for password toggle state
  const eyeOpenSvg = `
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
      <circle cx="12" cy="12" r="3"></circle>
    </svg>
  `;

  const eyeClosedSvg = `
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
      <line x1="1" y1="1" x2="23" y2="23"></line>
    </svg>
  `;

  // Toggle password visibility with SVG replacement
  togglePasswordBtns.forEach((btn) => {
    btn.innerHTML = eyeOpenSvg;
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');
      const targetInput = document.getElementById(targetId);

      if (targetInput) {
        const isPassword = targetInput.type === 'password';
        targetInput.type = isPassword ? 'text' : 'password';
        btn.innerHTML = isPassword ? eyeClosedSvg : eyeOpenSvg;
      }
    });
  });

  // Client-side form validation and submit handling
  if (registerForm) {
    registerForm.addEventListener('submit', (e) => {
      const firstName = firstNameInput.value.trim();
      const lastName = lastNameInput.value.trim();
      const email = emailInput.value.trim();
      const ageVal = parseInt(ageInput.value, 10);
      const password = passwordInput.value;
      const confirmPassword = confirmPasswordInput.value;

      // 1. Campos obligatorios
      if (!firstName || !lastName || !email || !ageInput.value || !password || !confirmPassword) {
        e.preventDefault();
        showClientError('Todos los campos son obligatorios.');
        return;
      }

      // 2. Regla de Validación 1: Mayoría de edad (18 a 100 años)
      if (isNaN(ageVal) || ageVal < 18 || ageVal > 100) {
        e.preventDefault();
        showClientError('Debes tener al menos 18 años (y un máximo de 100 años) para registrarte.');
        ageInput.focus();
        return;
      }

      // 3. Regla de Validación 2: Fortaleza de contraseña (mínimo 8 caracteres, al menos 1 letra y 1 número)
      const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d).{8,}$/;
      if (!passwordRegex.test(password)) {
        e.preventDefault();
        showClientError('La contraseña debe tener al menos 8 caracteres y contener al menos una letra y un número.');
        passwordInput.focus();
        return;
      }

      // 4. Coincidencia de contraseñas
      if (password !== confirmPassword) {
        e.preventDefault();
        showClientError('Las contraseñas no coinciden. Por favor verifícalas.');
        confirmPasswordInput.focus();
        return;
      }

      // Si todo es válido, activar el estado de carga
      if (submitBtn && btnSpinner && btnText) {
        submitBtn.disabled = true;
        btnSpinner.style.display = 'inline-block';
        if (btnIcon) btnIcon.style.display = 'none';
        btnText.textContent = 'Procesando registro...';
      }
    });
  }

  // Función auxiliar para mostrar mensajes de error dinámicos
  function showClientError(message) {
    let flashContainer = document.querySelector('.flash-container');
    if (!flashContainer) {
      flashContainer = document.createElement('div');
      flashContainer.className = 'flash-container';
      const form = document.getElementById('registerForm');
      form.parentNode.insertBefore(flashContainer, form);
    }

    flashContainer.innerHTML = `
      <div class="flash-message error">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        <span>${message}</span>
      </div>
    `;

    window.scrollTo({ top: flashContainer.offsetTop - 30, behavior: 'smooth' });
  }
});
