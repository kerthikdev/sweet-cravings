/**
 * Central API client.
 * Uses relative paths (/api/...) so Vite proxies to http://localhost:5050 in dev,
 * and in production you point Nginx/etc. at the real api_gateway.
 */

function getToken() {
  return localStorage.getItem('token');
}

function authHeaders() {
  const token = getToken();
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

async function request(method, path, body = null) {
  const opts = {
    method,
    headers: authHeaders(),
  };
  if (body) opts.body = JSON.stringify(body);

  const res = await fetch(path, opts);
  const data = await res.json().catch(() => ({}));
  return { ok: res.ok, status: res.status, data };
}

// ─── Auth ─────────────────────────────────────────────────────────────────────
export const apiSignup  = (u, p)  => request('POST', '/api/auth/signup',  { username: u, password: p });
export const apiLogin   = (u, p)  => request('POST', '/api/auth/login',   { username: u, password: p });

// ─── Products ─────────────────────────────────────────────────────────────────
export const apiGetProducts      = ()    => request('GET',  '/api/products');
export const apiSearchProducts   = (q)   => request('GET',  `/api/products/search?q=${encodeURIComponent(q)}`);
export const apiGetByCategory    = (cat) => request('GET',  `/api/products/category/${encodeURIComponent(cat)}`);
export const apiAddProduct       = (d)   => request('POST', '/api/products', d);
export const apiUpdateProduct    = (id, d) => request('PUT',  `/api/products/${id}`, d);
export const apiDeleteProduct    = (id)  => request('DELETE', `/api/products/${id}`);

// ─── Orders ───────────────────────────────────────────────────────────────────
export const apiCheckout     = (items, total) => request('POST', '/api/checkout', { items, total });
export const apiGetOrders    = ()             => request('GET',  '/api/orders');
export const apiGetOrder     = (id)           => request('GET',  `/api/orders/${id}`);
export const apiCancelOrder  = (id)           => request('PUT',  `/api/orders/${id}/cancel`, {});

// ─── Payment ──────────────────────────────────────────────────────────────────
export const apiConfirmPayment = (id) => request('POST', `/api/payment/confirm/${id}`, {});
export const apiFailPayment    = (id) => request('POST', `/api/payment/fail/${id}`, {});
