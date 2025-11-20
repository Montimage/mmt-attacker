import { AlertTriangle, Shield } from 'lucide-react'

function Home() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <div className="flex justify-center mb-6">
          <Shield className="w-20 h-20 text-green-900" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold text-black mb-4">
          MMT-Attacker Demonstration Platform
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Interactive Cybersecurity Attack Simulation
        </p>

        {/* Legal Warning Banner */}
        <div className="card border-green-900 bg-green-50 max-w-3xl mx-auto">
          <div className="flex items-start space-x-3">
            <AlertTriangle className="w-8 h-8 text-green-900 flex-shrink-0 mt-1" />
            <div className="text-left">
              <h3 className="text-xl font-bold text-green-900 mb-2">⚠️ Legal Warning</h3>
              <p className="text-gray-800 leading-relaxed">
                This tool is for <strong>EDUCATIONAL AND TESTING PURPOSES ONLY</strong>.
                You must obtain proper authorization before testing, use in controlled
                environments only, and comply with all applicable laws and regulations.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Attack Categories Section */}
      <div className="mt-16">
        <h2 className="text-3xl font-bold text-black mb-8 text-center">Attack Categories</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Placeholder cards - will be replaced with actual attack cards */}
          <div className="card card-hover cursor-pointer">
            <h3 className="text-xl font-bold text-black mb-2">Network-Layer Attacks</h3>
            <p className="text-gray-600">ARP Spoofing, SYN Flood, Ping of Death</p>
          </div>
          <div className="card card-hover cursor-pointer">
            <h3 className="text-xl font-bold text-black mb-2">Application-Layer Attacks</h3>
            <p className="text-gray-600">HTTP DoS, Slowloris, Credential Harvester</p>
          </div>
          <div className="card card-hover cursor-pointer">
            <h3 className="text-xl font-bold text-black mb-2">Amplification Attacks</h3>
            <p className="text-gray-600">DNS Amplification</p>
          </div>
          <div className="card card-hover cursor-pointer">
            <h3 className="text-xl font-bold text-black mb-2">Credential Attacks</h3>
            <p className="text-gray-600">SSH Brute Force, SQL Injection</p>
          </div>
          <div className="card card-hover cursor-pointer">
            <h3 className="text-xl font-bold text-black mb-2">PCAP Replay</h3>
            <p className="text-gray-600">Traffic replay and simulation</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
