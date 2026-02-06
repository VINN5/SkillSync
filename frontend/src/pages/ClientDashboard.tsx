import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

interface Project {
  id: string
  title: string
  description: string
  budget: number
  status: 'open' | 'in_progress' | 'completed'
  skillsRequired: string[]
  postedDate: string
  proposals?: number
}

interface Contractor {
  id: string
  name: string
  skills: string[]
  rating: number
  hourlyRate: number
  completedProjects: number
  avatar?: string
}

export default function ClientDashboard() {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState<'projects' | 'browse' | 'messages'>('projects')
  const [projects, setProjects] = useState<Project[]>([])
  const [contractors, setContractors] = useState<Contractor[]>([])
  const [showNewProjectModal, setShowNewProjectModal] = useState(false)
  const [newProject, setNewProject] = useState({
    title: '',
    description: '',
    budget: '',
    skillsRequired: ''
  })

  useEffect(() => {
    // Fetch client's projects from API
    // Mock data for now
    setProjects([
      {
        id: '1',
        title: 'E-commerce Website Development',
        description: 'Need a full-stack developer to build a modern e-commerce platform with payment integration',
        budget: 5000,
        status: 'open',
        skillsRequired: ['React', 'Node.js', 'MongoDB'],
        postedDate: '2024-02-01',
        proposals: 12
      },
      {
        id: '2',
        title: 'Mobile App UI/UX Design',
        description: 'Looking for a designer to create intuitive mobile app designs',
        budget: 2000,
        status: 'in_progress',
        skillsRequired: ['Figma', 'UI/UX', 'Mobile Design'],
        postedDate: '2024-01-28',
        proposals: 8
      },
      {
        id: '3',
        title: 'Logo and Brand Identity',
        description: 'Need a creative designer for company rebranding',
        budget: 1500,
        status: 'completed',
        skillsRequired: ['Graphic Design', 'Branding', 'Adobe Illustrator'],
        postedDate: '2024-01-15',
        proposals: 15
      }
    ])

    // Fetch available contractors
    setContractors([
      {
        id: '1',
        name: 'Sarah Johnson',
        skills: ['React', 'Node.js', 'TypeScript', 'PostgreSQL'],
        rating: 4.9,
        hourlyRate: 85,
        completedProjects: 47
      },
      {
        id: '2',
        name: 'Michael Chen',
        skills: ['UI/UX Design', 'Figma', 'Mobile Design', 'Prototyping'],
        rating: 4.8,
        hourlyRate: 75,
        completedProjects: 62
      },
      {
        id: '3',
        name: 'Emily Rodriguez',
        skills: ['Python', 'Django', 'AWS', 'Docker'],
        rating: 5.0,
        hourlyRate: 95,
        completedProjects: 34
      },
      {
        id: '4',
        name: 'David Park',
        skills: ['Graphic Design', 'Branding', 'Adobe Suite', 'Illustration'],
        rating: 4.7,
        hourlyRate: 65,
        completedProjects: 89
      }
    ])
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  const handleCreateProject = (e: React.FormEvent) => {
    e.preventDefault()
    // API call to create project
    const project: Project = {
      id: String(projects.length + 1),
      title: newProject.title,
      description: newProject.description,
      budget: Number(newProject.budget),
      status: 'open',
      skillsRequired: newProject.skillsRequired.split(',').map(s => s.trim()),
      postedDate: new Date().toISOString().split('T')[0],
      proposals: 0
    }
    setProjects([project, ...projects])
    setShowNewProjectModal(false)
    setNewProject({ title: '', description: '', budget: '', skillsRequired: '' })
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open': return 'bg-green-100 text-green-800'
      case 'in_progress': return 'bg-blue-100 text-blue-800'
      case 'completed': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'open': return 'Open'
      case 'in_progress': return 'In Progress'
      case 'completed': return 'Completed'
      default: return status
    }
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Client Dashboard</h1>
              <p className="text-sm text-gray-600 mt-1">Manage your projects and find contractors</p>
            </div>
            <button
              onClick={handleLogout}
              className="px-6 py-2.5 bg-red-600 text-white rounded-lg font-medium hover:bg-red-700 transition-colors shadow-sm"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Active Projects</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">
                  {projects.filter(p => p.status === 'open' || p.status === 'in_progress').length}
                </p>
              </div>
              <div className="bg-blue-100 p-3 rounded-lg">
                <svg className="w-8 h-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Proposals</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">
                  {projects.reduce((sum, p) => sum + (p.proposals || 0), 0)}
                </p>
              </div>
              <div className="bg-green-100 p-3 rounded-lg">
                <svg className="w-8 h-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Completed</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">
                  {projects.filter(p => p.status === 'completed').length}
                </p>
              </div>
              <div className="bg-purple-100 p-3 rounded-lg">
                <svg className="w-8 h-8 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Budget</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">
                  ${projects.reduce((sum, p) => sum + p.budget, 0).toLocaleString()}
                </p>
              </div>
              <div className="bg-yellow-100 p-3 rounded-lg">
                <svg className="w-8 h-8 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 mb-6">
          <div className="flex border-b border-gray-200">
            <button
              onClick={() => setActiveTab('projects')}
              className={`flex-1 px-6 py-4 text-sm font-medium transition-colors ${
                activeTab === 'projects'
                  ? 'text-blue-600 border-b-2 border-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              My Projects
            </button>
            <button
              onClick={() => setActiveTab('browse')}
              className={`flex-1 px-6 py-4 text-sm font-medium transition-colors ${
                activeTab === 'browse'
                  ? 'text-blue-600 border-b-2 border-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Browse Contractors
            </button>
            <button
              onClick={() => setActiveTab('messages')}
              className={`flex-1 px-6 py-4 text-sm font-medium transition-colors ${
                activeTab === 'messages'
                  ? 'text-blue-600 border-b-2 border-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Messages
            </button>
          </div>

          <div className="p-6">
            {/* Projects Tab */}
            {activeTab === 'projects' && (
              <div>
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-xl font-bold text-gray-900">Your Projects</h2>
                  <button
                    onClick={() => setShowNewProjectModal(true)}
                    className="px-6 py-2.5 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors shadow-sm flex items-center gap-2"
                  >
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                    </svg>
                    New Project
                  </button>
                </div>

                <div className="space-y-4">
                  {projects.map((project) => (
                    <div key={project.id} className="bg-gray-50 rounded-lg p-6 border border-gray-200 hover:border-blue-300 transition-colors">
                      <div className="flex justify-between items-start mb-3">
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900">{project.title}</h3>
                          <p className="text-sm text-gray-600 mt-1">Posted on {project.postedDate}</p>
                        </div>
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(project.status)}`}>
                          {getStatusText(project.status)}
                        </span>
                      </div>
                      
                      <p className="text-gray-700 mb-4">{project.description}</p>
                      
                      <div className="flex flex-wrap gap-2 mb-4">
                        {project.skillsRequired.map((skill, idx) => (
                          <span key={idx} className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm font-medium">
                            {skill}
                          </span>
                        ))}
                      </div>
                      
                      <div className="flex justify-between items-center pt-4 border-t border-gray-200">
                        <div className="flex gap-6">
                          <div>
                            <p className="text-sm text-gray-600">Budget</p>
                            <p className="text-lg font-bold text-gray-900">${project.budget.toLocaleString()}</p>
                          </div>
                          <div>
                            <p className="text-sm text-gray-600">Proposals</p>
                            <p className="text-lg font-bold text-gray-900">{project.proposals || 0}</p>
                          </div>
                        </div>
                        <button className="px-5 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors">
                          View Details
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Browse Contractors Tab */}
            {activeTab === 'browse' && (
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-6">Available Contractors</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {contractors.map((contractor) => (
                    <div key={contractor.id} className="bg-gray-50 rounded-lg p-6 border border-gray-200 hover:border-blue-300 transition-colors">
                      <div className="flex items-start gap-4 mb-4">
                        <div className="w-16 h-16 bg-linear-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-xl font-bold">
                          {contractor.name.split(' ').map(n => n[0]).join('')}
                        </div>
                        <div className="flex-1">
                          <h3 className="text-lg font-semibold text-gray-900">{contractor.name}</h3>
                          <div className="flex items-center gap-2 mt-1">
                            <div className="flex items-center">
                              <svg className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                              </svg>
                              <span className="text-sm font-medium text-gray-900 ml-1">{contractor.rating}</span>
                            </div>
                            <span className="text-sm text-gray-600">• {contractor.completedProjects} projects</span>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex flex-wrap gap-2 mb-4">
                        {contractor.skills.map((skill, idx) => (
                          <span key={idx} className="px-3 py-1 bg-white border border-gray-300 text-gray-700 rounded-full text-sm">
                            {skill}
                          </span>
                        ))}
                      </div>
                      
                      <div className="flex justify-between items-center pt-4 border-t border-gray-200">
                        <div>
                          <p className="text-sm text-gray-600">Hourly Rate</p>
                          <p className="text-xl font-bold text-gray-900">${contractor.hourlyRate}/hr</p>
                        </div>
                        <button className="px-5 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors">
                          Contact
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Messages Tab */}
            {activeTab === 'messages' && (
              <div className="text-center py-12">
                <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">No messages yet</h3>
                <p className="text-gray-600">Start a conversation with contractors</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* New Project Modal */}
      {showNewProjectModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl max-w-2xl w-full p-8 shadow-2xl">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Create New Project</h2>
            <form onSubmit={handleCreateProject}>
              <div className="space-y-5">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Project Title</label>
                  <input
                    type="text"
                    required
                    value={newProject.title}
                    onChange={(e) => setNewProject({ ...newProject, title: e.target.value })}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="e.g., E-commerce Website Development"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                  <textarea
                    required
                    value={newProject.description}
                    onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
                    rows={4}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Describe your project requirements..."
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Budget ($)</label>
                  <input
                    type="number"
                    required
                    value={newProject.budget}
                    onChange={(e) => setNewProject({ ...newProject, budget: e.target.value })}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="5000"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Required Skills (comma-separated)</label>
                  <input
                    type="text"
                    required
                    value={newProject.skillsRequired}
                    onChange={(e) => setNewProject({ ...newProject, skillsRequired: e.target.value })}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="React, Node.js, MongoDB"
                  />
                </div>
              </div>
              
              <div className="flex gap-4 mt-8">
                <button
                  type="button"
                  onClick={() => setShowNewProjectModal(false)}
                  className="flex-1 px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
                >
                  Create Project
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}