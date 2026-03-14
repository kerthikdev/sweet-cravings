import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';

export default function Navbar() {
  const { isLoggedIn, username, logout } = useAuth();
  const { count } = useCart();
  const navigate   = useNavigate();
  const location   = useLocation();

  const handleLogout = () => { logout(); navigate('/login'); };

  const isActive = (path) => location.pathname === path ? 'nav-link active' : 'nav-link';

  if (!isLoggedIn) return null;

  return (
    <nav className="navbar">
      <div className="nav-brand">
        <span className="nav-logo">🍰</span>
        <span className="nav-title">Sweet Cravings</span>
      </div>

      <div className="nav-links">
        <Link to="/products" className={isActive('/products')}>Shop</Link>
        <Link to="/orders"   className={isActive('/orders')}>Orders</Link>
        <Link to="/admin"    className={isActive('/admin')}>Admin</Link>
      </div>

      <div className="nav-right">
        <Link to="/cart" className="cart-btn">
          🛒
          {count > 0 && <span className="cart-badge">{count}</span>}
        </Link>
        <span className="nav-user">👤 {username}</span>
        <button className="btn-logout" onClick={handleLogout}>Logout</button>
      </div>
    </nav>
  );
}
