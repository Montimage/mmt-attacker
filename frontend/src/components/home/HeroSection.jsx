import { AlertTriangle, Shield, ArrowDown } from 'lucide-react'

function HeroSection() {
  const scrollToCategories = () => {
    const categoriesSection = document.getElementById('attack-categories')
    if (categoriesSection) {
      categoriesSection.scrollIntoView({ behavior: 'smooth' })
    }
  }

  return (
    <div className="relative bg-gradient-to-b from-gray-50 to-white py-16 md:py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Main Title */}
        <div className="text-center mb-8 animate-fade-in">
          <div className="flex justify-center mb-6">
            <Shield className="w-20 h-20 md:w-24 md:h-24 text-green-900 animate-pulse-slow" />
          </div>
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-black mb-4">
            MMT-Attacker
          </h1>
          <h2 className="text-2xl md:text-3xl font-semibold text-green-900 mb-6">
            Demonstration Platform
          </h2>
          <p className="text-xl md:text-2xl text-gray-600 max-w-3xl mx-auto">
            Interactive Cybersecurity Attack Simulation
          </p>
        </div>

        {/* Legal Warning Banner */}
        <div className="max-w-4xl mx-auto mb-8 animate-slide-up">
          <div className="bg-white border-4 border-green-900 rounded-lg shadow-custom-lg p-6 md:p-8">
            <div className="flex items-start space-x-4">
              <AlertTriangle className="w-10 h-10 md:w-12 md:h-12 text-green-900 flex-shrink-0 mt-1 animate-bounce-slow" />
              <div>
                <h3 className="text-2xl md:text-3xl font-bold text-green-900 mb-3">
                  ⚠️ Legal Warning
                </h3>
                <div className="text-gray-800 leading-relaxed space-y-2">
                  <p className="text-lg font-semibold">
                    This tool is for <span className="text-green-900">EDUCATIONAL AND TESTING PURPOSES ONLY</span>.
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
          <button
            onClick={scrollToCategories}
            className="inline-flex items-center space-x-2 bg-green-900 text-white px-8 py-4 rounded-lg font-semibold text-lg shadow-custom-lg hover:bg-green-800 hover:shadow-custom-md transition-all duration-200 transform hover:-translate-y-1"
          >
            <span>Explore Attack Types</span>
            <ArrowDown className="w-5 h-5 animate-bounce" />
          </button>
        </div>
      </div>
    </div>
  )
}

export default HeroSection
