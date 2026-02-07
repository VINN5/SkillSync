import { useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'

export default function Register() {
  const [searchParams] = useSearchParams()
  const initialRole = searchParams.get('role') as 'client' | 'contractor' || 'client'

  const [formData, setFormData] = useState({
    name: '',        // ← Changed from full_name to name
    email: '',
    password: '',
    role: initialRole
  })
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      const data = await res.json()

      if (res.ok) {
        // Store the token and redirect to dashboard immediately
        localStorage.setItem('token', data.access_token)
        setMessage(`Success! Welcome, ${formData.name}. Redirecting...`)
        setTimeout(() => navigate('/dashboard'), 1500)
      } else {
        setMessage(data.detail || 'Registration failed')
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

      <div className="max-w-lg w-full bg-white/10 backdrop-blur-xl rounded-3xl shadow-2xl p-10 border border-white/20">
        <h2 className="text-4xl font-bold text-white text-center mb-2">Create Account</h2>
        <p className="text-center text-white/80 mb-10">Join SkillSync — fast, secure, professional</p>

        <form onSubmit={handleSubmit} className="space-y-6">
          <input
            type="text"
            placeholder="Full Name"
            required
            className="w-full px-6 py-4 bg-white/20 border border-white/30 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-4 focus:ring-white/50"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          />

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

          <div className="grid grid-cols-2 gap-4">
            <button
              type="button"
              onClick={() => setFormData({ ...formData, role: 'client' })}
              className={`py-4 rounded-xl font-bold text-lg transition ${
                formData.role === 'client'
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'bg-white/20 text-white hover:bg-white/30'
              }`}
            >
              Client
            </button>
            <button
              type="button"
              onClick={() => setFormData({ ...formData, role: 'contractor' })}
              className={`py-4 rounded-xl font-bold text-lg transition ${
                formData.role === 'contractor'
                  ? 'bg-green-600 text-white shadow-lg'
                  : 'bg-white/20 text-white hover:bg-white/30'
              }`}
            >
              Contractor
            </button>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-linear-to-r from-blue-600 to-indigo-600 text-white py-5 rounded-xl text-xl font-bold hover:from-blue-700 hover:to-indigo-700 transition shadow-xl disabled:opacity-70"
          >
            {loading ? 'Creating Account...' : 'Sign Up'}
          </button>
        </form>

        {message && (
          <p className={`mt-8 text-center text-xl font-medium ${message.includes('Success') ? 'text-green-300' : 'text-red-300'}`}>
            {message}
          </p>
        )}

        <p className="mt-10 text-center text-white/80">
          Already have an account?{' '}
          <Link to="/login" className="text-white font-bold underline hover:opacity-80">
            Log In
          </Link>
        </p>
      </div>
    </div>
  )
}