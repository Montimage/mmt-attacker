import { AlertTriangle, ArrowRight, Shield, Target, Users, GraduationCap, Zap } from 'lucide-react'
import { Link } from 'react-router-dom'

function HeroSection() {
  return (
    <div className="relative overflow-hidden">
      {/* Dark gradient hero */}
      <div className="bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 py-20 md:py-28">
        {/* Subtle grid pattern overlay */}
        <div
          className="absolute inset-0 opacity-5"
          style={{
            backgroundImage: 'linear-gradient(rgba(34,197,94,0.3) 1px, transparent 1px), linear-gradient(90deg, rgba(34,197,94,0.3) 1px, transparent 1px)',
            backgroundSize: '40px 40px'
          }}
        />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12 animate-fade-in">
            <div className="flex justify-center mb-6">
              <div className="relative">
                <div className="absolute inset-0 rounded-full bg-green-500 opacity-10 blur-2xl scale-150" />
                <img
                  src="/logo.svg"
                  alt="MMT-Attacker Logo"
                  className="relative w-20 h-20 md:w-28 md:h-28 object-contain animate-pulse-slow"
                />
              </div>
            </div>

            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-3 tracking-tight">
              MMT-Attacker
            </h1>
            <h2 className="text-xl md:text-2xl font-medium text-green-400 mb-5">
              Demonstration Platform
            </h2>
            <p className="text-lg md:text-xl text-slate-300 max-w-2xl mx-auto mb-10">
              Interactive Cybersecurity Attack Simulation for Education and Research
            </p>

            {/* Key Benefits */}
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 max-w-5xl mx-auto mb-10">
              {[
                { Icon: Shield, label: 'Safe Learning', desc: 'Simulated environment with no real impact' },
                { Icon: Target, label: 'Hands-on Practice', desc: 'Interactive scenarios with real commands' },
                { Icon: Zap, label: 'Real-world Scenarios', desc: 'Learn from actual attack techniques' },
                { Icon: GraduationCap, label: 'Educational Focus', desc: 'Designed for training and awareness' },
              ].map(({ Icon, label, desc }) => (
                <div
                  key={label}
                  className="bg-slate-800 border border-slate-700 rounded-xl p-5 hover:border-green-500 hover:bg-slate-700 transition-all duration-200 group"
                >
                  <Icon className="w-8 h-8 text-green-400 mx-auto mb-3 group-hover:scale-110 transition-transform" />
                  <h3 className="font-semibold text-white mb-1 text-sm">{label}</h3>
                  <p className="text-xs text-slate-400">{desc}</p>
                </div>
              ))}
            </div>

            {/* Who this is for */}
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-5 max-w-3xl mx-auto mb-10">
              <div className="flex items-center justify-center mb-3">
                <Users className="w-5 h-5 text-green-400 mr-2" />
                <h3 className="font-semibold text-white text-sm">Who This Is For</h3>
              </div>
              <div className="flex flex-wrap justify-center gap-2 text-xs">
                {['Security Professionals', 'Students & Educators', 'Researchers', 'Penetration Testers'].map(label => (
                  <span key={label} className="bg-slate-700 border border-slate-600 text-slate-300 px-3 py-1.5 rounded-lg">
                    {label}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Legal Warning Banner — on white background below hero */}
      <div className="bg-white py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 animate-slide-up">
          <div className="bg-amber-50 border-2 border-amber-400 rounded-xl shadow-custom-md p-6">
            <div className="flex items-start space-x-4">
              <AlertTriangle className="w-8 h-8 text-amber-500 flex-shrink-0 mt-0.5 animate-bounce-slow" />
              <div>
                <h3 className="text-xl font-bold text-amber-900 mb-2">
                  ⚠️ Legal Warning
                </h3>
                <div className="text-amber-800 leading-relaxed space-y-2">
                  <p className="font-semibold text-sm">
                    This tool is for <span className="text-green-700 font-bold">EDUCATIONAL AND TESTING PURPOSES ONLY</span>.
                  </p>
                  <ul className="text-sm space-y-1 list-disc list-inside ml-1">
                    <li>Obtain proper authorization before testing</li>
                    <li>Use in controlled environments only</li>
                    <li>Follow responsible disclosure practices</li>
                    <li>Comply with all applicable laws and regulations</li>
                    <li>Accept full responsibility for any consequences</li>
                  </ul>
                  <p className="text-sm font-semibold mt-3 text-amber-900">
                    ⚠️ Improper use of this tool may be illegal and result in criminal charges.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div className="bg-white pb-12 text-center animate-fade-in">
        <Link
          to="/browse"
          className="inline-flex items-center space-x-2 bg-green-600 text-white border border-green-700 px-8 py-3.5 rounded-xl font-bold text-base shadow-custom-lg hover:bg-green-500 hover:shadow-glow-lg hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200"
        >
          <span>Explore Attack Types</span>
          <ArrowRight className="w-5 h-5" />
        </Link>
      </div>
    </div>
  )
}

export default HeroSection
