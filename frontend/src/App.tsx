import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import Register from './pages/Register'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'  // ← Added

function App() {
  return (
    <Router>
      {/* Global Header */}
      <header className="bg-linear-to-r from-blue-700 to-indigo-800 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-6 py-5 flex justify-between items-center">
          <Link to="/" className="text-3xl font-black tracking-tight">
            SkillSync
          </Link>
          <div className="flex items-center gap-6">
            <Link to="/login" className="text-lg font-medium hover:opacity-80 transition">
              Log In
            </Link>
            <Link
              to="/register"
              className="bg-white text-blue-700 px-8 py-3 rounded-full text-lg font-bold hover:bg-gray-100 transition shadow-md"
            >
              Sign Up
            </Link>
          </div>
        </div>
      </header>

      {/* Routes */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />  // ← Added dashboard route
      </Routes>
    </Router>
  )
}

export default App