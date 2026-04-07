import { ArrowRight, Terminal, ChevronRight, Lock, Network, Globe, Key, Repeat, Zap } from 'lucide-react'
import { Link } from 'react-router-dom'

const TERMINAL_LINES = [
  { type: 'cmd',    text: '$ mag syn-flood --target-ip 192.168.56.10 --target-port 80 --count 500' },
  { type: 'info',   text: '[*] Starting SYN Flood attack on 192.168.56.10:80' },
  { type: 'info',   text: '[*] Sending 500 SYN packets (spoofed source IPs)' },
  { type: 'ok',     text: '[+] Packet  100/500 — 18,432 bytes sent' },
  { type: 'ok',     text: '[+] Packet  250/500 — 46,080 bytes sent' },
  { type: 'ok',     text: '[+] Packet  500/500 — 92,160 bytes sent' },
  { type: 'result', text: '[=] Attack complete: 500 packets · 90.0 KB · target unresponsive' },
]

const STEPS = [
  { n: '01', label: 'Pick an attack', desc: 'Browse 26 techniques across 5 categories.' },
  { n: '02', label: 'Configure parameters', desc: 'Fill the form — IP, port, count, interface.' },
  { n: '03', label: 'Copy & run', desc: 'Get the exact mag command. Paste into your terminal.' },
]

const ATTACK_LAYERS = [
  {
    Icon: Network,
    label: 'Network',
    count: 10,
    attacks: ['SYN Flood', 'ARP Spoof', 'UDP Flood', 'ICMP Flood', 'DHCP Starvation', 'MAC Flooding', '+4 more'],
  },
  {
    Icon: Globe,
    label: 'Application',
    count: 10,
    attacks: ['HTTP DoS', 'Slowloris', 'SQL Injection', 'XSS', 'Directory Traversal', 'SSL Strip', '+4 more'],
  },
  {
    Icon: Zap,
    label: 'Amplification',
    count: 2,
    attacks: ['DNS Amplification', 'NTP Amplification'],
  },
  {
    Icon: Key,
    label: 'Credential',
    count: 4,
    attacks: ['SSH Brute Force', 'FTP Brute Force', 'RDP Brute Force', 'Credential Harvester'],
  },
  {
    Icon: Repeat,
    label: 'Replay',
    count: 2,
    attacks: ['MITM', 'PCAP Replay'],
  },
]

function HeroSection() {
  return (
    <div className="bg-gray-950">

      {/* ── Hero ─────────────────────────────────────────────────── */}
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-14">
        <div className="grid lg:grid-cols-2 gap-12 items-center">

          {/* Left: copy */}
          <div>
            <div className="inline-flex items-center gap-2 bg-green-950 border border-green-800 text-green-400 text-xs font-semibold px-3 py-1.5 rounded-full mb-6">
              <Lock className="w-3 h-3" />
              Authorized use only · Educational platform
            </div>

            <h1 className="text-4xl md:text-5xl font-bold text-gray-100 mb-4 leading-tight tracking-tight">
              26 network attacks.<br />
              Browser to terminal<br />
              <span className="text-green-400">in 30 seconds.</span>
            </h1>

            <p className="text-lg text-gray-400 mb-8 leading-relaxed">
              Configure any attack visually, get the exact <code className="text-green-400 bg-gray-800 px-1.5 py-0.5 rounded text-sm">mag</code> CLI command, run it in a Docker container against your lab. Built for red-team demos, security courses, and authorized pentesting.
            </p>

            <div className="flex flex-col sm:flex-row gap-3">
              <Link
                to="/browse"
                className="inline-flex items-center justify-center gap-2 bg-green-600 text-white border border-green-500 px-7 py-3 rounded-xl font-bold text-sm shadow-custom-md hover:bg-green-500 hover:shadow-custom-lg hover:-translate-y-0.5 transition-all duration-200"
              >
                Browse Attacks
                <ArrowRight className="w-4 h-4" />
              </Link>
              <Link
                to="/docs"
                className="inline-flex items-center justify-center gap-2 bg-gray-800 text-gray-100 border-2 border-gray-600 px-7 py-3 rounded-xl font-semibold text-sm hover:border-gray-400 hover:shadow-custom-md hover:-translate-y-0.5 transition-all duration-200"
              >
                <Terminal className="w-4 h-4" />
                CLI Docs
              </Link>
            </div>

            {/* Stats */}
            <div className="flex gap-8 mt-10 pt-8 border-t border-gray-800">
              {[['26', 'attack types'], ['50+', 'scenarios'], ['5', 'categories']].map(([n, label]) => (
                <div key={label}>
                  <div className="text-2xl font-bold text-gray-100">{n}</div>
                  <div className="text-xs text-gray-500 mt-0.5">{label}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Right: terminal preview */}
          <div className="bg-gray-900 border border-gray-700 rounded-2xl overflow-hidden shadow-custom-xl">
            {/* Terminal chrome */}
            <div className="flex items-center gap-1.5 px-4 py-3 border-b border-gray-700 bg-gray-800">
              <span className="w-3 h-3 rounded-full bg-red-500/70" />
              <span className="w-3 h-3 rounded-full bg-yellow-500/70" />
              <span className="w-3 h-3 rounded-full bg-green-500/70" />
              <span className="ml-3 text-xs text-gray-500 font-mono">mag · attacker container</span>
            </div>
            {/* Terminal body */}
            <div className="p-5 font-mono text-xs leading-relaxed space-y-1.5">
              {TERMINAL_LINES.map((line, i) => (
                <div key={i} className={
                  line.type === 'cmd'    ? 'text-gray-100' :
                  line.type === 'ok'    ? 'text-green-400' :
                  line.type === 'result'? 'text-yellow-300 font-semibold' :
                                          'text-gray-400'
                }>
                  {line.text}
                </div>
              ))}
              <div className="text-gray-600 mt-3">█</div>
            </div>
          </div>
        </div>
      </div>

      {/* ── How it works ─────────────────────────────────────────── */}
      <div className="border-t border-gray-800 bg-gray-900 py-14">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-xl font-bold text-gray-100 mb-10 text-center">How it works</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {STEPS.map(({ n, label, desc }, i) => (
              <div key={n} className="relative flex gap-4 items-start">
                <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-green-950 border border-green-800 flex items-center justify-center">
                  <span className="text-xs font-bold text-green-400 font-mono">{n}</span>
                </div>
                <div>
                  <h3 className="font-bold text-gray-100 text-sm mb-1">{label}</h3>
                  <p className="text-xs text-gray-400 leading-relaxed">{desc}</p>
                </div>
                {i < STEPS.length - 1 && (
                  <ChevronRight className="hidden md:block absolute -right-3 top-3 w-4 h-4 text-gray-600" />
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ── Attack coverage ──────────────────────────────────────── */}
      <div className="border-t border-gray-800 bg-gray-950 py-14">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-xl font-bold text-gray-100">Attack coverage</h2>
            <Link
              to="/browse"
              className="text-xs text-green-400 hover:text-green-300 font-medium flex items-center gap-1 transition-colors"
            >
              Browse all <ArrowRight className="w-3 h-3" />
            </Link>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
            {ATTACK_LAYERS.map(({ Icon, label, count, attacks }) => (
              <div
                key={label}
                className="bg-gray-900 border border-gray-700 rounded-xl p-4 hover:border-green-600 transition-colors"
              >
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-7 h-7 rounded-md bg-green-950 border border-green-800 flex items-center justify-center flex-shrink-0">
                    <Icon className="w-3.5 h-3.5 text-green-400" />
                  </div>
                  <div>
                    <span className="text-xs font-bold text-gray-100">{label}</span>
                    <span className="ml-1.5 text-xs text-gray-500">·{count}</span>
                  </div>
                </div>
                <ul className="space-y-1">
                  {attacks.map(a => (
                    <li key={a} className={`text-xs ${a.startsWith('+') ? 'text-gray-600 italic' : 'text-gray-400'}`}>
                      {a}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ── Access CTA ───────────────────────────────────────────── */}
      <div className="border-t border-gray-800 bg-gray-900 py-14">
        <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center gap-2 bg-gray-800 border border-gray-700 rounded-full px-4 py-1.5 text-xs text-gray-400 mb-6">
            <Lock className="w-3 h-3" />
            CLI access is free · private distribution
          </div>
          <h2 className="text-2xl font-bold text-gray-100 mb-3">Get the mag CLI</h2>
          <p className="text-gray-400 text-sm mb-6">
            The web interface is open. The <code className="text-green-400 bg-gray-800 px-1 py-0.5 rounded">mag</code> CLI is distributed privately to prevent misuse — email us with your name, org, and intended use.
          </p>
          <a
            href="mailto:contact@montimage.eu?subject=mag CLI access request"
            className="inline-flex items-center gap-2 bg-green-600 text-white border border-green-500 px-7 py-3 rounded-xl font-bold text-sm shadow-custom-md hover:bg-green-500 hover:shadow-custom-lg hover:-translate-y-0.5 transition-all duration-200"
          >
            Request CLI access
            <ArrowRight className="w-4 h-4" />
          </a>
          <p className="text-xs text-gray-600 mt-4">contact@montimage.eu · subject: mag CLI access request</p>
        </div>
      </div>

    </div>
  )
}

export default HeroSection
