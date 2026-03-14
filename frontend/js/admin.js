// admin.js — product management (add, update price, delete)

(function () {
  if (!requireAuth()) return;

  const tbody = document.getElementById('product-table-body');

  async function loadProducts() {
    try {
      const res  = await fetch(`${API_BASE}/api/products`, { headers: authHeaders() });
      const list = await res.json();
      renderTable(list);
    } catch (e) {
      tbody.innerHTML = `<tr><td colspan="5" class="empty-state">Could not load products.</td></tr>`;
    }
  }

  function renderTable(list) {
    if (!list.length) {
      tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;padding:2rem;color:var(--muted);">No products yet.</td></tr>`;
      return;
    }
    tbody.innerHTML = list.map(p => `
      <tr>
        <td>${p.name}</td>
        <td>${p.category}</td>
        <td>
          <input type="number" value="${p.price}" id="price-${p._id}"
            style="width:80px;padding:4px 8px;border:1px solid #ddd;border-radius:6px;">
        </td>
        <td><img src="images/${p.image}" style="height:40px;border-radius:6px;" onerror="this.style.display='none'"></td>
        <td style="display:flex;gap:6px;flex-wrap:wrap;">
          <button class="btn btn-warning btn-sm" onclick="updatePrice('${p._id}')">Save</button>
          <button class="btn btn-danger btn-sm"  onclick="deleteProduct('${p._id}')">Delete</button>
        </td>
      </tr>
    `).join('');
  }

  window.addProduct = async function () {
    const name     = document.getElementById('new-name').value.trim();
    const price    = parseInt(document.getElementById('new-price').value);
    const image    = document.getElementById('new-image').value.trim();
    const category = document.getElementById('new-category').value;

    if (!name || !price || !image) { alert('Please fill in all fields.'); return; }

    await fetch(`${API_BASE}/api/products`, {
      method: 'POST',
      headers: authHeaders(),
      body: JSON.stringify({ name, price, image, category })
    });
    document.getElementById('new-name').value  = '';
    document.getElementById('new-price').value = '';
    document.getElementById('new-image').value = '';
    loadProducts();
  };

  window.updatePrice = async function (id) {
    const price = parseInt(document.getElementById(`price-${id}`).value);
    await fetch(`${API_BASE}/api/products/${id}`, {
      method: 'PUT',
      headers: authHeaders(),
      body: JSON.stringify({ price })
    });
    loadProducts();
  };

  window.deleteProduct = async function (id) {
    if (!confirm('Delete this product?')) return;
    await fetch(`${API_BASE}/api/products/${id}`, { method: 'DELETE', headers: authHeaders() });
    loadProducts();
  };

  loadProducts();
})();
