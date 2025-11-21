import { Link } from 'react-router-dom'
import { Shield, AlertTriangle, ArrowRight, Grid } from 'lucide-react'

function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section - Clean and Focused */}
      <div className="relative py-20 md:py-32">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          {/* Logo */}
          <div className="flex justify-center mb-8">
            <div className="bg-white border-2 border-gray-400 rounded-2xl p-6 shadow-custom-lg">
              <Shield className="w-16 h-16 md:w-20 md:h-20 text-black" />
            </div>
          </div>

          {/* Title */}
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-black mb-6">
            MMT-Attacker
          </h1>
          <p className="text-xl md:text-2xl text-gray-700 mb-12 max-w-2xl mx-auto">
            Interactive Cybersecurity Attack Simulation Platform
          </p>

          {/* Primary CTA */}
          <Link
            to="/browse"
            className="inline-flex items-center space-x-3 bg-black text-white border-2 border-black px-10 py-5 rounded-lg font-bold text-xl shadow-custom-xl hover:shadow-custom-lg hover:-translate-y-1 active:translate-y-0 transition-all duration-200"
          >
            <Grid className="w-6 h-6" />
            <span>Explore Attacks</span>
            <ArrowRight className="w-6 h-6" />
          </Link>
        </div>
      </div>

      {/* Legal Warning - Compact */}
      <div className="border-t-2 border-gray-300 bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white border-2 border-black rounded-lg shadow-custom-lg p-8">
            <div className="flex items-start space-x-4">
              <AlertTriangle className="w-8 h-8 text-black flex-shrink-0 mt-1" />
              <div>
                <h2 className="text-2xl font-bold text-black mb-3">
                  Educational Use Only
                </h2>
                <p className="text-gray-800 leading-relaxed">
                  This tool is for <span className="text-green-600 font-bold">EDUCATIONAL AND TESTING PURPOSES ONLY</span>.
                  Users must obtain proper authorization, use in controlled environments, follow responsible disclosure practices,
                  and comply with all applicable laws. Improper use may be illegal and result in criminal charges.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="py-16 border-t-2 border-gray-300">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="text-5xl font-bold text-black mb-2">10+</div>
              <div className="text-lg text-gray-700 font-semibold">Attack Types</div>
              <p className="text-sm text-gray-600 mt-2">Network, Application & More</p>
            </div>
            <div className="text-center">
              <div className="text-5xl font-bold text-black mb-2">5</div>
              <div className="text-lg text-gray-700 font-semibold">Categories</div>
              <p className="text-sm text-gray-600 mt-2">Organized for Easy Discovery</p>
            </div>
            <div className="text-center">
              <div className="text-5xl font-bold text-black mb-2">100%</div>
              <div className="text-lg text-gray-700 font-semibold">Interactive</div>
              <p className="text-sm text-gray-600 mt-2">Hands-on Simulations</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
