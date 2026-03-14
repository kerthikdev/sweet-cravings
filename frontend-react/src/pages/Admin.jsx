import { useState, useEffect, useCallback } from 'react';
import { apiGetProducts, apiAddProduct, apiUpdateProduct, apiDeleteProduct } from '../api';

const CATEGORIES = ['Bread', 'Cakes', 'Pastries'];

export default function Admin() {
  const [products, setProducts] = useState([]);
  const [loading,  setLoading]  = useState(true);
  const [error,    setError]    = useState('');
  const [success,  setSuccess]  = useState('');

  // New product form
  const [form, setForm] = useState({ name: '', price: '', image: '', category: 'Bread' });

  // Inline price editing state: { [productId]: newPrice }
  const [prices, setPrices] = useState({});

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const { ok, data } = await apiGetProducts();
      if (ok) setProducts(Array.isArray(data) ? data : []);
      else setError('Failed to load products.');
    } catch {
      setError('Cannot reach server.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  function flash(msg) { setSuccess(msg); setTimeout(() => setSuccess(''), 2500); }

  async function handleAdd(e) {
    e.preventDefault();
    if (!form.name || !form.price || !form.image) { setError('Fill all fields.'); return; }
    setError('');
    const { ok } = await apiAddProduct({ ...form, price: parseInt(form.price) });
    if (ok) { flash('Product added!'); setForm({ name: '', price: '', image: '', category: 'Bread' }); load(); }
    else setError('Failed to add product.');
  }

  async function handleUpdatePrice(id) {
    const price = parseInt(prices[id]);
    if (!price) return;
    const { ok } = await apiUpdateProduct(id, { price });
    if (ok) { flash('Price updated!'); load(); }
    else setError('Failed to update price.');
  }

  async function handleDelete(id) {
    if (!confirm('Delete this product?')) return;
    const { ok } = await apiDeleteProduct(id);
    if (ok) { flash('Product deleted.'); load(); }
    else setError('Failed to delete.');
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">⚙️ Admin Panel</h1>
      </div>

      {error   && <div className="alert alert-error"   style={{ marginBottom: '1rem' }}>{error}</div>}
      {success && <div className="alert alert-success" style={{ marginBottom: '1rem' }}>{success}</div>}

      {/* Add Product Form */}
      <div className="admin-card">
        <h2 className="admin-section-title">Add New Product</h2>
        <form onSubmit={handleAdd} className="admin-form">
          <input className="form-input" placeholder="Product name"
            value={form.name} onChange={e => setForm(f => ({ ...f, name: e.target.value }))} required />
          <input className="form-input" type="number" placeholder="Price (₹)"
            value={form.price} onChange={e => setForm(f => ({ ...f, price: e.target.value }))} required />
          <input className="form-input" placeholder="Image filename (e.g. croissant.jpg)"
            value={form.image} onChange={e => setForm(f => ({ ...f, image: e.target.value }))} required />
          <select className="form-input" value={form.category}
            onChange={e => setForm(f => ({ ...f, category: e.target.value }))}>
            {CATEGORIES.map(c => <option key={c}>{c}</option>)}
          </select>
          <button className="btn btn-primary" type="submit">Add Product</button>
        </form>
      </div>

      {/* Products Table */}
      <div className="admin-card" style={{ marginTop: '2rem' }}>
        <h2 className="admin-section-title">All Products ({products.length})</h2>

        {loading && <div className="spinner-center"><div className="spinner" /></div>}

        {!loading && (
          <div className="admin-table-wrap">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Category</th>
                  <th>Price (₹)</th>
                  <th>Image</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {products.map(p => (
                  <tr key={p._id}>
                    <td>{p.name}</td>
                    <td><span className="product-category">{p.category}</span></td>
                    <td>
                      <input
                        className="price-input"
                        type="number"
                        defaultValue={p.price}
                        onChange={e => setPrices(prev => ({ ...prev, [p._id]: e.target.value }))}
                      />
                    </td>
                    <td>
                      <img src={`/images/${p.image}`} alt={p.name} className="admin-thumb"
                        onError={e => { e.target.style.display = 'none'; }} />
                    </td>
                    <td className="action-cell">
                      <button className="btn btn-warning btn-sm" onClick={() => handleUpdatePrice(p._id)}>Save</button>
                      <button className="btn btn-danger btn-sm"  onClick={() => handleDelete(p._id)}>Delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
