function getAll(params) {
  const requestOptions = {
    method: 'GET',
    headers: {
      'Authorization': `Basic ${localStorage['user']}`
    },

  };

  return fetch(`/api/donations${params}`, requestOptions)
    .then(response => {
      return response.json();
    });
}

function update(params) {
  const requestOptions = {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${localStorage['user']}`
    },
    body: params
  };

  return fetch(`/api/donations`, requestOptions)
    .then(response => {
      return response.json();
    });
}

function destroy(params) {
  const requestOptions = {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${localStorage['user']}`
    },
    body: params
  };

  return fetch(`/api/donations/delete`, requestOptions)
    .then(response => {
      return response.json();
    });
}

export const donationsService = {
  getAll,
  update,
  destroy
};
