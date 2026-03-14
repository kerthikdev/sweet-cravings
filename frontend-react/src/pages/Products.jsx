import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { apiGetProducts, apiSearchProducts, apiGetByCategory } from '../api';

const CATEGORIES = ['All', 'Bread', 'Cakes', 'Pastries'];

function ProductCard({ product, onAdd }) {
  const [added, setAdded] = useState(false);

  function handleAdd() {
    onAdd(product);
    setAdded(true);
    setTimeout(() => setAdded(false), 1500);
  }

  return (
    <div className="product-card">
      <div className="product-img-wrap">
        <img
          src={`/images/${product.image}`}
          alt={product.name}
          className="product-img"
          onError={e => { e.target.src = '/images/logo.png'; }}
        />
      </div>
      <div className="product-body">
        <span className="product-category">{product.category}</span>
        <h3 className="product-name">{product.name}</h3>
        <p className="product-price">₹{product.price}</p>
        <button
          className={`btn ${added ? 'btn-success' : 'btn-primary'} btn-full`}
          onClick={handleAdd}
          disabled={added}
        >
          {added ? '✅ Added!' : '🛒 Add to Cart'}
        </button>
      </div>
    </div>
  );
}

export default function Products() {
  const [products, setProducts] = useState([]);
  const [loading,  setLoading]  = useState(true);
  const [error,    setError]    = useState('');
  const [activeTab, setActiveTab] = useState('All');
  const [search,   setSearch]   = useState('');
  const { addToCart } = useCart();
  const navigate = useNavigate();

  async function load(cat = 'All', q = '') {
    setLoading(true); setError('');
    try {
      let res;
      if (q)           res = await apiSearchProducts(q);
      else if (cat !== 'All') res = await apiGetByCategory(cat);
      else             res = await apiGetProducts();
      if (res.ok) setProducts(Array.isArray(res.data) ? res.data : []);
      else setError('Failed to load products.');
    } catch {
      setError('Cannot reach server. Is the backend running?');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  function handleSearch(e) {
    e.preventDefault();
    setActiveTab('All');
    load('All', search.trim());
  }

  function handleCategory(cat) {
    setActiveTab(cat); setSearch('');
    load(cat);
  }

  return (
    <div className="page">
      {/* Header */}
      <div className="page-header">
        <h1 className="page-title">Our Bakery</h1>
        <form onSubmit={handleSearch} className="search-form">
          <input
            className="search-input"
            placeholder="Search products…"
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
          <button className="btn btn-accent" type="submit">Search</button>
        </form>
      </div>

      {/* Category Tabs */}
      <div className="category-tabs">
        {CATEGORIES.map(cat => (
          <button
            key={cat}
            className={`tab-btn ${activeTab === cat ? 'tab-active' : ''}`}
            onClick={() => handleCategory(cat)}
          >
            {cat === 'All' ? '🧺 All' : cat === 'Bread' ? '🥖 Bread' : cat === 'Cakes' ? '🎂 Cakes' : '🥐 Pastries'}
          </button>
        ))}
      </div>

      {/* Cart shortcut */}
      <div style={{ textAlign: 'right', marginBottom: '1rem' }}>
        <button className="btn btn-outline" onClick={() => navigate('/cart')}>
          View Cart →
        </button>
      </div>

      {/* Grid */}
      {loading && <div className="spinner-center"><div className="spinner" /></div>}
      {error   && <div className="empty-state"><span>⚠️</span><p>{error}</p></div>}
      {!loading && !error && products.length === 0 && (
        <div className="empty-state"><span>🥺</span><p>No products found.</p></div>
      )}
      {!loading && !error && (
        <div className="product-grid">
          {products.map(p => (
            <ProductCard key={p._id} product={p} onAdd={addToCart} />
          ))}
        </div>
      )}
    </div>
  );
}
