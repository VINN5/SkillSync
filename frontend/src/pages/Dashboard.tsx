import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowRight, LogOut } from 'lucide-react'

interface UserPayload {
  sub: string      // user ID from JWT
  role: 'client' | 'contractor' | 'admin'
  exp: number      // expiration timestamp
}

export default function Dashboard() {
  const [user, setUser] = useState<UserPayload | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem('token')

    if (!token) {
      navigate('/login')
      return
    }

    try {
      const payloadBase64 = token.split('.')[1]
      const decodedPayload = JSON.parse(atob(payloadBase64))

      // Check if token is expired
      if (decodedPayload.exp * 1000 < Date.now()) {
        localStorage.removeItem('token')
        navigate('/login')
        return
      }

      setUser(decodedPayload)
    } catch (error) {
      localStorage.removeItem('token')
      navigate('/login')
    }
  }, [navigate])

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/')
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-2xl text-gray-600">Loading dashboard...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Dashboard Header */}
      <header className="bg-white shadow-md border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-5 flex justify-between items-center">
          <div className="flex items-center gap-6">
            <h1 className="text-4xl font-bold text-gray-900">Dashboard</h1>
            <span className="bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-semibold">
              {user.role.toUpperCase()}
            </span>
          </div>

          <button
            onClick={handleLogout}
            className="flex items-center gap-3 text-red-600 hover:text-red-700 font-semibold transition"
          >
            <LogOut className="w-6 h-6" />
            Logout
          </button>
        </div>
      </header>

      {/* Role-based Content */}
      <main className="max-w-7xl mx-auto px-6 py-12">
        {user.role === 'admin' && <AdminDashboard />}
        {user.role === 'client' && <ClientDashboard />}
        {user.role === 'contractor' && <ContractorDashboard />}
      </main>
    </div>
  )
}

// Admin Dashboard
function AdminDashboard() {
  return (
    <div>
      <h2 className="text-4xl font-bold text-gray-900 mb-10">Admin Control Center</h2>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-10">
        <div className="bg-white p-10 rounded-2xl shadow-xl hover:shadow-2xl transition">
          <h3 className="text-3xl font-bold mb-4">User Management</h3>
          <p className="text-gray-600 mb-6">View, edit, suspend, or delete users across the platform.</p>
          <button className="bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-blue-700 flex items-center gap-3">
            Manage Users <ArrowRight className="w-6 h-6" />
          </button>
        </div>

        <div className="bg-white p-10 rounded-2xl shadow-xl hover:shadow-2xl transition">
          <h3 className="text-3xl font-bold mb-4">Project Oversight</h3>
          <p className="text-gray-600 mb-6">Monitor all projects, resolve disputes, and track progress.</p>
          <button className="bg-purple-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-purple-700 flex items-center gap-3">
            View Projects <ArrowRight className="w-6 h-6" />
          </button>
        </div>

        <div className="bg-white p-10 rounded-2xl shadow-xl hover:shadow-2xl transition">
          <h3 className="text-3xl font-bold mb-4">Platform Analytics</h3>
          <p className="text-gray-600 mb-6">Growth metrics, revenue, user activity, and system health.</p>
          <button className="bg-green-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-green-700 flex items-center gap-3">
            View Analytics <ArrowRight className="w-6 h-6" />
          </button>
        </div>
      </div>
    </div>
  )
}

// Client Dashboard
function ClientDashboard() {
  return (
    <div>
      <h2 className="text-4xl font-bold text-gray-900 mb-10">Welcome back, Client!</h2>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-10">
        <div className="bg-white p-10 rounded-2xl shadow-xl hover:shadow-2xl transition">
          <h3 className="text-3xl font-bold mb-4">Post a New Project</h3>
          <p className="text-gray-600 mb-6">Get quotes from trusted contractors in minutes.</p>
          <button className="bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-blue-700 flex items-center gap-3">
            Create Project <ArrowRight className="w-6 h-6" />
          </button>
        </div>

        <div className="bg-white p-10 rounded-2xl shadow-xl hover:shadow-2xl transition">
          <h3 className="text-3xl font-bold mb-4">My Active Projects</h3>
          <p className="text-gray-600 mb-6">Track progress, communicate, and manage ongoing work.</p>
          <button className="bg-green-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-green-700 flex items-center gap-3">
            View Projects <ArrowRight className="w-6 h-6" />
          </button>
        </div>

        <div className="bg-white p-10 rounded-2xl shadow-xl hover:shadow-2xl transition">
          <h3 className="text-3xl font-bold mb-4">Hired Contractors</h3>
          <p className="text-gray-600 mb-6">View past and current contractors you've worked with.</p>
          <button className="bg-purple-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-purple-700 flex items-center gap-3">
            View History <ArrowRight className="w-6 h-6" />
          </button>
        </div>
      </div>
    </div>
  )
}

// Contractor Dashboard
function ContractorDashboard() {
  return (
    <div>
      <h2 className="text-4xl font-bold text-gray-900 mb-10">Welcome back, Contractor!</h2>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-10">
        <div className="bg-white p-10 rounded-2xl shadow-xl hover:shadow-2xl transition">
          <h3 className="text-3xl font-bold mb-4">Find New Projects</h3>
          <p className="text-gray-600 mb-6">Browse jobs that match your skills and location.</p>
          <button className="bg-green-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-green-700 flex items-center gap-3">
            Browse Jobs <ArrowRight className="w-6 h-6" />
          </button>
        </div>

        <div className="bg-white p-10 rounded-2xl shadow-xl hover:shadow-2xl transition">
          <h3 className="text-3xl font-bold mb-4">My Active Jobs</h3>
          <p className="text-gray-600 mb-6">Manage ongoing projects and client communication.</p>
          <button className="bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-blue-700 flex items-center gap-3">
            View Jobs <ArrowRight className="w-6 h-6" />
          </button>
        </div>

        <div className="bg-white p-10 rounded-2xl shadow-xl hover:shadow-2xl transition">
          <h3 className="text-3xl font-bold mb-4">Update Profile</h3>
          <p className="text-gray-600 mb-6">Keep your portfolio, rates, and certifications current.</p>
          <button className="bg-purple-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-purple-700 flex items-center gap-3">
            Edit Profile <ArrowRight className="w-6 h-6" />
          </button>
        </div>
      </div>
    </div>
  )
}