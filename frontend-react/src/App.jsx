import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { CartProvider } from './context/CartContext';
import Navbar        from './components/Navbar';
import Login         from './pages/Login';
import Signup        from './pages/Signup';
import Products      from './pages/Products';
import Cart          from './pages/Cart';
import Payment       from './pages/Payment';
import OrderSuccess  from './pages/OrderSuccess';
import Orders        from './pages/Orders';
import Admin         from './pages/Admin';

function Protected({ children }) {
  const { isLoggedIn } = useAuth();
  return isLoggedIn ? children : <Navigate to="/login" replace />;
}

function AppRoutes() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/"              element={<Navigate to="/login" replace />} />
        <Route path="/login"         element={<Login />} />
        <Route path="/signup"        element={<Signup />} />
        <Route path="/products"      element={<Protected><Products /></Protected>} />
        <Route path="/cart"          element={<Protected><Cart /></Protected>} />
        <Route path="/payment"       element={<Protected><Payment /></Protected>} />
        <Route path="/order-success" element={<Protected><OrderSuccess /></Protected>} />
        <Route path="/orders"        element={<Protected><Orders /></Protected>} />
        <Route path="/admin"         element={<Protected><Admin /></Protected>} />
        <Route path="*"              element={<Navigate to="/login" replace />} />
      </Routes>
    </>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <CartProvider>
          <AppRoutes />
        </CartProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}
