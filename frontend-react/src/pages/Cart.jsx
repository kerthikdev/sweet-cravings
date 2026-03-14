import { useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { apiCheckout } from '../api';
import { useState } from 'react';

export default function Cart() {
  const { cart, removeFromCart, clearCart, total } = useCart();
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState('');
  const navigate = useNavigate();

  async function handleCheckout() {
    setLoading(true); setError('');
    try {
      const { ok, data } = await apiCheckout(cart, total);
      if (ok) {
        clearCart();
        navigate(`/payment?order_id=${data.order_id}`);
      } else {
        setError(data.error || 'Checkout failed. Please try again.');
      }
    } catch {
      setError('Cannot reach server. Is the backend running?');
    } finally {
      setLoading(false);
    }
  }

  if (cart.length === 0) {
    return (
      <div className="page">
        <div className="empty-state large">
          <span>🛒</span>
          <h2>Your Cart is Empty</h2>
          <p>Add some delicious items from our bakery!</p>
          <button className="btn btn-primary" onClick={() => navigate('/products')} style={{ marginTop: '1rem' }}>
            Start Shopping
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">Your Cart</h1>
        <span className="badge-count">{cart.length} item{cart.length !== 1 ? 's' : ''}</span>
      </div>

      {error && <div className="alert alert-error" style={{ marginBottom: '1rem' }}>{error}</div>}

      <div className="cart-layout">
        <div className="cart-items">
          {cart.map((item, i) => (
            <div className="cart-item" key={i}>
              <img
                src={`/images/${item.image}`}
                alt={item.name}
                className="cart-item-img"
                onError={e => { e.target.src = '/images/logo.png'; }}
              />
              <div className="cart-item-info">
                <h3 className="cart-item-name">{item.name}</h3>
                <p className="cart-item-price">₹{item.price}</p>
              </div>
              <button className="btn-remove" onClick={() => removeFromCart(i)}>✕</button>
            </div>
          ))}
        </div>

        <div className="cart-summary-card">
          <h2 className="summary-title">Order Summary</h2>
          <div className="summary-row">
            <span>Subtotal ({cart.length} items)</span>
            <span>₹{total}</span>
          </div>
          <div className="summary-row summary-total">
            <span>Total</span>
            <span>₹{total}</span>
          </div>
          <button
            className="btn btn-primary btn-full btn-lg"
            onClick={handleCheckout}
            disabled={loading}
            style={{ marginTop: '1.5rem' }}
          >
            {loading ? <span className="spinner-sm" /> : 'Proceed to Checkout →'}
          </button>
        </div>
      </div>
    </div>
  );
}
