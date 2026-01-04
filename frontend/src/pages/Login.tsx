import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

export default function Login() {
  const [formData, setFormData] = useState({ email: '', password: '' })
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          username: formData.email,
          password: formData.password
        })
      })

      const data = await res.json()

      if (res.ok) {
        localStorage.setItem('token', data.access_token)
        setMessage('Welcome back!')
        setTimeout(() => navigate('/dashboard'), 1500)  // ← Changed to /dashboard
      } else {
        setMessage(data.detail || 'Invalid credentials')
      }
    } catch (err) {
      setMessage('Network error — is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-blue-900 via-indigo-800 to-purple-900 flex items-center justify-center py-12 px-4 relative">
      {/* Back to Home Button */}
      <Link
        to="/"
        className="absolute top-8 left-8 bg-white/20 backdrop-blur-md text-white px-6 py-3 rounded-full font-medium hover:bg-white/30 transition flex items-center gap-2 shadow-lg"
      >
        ← Back to Home
      </Link>

      <div className="max-w-md w-full bg-white/10 backdrop-blur-xl rounded-3xl shadow-2xl p-10 border border-white/20">
        <h2 className="text-4xl font-bold text-white text-center mb-10">Welcome Back</h2>

        <form onSubmit={handleSubmit} className="space-y-6">
          <input
            type="email"
            placeholder="Email"
            required
            className="w-full px-6 py-4 bg-white/20 border border-white/30 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-4 focus:ring-white/50"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          />

          <input
            type="password"
            placeholder="Password"
            required
            className="w-full px-6 py-4 bg-white/20 border border-white/30 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-4 focus:ring-white/50"
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-linear-to-r from-blue-600 to-indigo-600 text-white py-5 rounded-xl text-xl font-bold hover:from-blue-700 hover:to-indigo-700 transition shadow-xl disabled:opacity-70"
          >
            {loading ? 'Logging in...' : 'Log In'}
          </button>
        </form>

        {message && (
          <p className={`mt-8 text-center text-xl font-medium ${message.includes('Welcome') ? 'text-green-300' : 'text-red-300'}`}>
            {message}
          </p>
        )}

        <p className="mt-10 text-center text-white/80">
          New to SkillSync?{' '}
          <Link to="/register" className="text-white font-bold underline hover:opacity-80">
            Create Account
          </Link>
        </p>
      </div>
    </div>
  )
}