// ─── Auth Utilities ───────────────────────────────────────────────────────────

function getToken()    { return localStorage.getItem('token'); }
function getUsername() { return localStorage.getItem('username'); }

function authHeaders() {
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getToken()}`
    };
}

/** Redirect to login if no token present */
function requireAuth() {
    if (!getToken()) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

/** Display logged-in username wherever #logged-in-user exists */
function showUsername() {
    const el = document.getElementById('logged-in-user');
    if (el) el.textContent = getUsername() || 'User';
}

/** Update cart badge count from localStorage */
function updateCartBadge() {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    document.querySelectorAll('.cart-count').forEach(el => {
        el.textContent = cart.length;
    });
}

/** Logout */
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    localStorage.removeItem('cart');
    window.location.href = 'login.html';
}

// ─── Cart helpers (localStorage) ─────────────────────────────────────────────
function getCart()           { return JSON.parse(localStorage.getItem('cart') || '[]'); }
function saveCart(cart)      { localStorage.setItem('cart', JSON.stringify(cart)); }
function clearCart()         { localStorage.removeItem('cart'); }

function addToCart(product) {
    const cart = getCart();
    cart.push(product);
    saveCart(cart);
    updateCartBadge();
}

function removeFromCart(index) {
    const cart = getCart();
    cart.splice(index, 1);
    saveCart(cart);
}
