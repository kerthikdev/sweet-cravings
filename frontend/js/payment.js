// payment.js — load order details, confirm or fail payment

(function () {
  if (!requireAuth()) return;

  const orderId   = new URLSearchParams(window.location.search).get('order_id');
  const container = document.getElementById('payment-container');

  if (!orderId) {
    container.innerHTML = `<div class="empty-state"><div class="icon">⚠️</div><p>No order ID specified.</p></div>`;
    return;
  }

  function statusBadge(status) {
    const map = { Pending: 'badge-pending', Paid: 'badge-paid', Failed: 'badge-failed', Cancelled: 'badge-cancelled' };
    return `<span class="badge ${map[status] || ''}">${status}</span>`;
  }

  async function loadOrder() {
    try {
      const res   = await fetch(`${API_BASE}/api/orders/${orderId}`, { headers: authHeaders() });
      const order = await res.json();
      if (!res.ok) { container.innerHTML = `<div class="empty-state"><p>Order not found.</p></div>`; return; }
      renderOrder(order);
    } catch (e) {
      container.innerHTML = `<div class="empty-state"><p>Cannot load order.</p></div>`;
    }
  }

  function renderOrder(order) {
    const items = (order.items || []).map(item =>
      `<div class="payment-item"><span>${item.name}</span><span>₹${item.price}</span></div>`
    ).join('');

    const actionBtns = order.status === 'Pending' ? `
      <div class="payment-actions">
        <button class="btn btn-success btn-lg" onclick="confirmPay()">✅ Confirm Payment</button>
        <button class="btn btn-danger btn-lg" onclick="failPay()">❌ Simulate Failure</button>
      </div>` : '';

    container.innerHTML = `
      <div class="card payment-card">
        <h3 style="margin-bottom:1rem;color:var(--brown);">Order #${order.order_id}</h3>
        ${items}
        <div class="payment-total">
          <span>Total</span><span style="color:var(--success);">₹${order.total}</span>
        </div>
        <div style="margin-top:1rem;text-align:center;">Status: ${statusBadge(order.status)}</div>
        ${actionBtns}
      </div>`;
  }

  window.confirmPay = async function () {
    try {
      const res  = await fetch(`${API_BASE}/api/payment/confirm/${orderId}`, {
        method: 'POST', headers: authHeaders()
      });
      const data = await res.json();
      if (res.ok) {
        window.location.href = `order_success.html?order_id=${data.order_id}&total=${data.total}&timestamp=${encodeURIComponent(data.timestamp)}`;
      } else {
        alert(data.error || 'Payment failed.');
      }
    } catch (e) { alert('Server error.'); }
  };

  window.failPay = async function () {
    await fetch(`${API_BASE}/api/payment/fail/${orderId}`, { method: 'POST', headers: authHeaders() });
    window.location.href = `orders.html`;
  };

  loadOrder();
})();
