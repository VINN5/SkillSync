import { ArrowRight, LogOut, Users, FolderKanban, BarChart3 } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export default function AdminDashboard() {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/')
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white shadow-md border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-5 flex justify-between items-center">
          <div className="flex items-center gap-6">
            <h1 className="text-4xl font-bold text-gray-900">Admin Control Center</h1>
            <span className="bg-red-100 text-red-800 px-4 py-2 rounded-full text-sm font-semibold">
              ADMIN
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

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-12">
        {/* Stats Overview */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white p-6 rounded-xl shadow-md">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Total Users</p>
                <p className="text-3xl font-bold text-gray-900">1,247</p>
              </div>
              <Users className="w-12 h-12 text-blue-500" />
            </div>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Active Projects</p>
                <p className="text-3xl font-bold text-gray-900">342</p>
              </div>
              <FolderKanban className="w-12 h-12 text-purple-500" />
            </div>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Revenue (Monthly)</p>
                <p className="text-3xl font-bold text-gray-900">$45.2K</p>
              </div>
              <BarChart3 className="w-12 h-12 text-green-500" />
            </div>
          </div>
        </div>

        {/* Action Cards */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-10">
          <div className="bg-white p-10 rounded-2xl shadow-xl hover:shadow-2xl transition">
            <Users className="w-12 h-12 text-blue-600 mb-4" />
            <h3 className="text-3xl font-bold mb-4">User Management</h3>
            <p className="text-gray-600 mb-6">View, edit, suspend, or delete users across the platform.</p>
            <button className="bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-blue-700 flex items-center gap-3 w-full justify-center">
              Manage Users <ArrowRight className="w-6 h-6" />
            </button>
          </div>

          <div className="bg-white p-10 rounded-2xl shadow-xl hover:shadow-2xl transition">
            <FolderKanban className="w-12 h-12 text-purple-600 mb-4" />
            <h3 className="text-3xl font-bold mb-4">Project Oversight</h3>
            <p className="text-gray-600 mb-6">Monitor all projects, resolve disputes, and track progress.</p>
            <button className="bg-purple-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-purple-700 flex items-center gap-3 w-full justify-center">
              View Projects <ArrowRight className="w-6 h-6" />
            </button>
          </div>

          <div className="bg-white p-10 rounded-2xl shadow-xl hover:shadow-2xl transition">
            <BarChart3 className="w-12 h-12 text-green-600 mb-4" />
            <h3 className="text-3xl font-bold mb-4">Platform Analytics</h3>
            <p className="text-gray-600 mb-6">Growth metrics, revenue, user activity, and system health.</p>
            <button className="bg-green-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-green-700 flex items-center gap-3 w-full justify-center">
              View Analytics <ArrowRight className="w-6 h-6" />
            </button>
          </div>
        </div>
      </main>
    </div>
  )
}
