import { Video, Eye, UserCheck, ArrowRight } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <div className="min-h-screen bg-linear-to-b from-slate-50 to-white">
      {/* Hero Section - More dramatic and modern */}
      <section className="relative py-40 overflow-hidden">
        <div className="absolute inset-0 bg-linear-to-br from-blue-600/10 via-indigo-600/10 to-purple-600/10"></div>
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(99,102,241,0.1),transparent_70%)]"></div>
        
        <div className="relative max-w-7xl mx-auto px-6 text-center">
          <h1 className="text-8xl font-black text-gray-900 mb-10 leading-tight">
            SkillSync
          </h1>
          <p className="text-4xl text-gray-700 mb-16 max-w-5xl mx-auto font-light leading-relaxed">
            The future of contractor-client connections — powered by virtual consultations, AR previews, and verified trust.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-10 justify-center items-center">
            <Link
              to="/register?role=client"
              className="group bg-linear-to-r from-blue-600 to-indigo-600 text-white px-16 py-8 rounded-3xl text-3xl font-bold hover:from-blue-700 hover:to-indigo-700 transition-all shadow-2xl flex items-center gap-6 hover:scale-105"
            >
              Find a Contractor
              <ArrowRight className="w-10 h-10 group-hover:translate-x-3 transition" />
            </Link>
            
            <Link
              to="/register?role=contractor"
              className="group bg-linear-to-r from-green-600 to-emerald-600 text-white px-16 py-8 rounded-3xl text-3xl font-bold hover:from-green-700 hover:to-emerald-700 transition-all shadow-2xl flex items-center gap-6 hover:scale-105"
            >
              Get Hired Today
              <ArrowRight className="w-10 h-10 group-hover:translate-x-3 transition" />
            </Link>
          </div>
        </div>
      </section>

      {/* Features - Elevated cards with stronger hover */}
      <section className="py-32 bg-white">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <h2 className="text-6xl font-bold text-gray-900 mb-24">Built for the Future of Work</h2>
          
          <div className="grid md:grid-cols-3 gap-16">
            <div className="group bg-linear-to-br from-blue-50/80 to-blue-100/80 p-16 rounded-3xl shadow-xl hover:shadow-3xl hover:-translate-y-6 transition-all duration-500 border border-blue-200/50">
              <div className="w-32 h-32 mx-auto mb-10 bg-linear-to-br from-blue-200 to-blue-300 rounded-full flex items-center justify-center shadow-inner">
                <Video className="w-16 h-16 text-blue-700" />
              </div>
              <h3 className="text-4xl font-bold mb-6">Virtual Consultations</h3>
              <p className="text-xl text-gray-700 leading-relaxed">Real-time video walkthroughs — diagnose, quote, and plan without leaving home.</p>
            </div>

            <div className="group bg-linear-to-br from-purple-50/80 to-purple-100/80 p-16 rounded-3xl shadow-xl hover:shadow-3xl hover:-translate-y-6 transition-all duration-500 border border-purple-200/50">
              <div className="w-32 h-32 mx-auto mb-10 bg-linear-to-br from-purple-200 to-purple-300 rounded-full flex items-center justify-center shadow-inner">
                <Eye className="w-16 h-16 text-purple-700" />
              </div>
              <h3 className="text-4xl font-bold mb-6">AR Previews</h3>
              <p className="text-xl text-gray-700 leading-relaxed">See your renovation in real space before committing — reduce changes and surprises.</p>
            </div>

            <div className="group bg-linear-to-br from-green-50/80 to-green-100/80 p-16 rounded-3xl shadow-xl hover:shadow-3xl hover:-translate-y-6 transition-all duration-500 border border-green-200/50">
              <div className="w-32 h-32 mx-auto mb-10 bg-linear-to-br from-green-200 to-green-300 rounded-full flex items-center justify-center shadow-inner">
                <UserCheck className="w-16 h-16 text-green-700" />
              </div>
              <h3 className="text-4xl font-bold mb-6">Verified Professionals</h3>
              <p className="text-xl text-gray-700 leading-relaxed">Licensed, insured, reviewed — only the best contractors join SkillSync.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-linear-to-r from-gray-900 to-black text-white py-16 text-center">
        <p className="text-xl">© 2026 SkillSync — Redefining trust in home services</p>
      </footer>
    </div>
  )
}