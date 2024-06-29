document.getElementById('transaction-form').addEventListener('submit', function (e) {
  e.preventDefault();

  const sender = document.getElementById('sender').value;
  const recipient = document.getElementById('recipient').value;
  const product_id = document.getElementById('product_id').value;
  const product_name = document.getElementById('product_name').value;
  const status = document.getElementById('status').value;

  fetch('/transactions/new', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ sender, recipient, product_id, product_name, status }),
  })
  .then(response => response.json())
  .then(data => {
      document.getElementById('transaction-message').textContent = data.message;
      document.getElementById('transaction-form').reset();
  })
  .catch(error => console.error('Error:', error));
});

document.getElementById('mine-button').addEventListener('click', function () {
  fetch('/mine', {
      method: 'GET',
  })
  .then(response => response.json())
  .then(data => {
      document.getElementById('mine-message').textContent = data.message;
  })
  .catch(error => console.error('Error:', error));
});

document.getElementById('view-chain-button').addEventListener('click', function () {
  fetch('/chain', {
      method: 'GET',
  })
  .then(response => response.json())
  .then(data => {
      document.getElementById('blockchain-view').textContent = JSON.stringify(data, null, 2);
  })
  .catch(error => console.error('Error:', error));
});

document.getElementById('view-product-button').addEventListener('click', function () {
  const productId = document.getElementById('product-id').value;

  fetch(`/product/${productId}`, {
      method: 'GET',
  })
  .then(response => response.json())
  .then(data => {
      if (data.history) {
          document.getElementById('product-history').textContent = JSON.stringify(data.history, null, 2);
      } else {
          document.getElementById('product-history').textContent = data.message;
      }
  })
  .catch(error => console.error('Error:', error));
});

document.getElementById('authenticity-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const productId = document.getElementById('auth-product-id').value;

    fetch(`/verify-authenticity/${productId}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        if (data.is_authentic) {
            document.getElementById('authenticity-result').textContent = "Product is authentic.";
        } else {
            document.getElementById('authenticity-result').textContent = data.message;
        }
    })
    .catch(error => console.error('Error:', error));
});

