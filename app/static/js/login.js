// Login form validation
document.getElementById('loginBtn').addEventListener('click', function() {
  const email = document.getElementById('loginEmail').value.trim();
  const password = document.getElementById('loginPassword').value.trim();
  const errorMsg = document.getElementById('errorMsg');

  // Reset error
  errorMsg.classList.remove('show');
  errorMsg.textContent = '';

  // Validate email
  if (!email) {
    errorMsg.textContent = 'Please enter your email address.';
    errorMsg.classList.add('show');
    return;
  }

  // Validate email format
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    errorMsg.textContent = 'Please enter a valid email address.';
    errorMsg.classList.add('show');
    return;
  }

  // Validate password
  if (!password) {
    errorMsg.textContent = 'Please enter your password.';
    errorMsg.classList.add('show');
    return;
  }

 
  console.log('Login submitted:', email);

});