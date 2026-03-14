import { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { apiGetOrder, apiConfirmPayment, apiFailPayment } from '../api';

const STATUS_CLASS = {
  Pending:   'badge-pending',
  Paid:      'badge-paid',
  Failed:    'badge-failed',
  Cancelled: 'badge-cancelled',
};

export default function Payment() {
  const [params]            = useSearchParams();
  const orderId             = params.get('order_id');
  const [order,   setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [paying,  setPaying]  = useState(false);
  const [error,   setError]   = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    if (!orderId) { setLoading(false); return; }
    apiGetOrder(orderId).then(({ ok, data }) => {
      if (ok) setOrder(data);
      else    setError('Order not found.');
    }).catch(() => setError('Cannot load order.')).finally(() => setLoading(false));
  }, [orderId]);

  async function handleConfirm() {
    setPaying(true); setError('');
    try {
      const { ok, data } = await apiConfirmPayment(orderId);
      if (ok) {
        navigate(`/order-success?order_id=${data.order_id}&total=${data.total}&timestamp=${encodeURIComponent(data.timestamp)}`);
      } else {
        setError(data.error || 'Payment failed.');
      }
    } catch {
      setError('Server error. Please try again.');
    } finally {
      setPaying(false);
    }
  }

  async function handleFail() {
    await apiFailPayment(orderId);
    navigate('/orders');
  }

  if (loading) return <div className="spinner-center"><div className="spinner" /></div>;
  if (!orderId || error) return <div className="page"><div className="empty-state"><span>⚠️</span><p>{error || 'No order specified.'}</p></div></div>;

  return (
    <div className="page page-narrow">
      <h1 className="page-title" style={{ textAlign: 'center', marginBottom: '2rem' }}>💳 Payment</h1>

      <div className="payment-card">
        <div className="payment-header">
          <span className="order-id-label">Order #{order?.order_id}</span>
          <span className={`badge ${STATUS_CLASS[order?.status]}`}>{order?.status}</span>
        </div>

        <div className="payment-items">
          {(order?.items || []).map((item, i) => (
            <div className="payment-item" key={i}>
              <span>{item.name}</span>
              <span className="item-price">₹{item.price}</span>
            </div>
          ))}
        </div>

        <div className="payment-total">
          <span>Total</span>
          <span className="total-amount">₹{order?.total}</span>
        </div>

        {error && <div className="alert alert-error" style={{ marginTop: '1rem' }}>{error}</div>}

        {order?.status === 'Pending' && (
          <div className="payment-actions">
            <button className="btn btn-success btn-lg" onClick={handleConfirm} disabled={paying}>
              {paying ? <span className="spinner-sm" /> : '✅ Confirm Payment'}
            </button>
            <button className="btn btn-danger btn-lg" onClick={handleFail}>
              ❌ Simulate Failure
            </button>
          </div>
        )}

        {order?.status !== 'Pending' && (
          <button className="btn btn-outline btn-full" style={{ marginTop: '1.5rem' }}
            onClick={() => navigate('/orders')}>
            View All Orders
          </button>
        )}
      </div>
    </div>
  );
}
