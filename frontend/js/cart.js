// cart.js — render cart from localStorage, checkout

(function () {
  if (!requireAuth()) return;
  updateCartBadge();

  const container = document.getElementById('cart-container');
  const cart = getCart();

  if (cart.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="icon">🛒</div>
        <p>Your cart is empty.</p>
        <a href="products.html" class="btn btn-warning" style="margin-top:1rem;">Start Shopping</a>
      </div>`;
    return;
  }

  const total = cart.reduce((sum, item) => sum + item.price, 0);

  container.innerHTML = `
    <div class="product-grid">
      ${cart.map((item, i) => `
        <div class="card">
          <img class="card-img" src="images/${item.image}" alt="${item.name}" onerror="this.src='images/logo.png'">
          <div class="card-body">
            <h3 class="card-title">${item.name}</h3>
            <p class="price">₹${item.price}</p>
            <button class="btn btn-danger btn-sm btn-full" style="margin-top:0.5rem;"
              onclick="removeItem(${i})">🗑 Remove</button>
          </div>
        </div>
      `).join('')}
    </div>
    <div class="cart-summary">
      <div class="cart-total">Total: ₹${total}</div>
      <button class="btn btn-primary btn-lg" onclick="doCheckout()">Proceed to Checkout →</button>
    </div>`;

  window.removeItem = function (index) {
    removeFromCart(index);
    window.location.reload();
  };

  window.doCheckout = async function () {
    const cart  = getCart();
    const total = cart.reduce((sum, i) => sum + i.price, 0);
    try {
      const res  = await fetch(`${API_BASE}/api/checkout`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({ items: cart, total })
      });
      const data = await res.json();
      if (res.ok) {
        clearCart();
        window.location.href = `payment.html?order_id=${data.order_id}`;
      } else {
        alert(data.error || 'Checkout failed. Please try again.');
      }
    } catch (e) {
      alert('Cannot reach server. Is the backend running?');
    }
  };
})();
