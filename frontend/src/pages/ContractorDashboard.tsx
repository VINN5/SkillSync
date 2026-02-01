import { ArrowRight, LogOut, Search, Briefcase, User } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export default function ContractorDashboard() {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/')
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-green-50 to-emerald-50">
      {/* Header */}
      <header className="bg-white shadow-md border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-5 flex justify-between items-center">
          <div className="flex items-center gap-6">
            <h1 className="text-4xl font-bold text-gray-900">Contractor Dashboard</h1>
            <span className="bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-semibold">
              CONTRACTOR
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
        <h2 className="text-4xl font-bold text-gray-900 mb-10">Welcome back, Pro! 🛠️</h2>

        {/* Quick Stats */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white p-6 rounded-xl shadow-md">
            <p className="text-gray-500 text-sm">Active Jobs</p>
            <p className="text-3xl font-bold text-gray-900">5</p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md">
            <p className="text-gray-500 text-sm">Total Earnings</p>
            <p className="text-3xl font-bold text-gray-900">$28,340</p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md">
            <p className="text-gray-500 text-sm">Profile Views</p>
            <p className="text-3xl font-bold text-gray-900">142</p>
          </div>
        </div>

        {/* Action Cards */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-10">
          <div className="bg-white p-10 rounded-2xl shadow-xl hover:shadow-2xl transition">
            <Search className="w-12 h-12 text-green-600 mb-4" />
            <h3 className="text-3xl font-bold mb-4">Find New Projects</h3>
            <p className="text-gray-600 mb-6">Browse jobs that match your skills and location.</p>
            <button className="bg-green-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-green-700 flex items-center gap-3 w-full justify-center">
              Browse Jobs <ArrowRight className="w-6 h-6" />
            </button>
          </div>

          <div className="bg-white p-10 rounded-2xl shadow-xl hover:shadow-2xl transition">
            <Briefcase className="w-12 h-12 text-blue-600 mb-4" />
            <h3 className="text-3xl font-bold mb-4">My Active Jobs</h3>
            <p className="text-gray-600 mb-6">Manage ongoing projects and client communication.</p>
            <button className="bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-blue-700 flex items-center gap-3 w-full justify-center">
              View Jobs <ArrowRight className="w-6 h-6" />
            </button>
          </div>

          <div className="bg-white p-10 rounded-2xl shadow-xl hover:shadow-2xl transition">
            <User className="w-12 h-12 text-purple-600 mb-4" />
            <h3 className="text-3xl font-bold mb-4">Update Profile</h3>
            <p className="text-gray-600 mb-6">Keep your portfolio, rates, and certifications current.</p>
            <button className="bg-purple-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-purple-700 flex items-center gap-3 w-full justify-center">
              Edit Profile <ArrowRight className="w-6 h-6" />
            </button>
          </div>
        </div>
      </main>
    </div>
  )
}
