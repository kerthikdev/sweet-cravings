// orders.js — display user's order history

(function () {
  if (!requireAuth()) return;
  showUsername();
  updateCartBadge();

  const container = document.getElementById('orders-container');

  function statusBadge(status) {
    const map = { Pending: 'badge-pending', Paid: 'badge-paid', Failed: 'badge-failed', Cancelled: 'badge-cancelled' };
    return `<span class="badge ${map[status] || ''}">${status}</span>`;
  }

  async function loadOrders() {
    try {
      const res    = await fetch(`${API_BASE}/api/orders`, { headers: authHeaders() });
      const orders = await res.json();

      if (!orders || orders.length === 0) {
        container.innerHTML = `
          <div class="empty-state">
            <div class="icon">📦</div>
            <p>No orders yet.</p>
            <a href="products.html" class="btn btn-primary" style="margin-top:1rem;">Start Shopping</a>
          </div>`;
        return;
      }

      container.innerHTML = orders.reverse().map(order => `
        <div class="order-card">
          <div class="order-header">
            <span class="order-id">Order #${order.order_id}</span>
            ${statusBadge(order.status)}
          </div>
          <p style="color:var(--muted);font-size:0.85rem;">📅 ${order.timestamp}</p>
          <ul style="padding-left:1.2rem;margin:0.5rem 0;color:#555;">
            ${(order.items || []).map(i => `<li>${i.name} — ₹${i.price}</li>`).join('')}
          </ul>
          <p style="font-weight:700;color:var(--brown);">Total: ₹${order.total}</p>
          ${order.status === 'Pending' ? `
            <button class="btn btn-danger btn-sm" style="margin-top:0.5rem;"
              onclick="cancelOrder('${order.order_id}', this)">Cancel Order</button>` : ''}
        </div>
      `).join('');
    } catch (e) {
      container.innerHTML = `<div class="empty-state"><div class="icon">⚠️</div><p>Could not load orders.</p></div>`;
    }
  }

  window.cancelOrder = async function (orderId, btn) {
    if (!confirm('Cancel this order?')) return;
    btn.disabled = true;
    btn.textContent = 'Cancelling…';
    try {
      await fetch(`${API_BASE}/api/orders/${orderId}/cancel`, {
        method: 'PUT', headers: authHeaders()
      });
      loadOrders();
    } catch (e) { btn.disabled = false; btn.textContent = 'Cancel Order'; }
  };

  loadOrders();
})();
