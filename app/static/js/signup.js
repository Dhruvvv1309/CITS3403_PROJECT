// Signup form validation
document.getElementById('signupBtn').addEventListener('click', function() {
  const username = document.getElementById('signupUsername').value.trim();
  const email = document.getElementById('signupEmail').value.trim();
  const password = document.getElementById('signupPassword').value.trim();
  const confirm = document.getElementById('signupConfirm').value.trim();
  const errorMsg = document.getElementById('errorMsg');

  // Reset error
  errorMsg.classList.remove('show');
  errorMsg.textContent = '';

  // Validate username
  if (!username) {
    errorMsg.textContent = 'Please enter a username.';
    errorMsg.classList.add('show');
    return;
  }

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
    errorMsg.textContent = 'Please enter a password.';
    errorMsg.classList.add('show');
    return;
  }

  // Validate password length
  if (password.length < 8) {
    errorMsg.textContent = 'Password must be at least 8 characters.';
    errorMsg.classList.add('show');
    return;
  }

  // Validate confirm password
  if (password !== confirm) {
    errorMsg.textContent = 'Passwords do not match.';
    errorMsg.classList.add('show');
    return;
  }

  // All valid — TODO: replace with Flask POST request when backend is ready
  // fetch('/signup', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ username, email, password })
  // });
  console.log('Signup submitted:', username, email);

});