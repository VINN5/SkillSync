import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import AdminDashboard from './AdminDashboard'
import ClientDashboard from './ClientDashboard'
import ContractorDashboard from './ContractorDashboard'

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

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-2xl text-gray-600">Loading dashboard...</div>
      </div>
    )
  }

  // Route to the appropriate dashboard based on role
  if (user.role === 'admin') return <AdminDashboard />
  if (user.role === 'client') return <ClientDashboard />
  if (user.role === 'contractor') return <ContractorDashboard />

  // Fallback for unknown roles
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-2xl text-red-600">Unknown user role</div>
    </div>
  )
}
