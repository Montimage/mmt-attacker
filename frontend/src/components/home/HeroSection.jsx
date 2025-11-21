import { AlertTriangle, ArrowRight, Shield, Target, Users, GraduationCap, Zap } from 'lucide-react'
import { Link } from 'react-router-dom'

function HeroSection() {
  return (
    <div className="relative bg-white py-16 md:py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Main Title */}
        <div className="text-center mb-12 animate-fade-in">
          <div className="flex justify-center mb-6">
            <img
              src="/logo.svg"
              alt="MMT-Attacker Logo"
              className="w-24 h-24 md:w-32 md:h-32 object-contain animate-pulse-slow"
            />
          </div>
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-black mb-4">
            MMT-Attacker
          </h1>
          <h2 className="text-2xl md:text-3xl font-semibold text-gray-900 mb-6">
            Demonstration Platform
          </h2>
          <p className="text-xl md:text-2xl text-gray-700 max-w-3xl mx-auto mb-8">
            Interactive Cybersecurity Attack Simulation
          </p>

          {/* Key Benefits */}
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-5xl mx-auto mt-12 mb-8">
            <div className="bg-white border-2 border-gray-300 rounded-lg p-6 hover:border-black hover:shadow-custom-md transition-all">
              <Shield className="w-10 h-10 text-black mx-auto mb-3" />
              <h3 className="font-bold text-black mb-2">Safe Learning</h3>
              <p className="text-sm text-gray-600">Simulated environment with no real impact</p>
            </div>
            <div className="bg-white border-2 border-gray-300 rounded-lg p-6 hover:border-black hover:shadow-custom-md transition-all">
              <Target className="w-10 h-10 text-black mx-auto mb-3" />
              <h3 className="font-bold text-black mb-2">Hands-on Practice</h3>
              <p className="text-sm text-gray-600">Interactive attack scenarios with real commands</p>
            </div>
            <div className="bg-white border-2 border-gray-300 rounded-lg p-6 hover:border-black hover:shadow-custom-md transition-all">
              <Zap className="w-10 h-10 text-black mx-auto mb-3" />
              <h3 className="font-bold text-black mb-2">Real-world Scenarios</h3>
              <p className="text-sm text-gray-600">Learn from actual attack techniques</p>
            </div>
            <div className="bg-white border-2 border-gray-300 rounded-lg p-6 hover:border-black hover:shadow-custom-md transition-all">
              <GraduationCap className="w-10 h-10 text-black mx-auto mb-3" />
              <h3 className="font-bold text-black mb-2">Educational Focus</h3>
              <p className="text-sm text-gray-600">Designed for training and awareness</p>
            </div>
          </div>

          {/* Use Cases */}
          <div className="bg-gray-50 border-2 border-gray-300 rounded-lg p-6 max-w-4xl mx-auto">
            <div className="flex items-center justify-center mb-4">
              <Users className="w-6 h-6 text-black mr-2" />
              <h3 className="font-bold text-black text-lg">Who This Is For</h3>
            </div>
            <div className="flex flex-wrap justify-center gap-3 text-sm">
              <span className="bg-white border-2 border-gray-300 px-4 py-2 rounded-lg font-medium">Security Professionals</span>
              <span className="bg-white border-2 border-gray-300 px-4 py-2 rounded-lg font-medium">Students & Educators</span>
              <span className="bg-white border-2 border-gray-300 px-4 py-2 rounded-lg font-medium">Researchers</span>
              <span className="bg-white border-2 border-gray-300 px-4 py-2 rounded-lg font-medium">Penetration Testers</span>
            </div>
          </div>
        </div>

        {/* Legal Warning Banner */}
        <div className="max-w-4xl mx-auto mb-8 animate-slide-up">
          <div className="bg-white border-4 border-black rounded-lg shadow-custom-xl p-6 md:p-8">
            <div className="flex items-start space-x-4">
              <AlertTriangle className="w-10 h-10 md:w-12 md:h-12 text-black flex-shrink-0 mt-1 animate-bounce-slow" />
              <div>
                <h3 className="text-2xl md:text-3xl font-bold text-black mb-3">
                  ⚠️ Legal Warning
                </h3>
                <div className="text-gray-800 leading-relaxed space-y-2">
                  <p className="text-lg font-semibold">
                    This tool is for <span className="text-green-600 font-bold">EDUCATIONAL AND TESTING PURPOSES ONLY</span>.
                  </p>
                  <p className="text-base">
                    Users must:
                  </p>
                  <ul className="list-disc list-inside space-y-1 ml-2 text-base">
                    <li>Obtain proper authorization before testing</li>
                    <li>Use in controlled environments only</li>
                    <li>Follow responsible disclosure practices</li>
                    <li>Comply with all applicable laws and regulations</li>
                    <li>Accept full responsibility for any consequences</li>
                  </ul>
                  <p className="text-base font-semibold mt-4 text-gray-900">
                    ⚠️ Improper use of this tool may be illegal and result in criminal charges.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Call to Action */}
        <div className="text-center animate-fade-in">
          <Link
            to="/browse"
            className="inline-flex items-center space-x-2 bg-white text-black border-2 border-black px-8 py-4 rounded-lg font-bold text-lg shadow-custom-lg hover:shadow-custom-xl hover:-translate-y-1 active:translate-y-0 active:shadow-custom-lg transition-all duration-200"
          >
            <span>Explore Attack Types</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </div>
    </div>
  )
}

export default HeroSection
