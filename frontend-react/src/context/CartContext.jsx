import { createContext, useContext, useState, useCallback } from 'react';

const CartContext = createContext(null);

function loadCart() {
  try { return JSON.parse(localStorage.getItem('cart') || '[]'); }
  catch { return []; }
}

export function CartProvider({ children }) {
  const [cart, setCart] = useState(loadCart);

  const persist = (updated) => {
    localStorage.setItem('cart', JSON.stringify(updated));
    setCart(updated);
  };

  const addToCart     = useCallback((item) => persist([...cart, item]), [cart]);
  const removeFromCart = useCallback((idx) => persist(cart.filter((_, i) => i !== idx)), [cart]);
  const clearCart     = useCallback(() => persist([]), []);

  const total = cart.reduce((sum, i) => sum + i.price, 0);

  return (
    <CartContext.Provider value={{ cart, addToCart, removeFromCart, clearCart, total, count: cart.length }}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  return useContext(CartContext);
}
