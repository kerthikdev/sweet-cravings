import { useSearchParams, useNavigate } from 'react-router-dom';

export default function OrderSuccess() {
  const [params] = useSearchParams();
  const orderId   = params.get('order_id');
  const total     = params.get('total');
  const timestamp = params.get('timestamp');
  const navigate  = useNavigate();

  return (
    <div className="page page-narrow">
      <div className="success-card">
        <div className="success-icon">🎉</div>
        <h1 className="success-title">Order Confirmed!</h1>
        <p className="success-subtitle">Thank you for your purchase. Your baked goods are on their way!</p>

        <div className="success-details">
          {orderId   && <div className="detail-row"><span>Order ID</span><strong>#{orderId}</strong></div>}
          {total     && <div className="detail-row"><span>Total Paid</span><strong>₹{total}</strong></div>}
          {timestamp && <div className="detail-row"><span>Time</span><strong>{decodeURIComponent(timestamp)}</strong></div>}
        </div>

        <div className="success-actions">
          <button className="btn btn-primary" onClick={() => navigate('/orders')}>
            View My Orders
          </button>
          <button className="btn btn-outline" onClick={() => navigate('/products')}>
            Continue Shopping
          </button>
        </div>
      </div>
    </div>
  );
}
