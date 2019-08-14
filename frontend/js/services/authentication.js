function login(username, password) {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  };

  return fetch(`/api/authenticate`, requestOptions)
    .then(response => {
      response.text().then(text => {
        if (response.ok) {
          console.log("123")
          localStorage.setItem('user', window.btoa(username + ':' + password));
        } else {
          console.log("321")
          localStorage.removeItem('user');
        }
      })
    });
}

function isAuthenticated() {
  return !!localStorage['user'];
}

export const authenticationService = {
  login,
  isAuthenticated
};
