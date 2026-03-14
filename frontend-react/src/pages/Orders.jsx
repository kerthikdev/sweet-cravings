import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiGetOrders, apiCancelOrder } from '../api';

const STATUS_CLASS = {
  Pending:   'badge-pending',
  Paid:      'badge-paid',
  Failed:    'badge-failed',
  Cancelled: 'badge-cancelled',
};

export default function Orders() {
  const [orders,  setOrders]  = useState([]);
  const [loading, setLoading] = useState(true);
  const [error,   setError]   = useState('');
  const navigate = useNavigate();

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const { ok, data } = await apiGetOrders();
      if (ok) setOrders([...data].reverse());
      else    setError('Failed to load orders.');
    } catch {
      setError('Cannot reach server.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  async function handleCancel(orderId) {
    if (!confirm('Cancel this order?')) return;
    await apiCancelOrder(orderId);
    load();
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">My Orders</h1>
      </div>

      {loading && <div className="spinner-center"><div className="spinner" /></div>}
      {error   && <div className="alert alert-error">{error}</div>}

      {!loading && orders.length === 0 && (
        <div className="empty-state large">
          <span>📦</span>
          <h2>No Orders Yet</h2>
          <p>Start shopping and your orders will appear here.</p>
          <button className="btn btn-primary" style={{ marginTop: '1rem' }} onClick={() => navigate('/products')}>
            Shop Now
          </button>
        </div>
      )}

      <div className="orders-list">
        {orders.map(order => (
          <div className="order-card" key={order._id || order.order_id}>
            <div className="order-card-header">
              <span className="order-card-id">Order #{order.order_id}</span>
              <span className={`badge ${STATUS_CLASS[order.status] || ''}`}>{order.status}</span>
            </div>
            <p className="order-timestamp">📅 {order.timestamp}</p>
            <ul className="order-items">
              {(order.items || []).map((item, i) => (
                <li key={i}>{item.name} — <span className="item-price">₹{item.price}</span></li>
              ))}
            </ul>
            <div className="order-card-footer">
              <strong className="order-total">Total: ₹{order.total}</strong>
              {order.status === 'Pending' && (
                <button className="btn btn-danger btn-sm" onClick={() => handleCancel(order.order_id)}>
                  Cancel
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
