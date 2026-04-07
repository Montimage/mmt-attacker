import { ArrowRight, Shield, GraduationCap, Zap, Terminal, BookOpen, Users } from 'lucide-react'
import { Link } from 'react-router-dom'

function HeroSection() {
  return (
    <div className="bg-gray-950">
      {/* Hero */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-12 text-center">
        <div className="flex justify-center mb-6">
          <img
            src="/logo.svg"
            alt="MAG Logo"
            className="w-20 h-20 md:w-24 md:h-24 object-contain"
          />
        </div>

        <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-100 mb-4 tracking-tight">
          MAG
        </h1>
        <p className="text-xl md:text-2xl font-semibold text-green-400 mb-4">
          Montimage Attack Generator
        </p>
        <p className="text-lg text-gray-400 max-w-2xl mx-auto mb-10">
          Explore 26 real-world attack techniques through interactive simulations,
          hands-on CLI commands, and guided scenarios — built for security professionals,
          researchers, and educators.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-14">
          <Link
            to="/browse"
            className="inline-flex items-center gap-2 bg-green-600 text-white border border-green-500 px-8 py-3.5 rounded-xl font-bold text-base shadow-custom-md hover:bg-green-500 hover:shadow-custom-lg hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200"
          >
            <span>Explore Attacks</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
          <Link
            to="/about"
            className="inline-flex items-center gap-2 bg-gray-800 text-gray-100 border-2 border-gray-600 px-8 py-3.5 rounded-xl font-semibold text-base hover:border-gray-400 hover:shadow-custom-md hover:-translate-y-0.5 transition-all duration-200"
          >
            <BookOpen className="w-5 h-5" />
            <span>Learn More</span>
          </Link>
        </div>

        {/* Stats bar */}
        <div className="grid grid-cols-3 gap-6 max-w-xl mx-auto border-t-2 border-gray-800 pt-10">
          <div className="text-center">
            <div className="text-4xl font-bold text-gray-100 mb-1">26</div>
            <div className="text-sm font-semibold text-gray-400">Attack Types</div>
          </div>
          <div className="text-center border-x-2 border-gray-800">
            <div className="text-4xl font-bold text-gray-100 mb-1">5</div>
            <div className="text-sm font-semibold text-gray-400">Categories</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-gray-100 mb-1">50+</div>
            <div className="text-sm font-semibold text-gray-400">Scenarios</div>
          </div>
        </div>
      </div>

      {/* Features strip */}
      <div className="border-t-2 border-gray-800 bg-gray-900 py-12">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                Icon: Shield,
                label: 'Safe Environment',
                desc: 'Simulated attacks with zero real-world impact on live systems.',
              },
              {
                Icon: Terminal,
                label: 'Real CLI Commands',
                desc: 'Generate exact mag CLI commands from your chosen parameters.',
              },
              {
                Icon: Zap,
                label: 'Live Simulation',
                desc: 'Watch attacks unfold step-by-step with realistic log output.',
              },
              {
                Icon: GraduationCap,
                label: 'Educational Focus',
                desc: 'Built for training, awareness programs, and security research.',
              },
            ].map(({ Icon, label, desc }) => (
              <div
                key={label}
                className="bg-gray-800 border-2 border-gray-700 rounded-xl p-5 hover:border-green-500 hover:shadow-custom-md transition-all duration-200"
              >
                <div className="bg-green-950 border border-green-800 w-10 h-10 rounded-lg flex items-center justify-center mb-3">
                  <Icon className="w-5 h-5 text-green-400" />
                </div>
                <h3 className="font-bold text-gray-100 mb-1 text-sm">{label}</h3>
                <p className="text-xs text-gray-400 leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Who it's for */}
      <div className="py-12 bg-gray-950 border-t-2 border-gray-800">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-2 mb-6">
            <Users className="w-5 h-5 text-green-500" />
            <h2 className="text-lg font-bold text-gray-100">Who This Is For</h2>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              { title: 'Security Professionals', desc: 'Validate defences and understand attacker techniques.' },
              { title: 'Students & Educators', desc: 'Hands-on learning material for cybersecurity courses.' },
              { title: 'Researchers', desc: 'Reproduce attack patterns in a controlled environment.' },
              { title: 'Penetration Testers', desc: 'Reference implementation for common attack vectors.' },
            ].map(({ title, desc }) => (
              <div key={title} className="bg-gray-900 border-2 border-gray-700 rounded-xl p-5 hover:border-green-600 transition-colors">
                <div className="w-2 h-2 rounded-full bg-green-500 mb-3" />
                <h3 className="font-bold text-gray-200 text-sm mb-1">{title}</h3>
                <p className="text-xs text-gray-400 leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default HeroSection
