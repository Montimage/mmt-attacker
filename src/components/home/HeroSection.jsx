import { ArrowRight, Terminal, ChevronRight, Lock, Network, Globe, Key, Repeat, Zap } from 'lucide-react'
import { Link } from 'react-router-dom'
import { getCategories, getAttacksByCategory, getAllAttacks } from '../../data/attacksData'
import { useTheme } from '../../context/ThemeContext'

const TERMINAL_LINES = [
  { type: 'cmd',    text: '$ mag http-dos --target-url http://192.168.56.10 --num-connections 50 --duration 60' },
  { type: 'info',   text: '[*] Initialized HTTP DoS attack simulation' },
  { type: 'info',   text: '[*] Target: http://192.168.56.10  method: GET  connections: 50' },
  { type: 'ok',     text: '[+] Progress: 25.0%  active connections: 50  requests: 187' },
  { type: 'ok',     text: '[+] Progress: 50.0%  active connections: 50  requests: 374' },
  { type: 'ok',     text: '[+] Progress: 100.0%  active connections: 50  requests: 748' },
  { type: 'result', text: '[=] HTTP DoS complete: 748 requests · server response time +3400ms' },
]

const STEPS = [
  { n: '01', label: 'Study the attack', desc: 'Browse techniques, read how each attack works at the protocol level, and simulate it — all in the browser, no install required.' },
  { n: '02', label: 'Configure & generate', desc: 'Set target IP, port, count, and interface visually. Get the exact mag CLI command, ready to copy or pass to an agent.' },
  { n: '03', label: 'Execute & integrate', desc: 'Run mag in a Docker container against your lab. Works from the terminal, AI agent pipelines, or any automated pentest workflow.' },
]

const CATEGORY_META = {
  'Network-Layer':    { Icon: Network, label: 'Network' },
  'Application-Layer':{ Icon: Globe,   label: 'Application' },
  'Amplification':    { Icon: Zap,     label: 'Amplification' },
  'Credential':       { Icon: Key,     label: 'Credential' },
  'Other':            { Icon: Repeat,  label: 'Other' },
}

const MAX_SHOWN = 6

const MagKeyword = () => (
  <code className="font-bold text-green-500 bg-green-950 border border-green-700 px-2 py-0.5 rounded text-[0.95em] not-italic">
    mag
  </code>
)

function HeroSection() {
  const { isDark } = useTheme()
  const categories = getCategories()
  const allAttacks = getAllAttacks()
  const totalScenarios = allAttacks.reduce((sum, a) => sum + (a.scenarios?.length ?? 0), 0)

  const attackLayers = categories.map(cat => {
    const attacks = getAttacksByCategory(cat)
    const meta = CATEGORY_META[cat] ?? { Icon: Network, label: cat }
    const shown = attacks.slice(0, MAX_SHOWN).map(a => a.name)
    const remaining = attacks.length - shown.length
    return {
      ...meta,
      attacks: remaining > 0 ? [...shown, `+${remaining} more`] : shown,
    }
  })

  return (
    <div className="bg-gray-950">

      {/* ── Hero ─────────────────────────────────────────────────── */}
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-14">
        <div className="grid lg:grid-cols-2 gap-12 items-center">

          {/* Left: copy */}
          <div>
            <div className="inline-flex items-center gap-2 bg-green-950 border border-green-800 text-green-400 text-xs font-semibold px-3 py-1.5 rounded-full mb-6">
              <Lock className="w-3 h-3" />
              Authorized use only · Educational & pentesting platform
            </div>

            <h1 className="text-4xl md:text-5xl font-bold text-gray-100 mb-4 leading-tight tracking-tight">
              A pentesting toolkit<br />
              <span className="text-green-400">for humans & AI agents.</span>
            </h1>

            <p className="text-lg text-gray-400 mb-6 leading-relaxed">
              Run authorized network attacks from the <MagKeyword /> CLI — from your terminal, an AI agent, or any automated pentest pipeline. The web interface lets you explore and simulate attacks to understand how they work.
            </p>

            {/* Two-audience callouts */}
            <div className="flex flex-col sm:flex-row gap-3 mb-8">
              <div className="flex-1 bg-gray-900 border border-green-800 rounded-xl px-4 py-3">
                <div className="text-green-400 font-semibold text-sm mb-1.5">Pentesters & AI agents</div>
                <div className="text-gray-400 text-sm leading-relaxed">Drive attacks with the <MagKeyword /> CLI — integrate into red-team scripts, agentic workflows, or CI/CD security pipelines.</div>
              </div>
              <div className="flex-1 bg-gray-900 border border-gray-700 rounded-xl px-4 py-3">
                <div className="text-gray-200 font-semibold text-sm mb-1.5">Learners & researchers</div>
                <div className="text-gray-400 text-sm leading-relaxed">Simulate and study attacks in the browser — free, no install. Understand protocol mechanics and attack patterns.</div>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-3">
              <Link
                to="/browse"
                className="inline-flex items-center justify-center gap-2 bg-green-600 text-white border border-green-500 px-7 py-3 rounded-xl font-bold text-sm shadow-custom-md hover:bg-green-500 hover:shadow-custom-lg hover:-translate-y-0.5 transition-all duration-200"
              >
                Explore Attacks
                <ArrowRight className="w-4 h-4" />
              </Link>
              <Link
                to="/docs"
                className="inline-flex items-center justify-center gap-2 bg-gray-800 text-gray-100 border-2 border-gray-600 px-7 py-3 rounded-xl font-semibold text-sm hover:border-gray-400 hover:shadow-custom-md hover:-translate-y-0.5 transition-all duration-200"
              >
                <Terminal className="w-4 h-4" />
                CLI & Agent Docs
              </Link>
            </div>

            {/* Stats — derived from data */}
            <div className="flex gap-8 mt-10 pt-8 border-t border-gray-800">
              {[
                [allAttacks.length,  'attack types'],
                [totalScenarios,     'scenarios'],
                [categories.length,  'categories'],
              ].map(([n, label]) => (
                <div key={label}>
                  <div className="text-2xl font-bold text-gray-100">{n}</div>
                  <div className="text-xs text-gray-500 mt-0.5">{label}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Right: terminal preview */}
          <div
            className="rounded-2xl overflow-hidden shadow-custom-xl border"
            style={isDark
              ? { backgroundColor: '#f9fafb', borderColor: '#e5e7eb' }
              : { backgroundColor: '#111827', borderColor: '#374151' }
            }
          >
            <div
              className="flex items-center gap-1.5 px-4 py-3 border-b"
              style={isDark
                ? { backgroundColor: '#ffffff', borderColor: '#e5e7eb' }
                : { backgroundColor: '#1f2937', borderColor: '#374151' }
              }
            >
              <span className="w-3 h-3 rounded-full bg-red-400" />
              <span className="w-3 h-3 rounded-full bg-yellow-400" />
              <span className="w-3 h-3 rounded-full bg-green-400" />
              <span className="ml-3 text-xs font-mono" style={{ color: isDark ? '#9ca3af' : '#6b7280' }}>mag http-dos · attacker container</span>
            </div>
            <div className="p-5 font-mono text-xs leading-relaxed space-y-1.5">
              {TERMINAL_LINES.map((line, i) => (
                <div key={i} style={{ color:
                  line.type === 'cmd'    ? (isDark ? '#111827' : '#f3f4f6') :
                  line.type === 'ok'    ? (isDark ? '#16a34a' : '#4ade80') :
                  line.type === 'result'? (isDark ? '#ea580c' : '#fde047') :
                                          (isDark ? '#6b7280' : '#9ca3af')
                }} className={line.type === 'cmd' || line.type === 'result' ? 'font-semibold' : ''}>
                  {line.text}
                </div>
              ))}
              <div style={{ color: isDark ? '#d1d5db' : '#4b5563' }} className="mt-3">█</div>
            </div>
          </div>
        </div>
      </div>

      {/* ── How it works ─────────────────────────────────────────── */}
      <div className="border-t border-gray-800 bg-gray-900 py-14">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-xl font-bold text-gray-100 mb-2 text-center">How it works</h2>
          <p className="text-xs text-gray-500 text-center mb-10">Study in the browser — execute with the CLI</p>
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
            {attackLayers.map(({ Icon, label, attacks }) => (
              <div
                key={label}
                className="bg-gray-900 border border-gray-700 rounded-xl p-4 hover:border-green-600 transition-colors"
              >
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-7 h-7 rounded-md bg-green-950 border border-green-800 flex items-center justify-center flex-shrink-0">
                    <Icon className="w-3.5 h-3.5 text-green-400" />
                  </div>
                  <span className="text-xs font-bold text-gray-100">{label}</span>
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
            Free for education & research · private distribution
          </div>
          <h2 className="text-2xl font-bold text-gray-100 mb-3">Get the mag CLI</h2>
          <p className="text-gray-400 text-sm mb-6">
            The web interface is open to everyone. The <MagKeyword /> CLI — usable by humans and AI agents alike — is distributed privately to prevent misuse. Email us with your name, org, and intended use (course, research, pentest engagement, or agentic workflow).
          </p>
          <a
            href="mailto:contact@montimage.eu?subject=mag CLI access request"
            className="inline-flex items-center gap-2 bg-green-600 text-white border border-green-500 px-7 py-3 rounded-xl font-bold text-sm shadow-custom-md hover:bg-green-500 hover:shadow-custom-lg hover:-translate-y-0.5 transition-all duration-200"
          >
            Request CLI access
            <ArrowRight className="w-4 h-4" />
          </a>
          <p className="text-xs text-gray-600 mt-4">contact@montimage.eu · subject: mag CLI access request</p>
          <p className="text-xs text-gray-600 mt-3">
            Bug reports & feature requests →{' '}
            <a
              href="https://github.com/Montimage/mmt-attacker/issues"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-500 hover:text-gray-400 underline underline-offset-2 transition-colors"
            >
              GitHub Issues
            </a>
          </p>
        </div>
      </div>

    </div>
  )
}

export default HeroSection
