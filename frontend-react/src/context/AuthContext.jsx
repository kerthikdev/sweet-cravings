import { createContext, useContext, useState, useCallback } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token,    setToken]    = useState(() => localStorage.getItem('token') || null);
  const [username, setUsername] = useState(() => localStorage.getItem('username') || null);

  const login = useCallback((tkn, uname) => {
    localStorage.setItem('token',    tkn);
    localStorage.setItem('username', uname);
    setToken(tkn);
    setUsername(uname);
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    localStorage.removeItem('cart');
    setToken(null);
    setUsername(null);
  }, []);

  const ADMIN_USER = 'admin';

  return (
    <AuthContext.Provider value={{ token, username, login, logout, isLoggedIn: !!token, isAdmin: username === ADMIN_USER }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
