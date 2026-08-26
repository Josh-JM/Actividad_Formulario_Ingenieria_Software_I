document.addEventListener('DOMContentLoaded', () => {
  const registerForm = document.getElementById('registerForm');
  const submitBtn = document.getElementById('submitBtn');
  const btnSpinner = document.getElementById('btnSpinner');
  const btnText = document.getElementById('btnText');
  const passwordInput = document.getElementById('password');
  const confirmPasswordInput = document.getElementById('confirm_password');
  const togglePasswordBtns = document.querySelectorAll('.toggle-password');

  // Toggle password visibility
  togglePasswordBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');
      const targetInput = document.getElementById(targetId);

      if (targetInput) {
        const isPassword = targetInput.type === 'password';
        targetInput.type = isPassword ? 'text' : 'password';
        btn.textContent = isPassword ? '👁️' : '🔒';
      }
    });
  });

  // Client-side form validation and submit state
  if (registerForm) {
    registerForm.addEventListener('submit', (e) => {
      if (passwordInput.value !== confirmPasswordInput.value) {
        e.preventDefault();
        alert('Las contraseñas no coinciden. Por favor verifícalas.');
        confirmPasswordInput.focus();
        return;
      }

      // Show loading state
      if (submitBtn && btnSpinner && btnText) {
        submitBtn.disabled = true;
        btnSpinner.style.display = 'inline-block';
        btnText.textContent = 'Procesando registro...';
      }
    });
  }
});
