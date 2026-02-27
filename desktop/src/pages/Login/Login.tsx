import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const endpoint = isLogin ? '/auth/login' : '/auth/signup';
      const body = isLogin ? { username, password } : { username, password, email };

      const response = await fetch(`http://localhost:8001${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      const data = await response.json();

      if (data.success) {
        if (isLogin) {
          localStorage.setItem('token', data.token);
          localStorage.setItem('username', data.username);
          navigate('/');
        } else {
          setIsLogin(true);
          setError('Account created! Please login.');
        }
      } else {
        setError(data.error || 'Failed');
      }
    } catch {
      setError('Connection error');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <h1 className="text-2xl font-bold mb-6 text-center">🔒 CortexDesk</h1>
        
        <div className="flex gap-2 mb-6">
          <button onClick={() => setIsLogin(true)} className={`flex-1 py-2 rounded ${isLogin ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}>Login</button>
          <button onClick={() => setIsLogin(false)} className={`flex-1 py-2 rounded ${!isLogin ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}>Sign Up</button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Username</label>
            <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} className="w-full px-3 py-2 border rounded" required />
          </div>

          {!isLogin && (
            <div>
              <label className="block text-sm font-medium mb-1">Email</label>
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="w-full px-3 py-2 border rounded" required />
            </div>
          )}

          <div>
            <label className="block text-sm font-medium mb-1">Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full px-3 py-2 border rounded" required />
          </div>

          {error && <div className={`text-sm p-2 rounded ${error.includes('created') ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>{error}</div>}

          <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">{isLogin ? 'Login' : 'Sign Up'}</button>
        </form>

        <p className="text-xs text-gray-500 mt-4 text-center">100% Local • Privacy-First</p>
      </div>
    </div>
  );
}

export default Login;
