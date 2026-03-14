// products.js — product listing, category filter, search, add-to-cart

(function () {
  if (!requireAuth()) return;
  updateCartBadge();

  const grid = document.getElementById('product-grid');

  // ------- Render products -------
  function renderProducts(list) {
    if (!list || list.length === 0) {
      grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1;"><div class="icon">🥺</div><p>No products found.</p></div>`;
      return;
    }
    grid.innerHTML = list.map(p => `
      <div class="card">
        <img class="card-img" src="images/${p.image}" alt="${p.name}" onerror="this.src='images/logo.png'">
        <div class="card-body">
          <h3 class="card-title">${p.name}</h3>
          <p class="price">₹${p.price}</p>
          <span style="font-size:0.78rem;color:var(--muted);">${p.category}</span>
          <div style="margin-top:0.8rem;">
            <button class="btn btn-primary btn-full" onclick="addToCartAction('${p._id}', '${p.name}', ${p.price}, '${p.image}')">🛒 Add to Cart</button>
          </div>
        </div>
      </div>
    `).join('');
  }

  // ------- Fetch all products -------
  async function loadProducts(url) {
    grid.innerHTML = '<div class="spinner" style="grid-column:1/-1;"></div>';
    try {
      const res  = await fetch(url, { headers: authHeaders() });
      const data = await res.json();
      renderProducts(data);
    } catch (e) {
      grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1;"><div class="icon">⚠️</div><p>Could not load products.</p></div>`;
    }
  }

  // ------- Initial load -------
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('q')) {
    loadProducts(`${API_BASE}/api/products/search?q=${encodeURIComponent(urlParams.get('q'))}`);
  } else if (urlParams.get('cat')) {
    loadProducts(`${API_BASE}/api/products/category/${urlParams.get('cat')}`);
  } else {
    loadProducts(`${API_BASE}/api/products`);
  }

  // ------- Category filter -------
  window.loadCategory = function (cat) {
    window.location.href = `products.html?cat=${encodeURIComponent(cat)}`;
  };

  // ------- Search -------
  window.doSearch = function (e) {
    e.preventDefault();
    const q = document.getElementById('search-input').value.trim();
    if (q) window.location.href = `products.html?q=${encodeURIComponent(q)}`;
    return false;
  };

  // ------- Add to cart -------
  window.addToCartAction = function (id, name, price, image) {
    addToCart({ _id: id, name, price, image });
    updateCartBadge();
    // Flash feedback
    const btn = event.target;
    btn.textContent = '✅ Added!';
    btn.disabled = true;
    setTimeout(() => { btn.textContent = '🛒 Add to Cart'; btn.disabled = false; }, 1200);
  };
})();
