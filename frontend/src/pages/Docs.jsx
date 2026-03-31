import { useState } from 'react'
import { Link } from 'react-router-dom'
import {
  ArrowLeft,
  Terminal,
  Download,
  Package,
  BookOpen,
  Shield,
  Layers,
  ChevronRight,
  ChevronDown,
  Copy,
  Check,
  Network,
  Globe,
  Repeat,
  AlertTriangle,
  Container,
  Zap,
} from 'lucide-react'

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function CodeBlock({ code, language = 'bash' }) {
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="relative group my-4">
      <div className="flex items-center justify-between bg-gray-800 rounded-t-lg px-4 py-2 border-b border-gray-700">
        <span className="text-xs font-mono text-gray-400">{language}</span>
        <button
          onClick={handleCopy}
          className="flex items-center space-x-1 text-xs text-gray-400 hover:text-white transition-colors"
          title="Copy to clipboard"
        >
          {copied ? (
            <>
              <Check className="w-3.5 h-3.5 text-green-400" />
              <span className="text-green-400">Copied!</span>
            </>
          ) : (
            <>
              <Copy className="w-3.5 h-3.5" />
              <span>Copy</span>
            </>
          )}
        </button>
      </div>
      <pre className="bg-gray-900 rounded-b-lg p-4 overflow-x-auto text-sm">
        <code className="text-green-300 font-mono whitespace-pre">{code}</code>
      </pre>
    </div>
  )
}

function Section({ id, icon: Icon, title, children }) {
  return (
    <section id={id} className="mb-12 scroll-mt-24">
      <div className="flex items-center space-x-3 mb-6">
        <div className="flex items-center justify-center w-10 h-10 bg-black rounded-lg flex-shrink-0">
          <Icon className="w-5 h-5 text-white" />
        </div>
        <h2 className="text-2xl font-bold text-black">{title}</h2>
      </div>
      {children}
    </section>
  )
}

function Subsection({ title, children }) {
  return (
    <div className="mb-8">
      <h3 className="text-lg font-bold text-black mb-3 flex items-center space-x-2">
        <ChevronRight className="w-4 h-4 text-green-600" />
        <span>{title}</span>
      </h3>
      {children}
    </div>
  )
}

function Card({ children, className = '' }) {
  return (
    <div className={`bg-white border-2 border-gray-200 rounded-lg p-6 shadow-sm ${className}`}>
      {children}
    </div>
  )
}

function NoteCard({ type = 'info', children }) {
  const styles = {
    info: 'bg-blue-50 border-blue-300 text-blue-800',
    warning: 'bg-yellow-50 border-yellow-400 text-yellow-800',
    danger: 'bg-red-50 border-red-400 text-red-800',
    tip: 'bg-green-50 border-green-400 text-green-800',
  }
  const labels = { info: 'Note', warning: 'Warning', danger: 'Important', tip: 'Tip' }

  return (
    <div className={`border-l-4 rounded-r-lg px-5 py-4 my-4 ${styles[type]}`}>
      <p className="text-sm font-bold mb-1">{labels[type]}</p>
      <div className="text-sm">{children}</div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Sidebar nav items
// ---------------------------------------------------------------------------

const NAV_ITEMS = [
  { id: 'overview', label: 'Overview', icon: BookOpen },
  { id: 'installation', label: 'Installation', icon: Download },
  { id: 'quickstart', label: 'Quick Start', icon: Zap },
  { id: 'cli-reference', label: 'CLI Reference', icon: Terminal },
  { id: 'attacks', label: 'Attack Catalogue', icon: Shield },
  { id: 'docker', label: 'Docker Lab', icon: Container },
  { id: 'completions', label: 'Shell Completions', icon: Package },
]

// ---------------------------------------------------------------------------
// Attack catalogue data
// ---------------------------------------------------------------------------

const NETWORK_ATTACKS = [
  { cmd: 'arp-spoof', desc: 'ARP spoofing / Man-in-the-Middle setup', params: '--target-ip <IP> --gateway-ip <IP>' },
  { cmd: 'bgp-hijacking', desc: 'BGP route hijacking simulation', params: '--target-prefix <CIDR>' },
  { cmd: 'dhcp-starvation', desc: 'DHCP pool exhaustion', params: '--interface <IF>' },
  { cmd: 'dns-amplification', desc: 'DNS amplification DDoS', params: '--target-ip <IP>' },
  { cmd: 'icmp-flood', desc: 'ICMP ping flood', params: '--target-ip <IP> --count <N>' },
  { cmd: 'mac-flooding', desc: 'Switch CAM table overflow', params: '--interface <IF> --count <N>' },
  { cmd: 'mitm', desc: 'Man-in-the-Middle traffic interception', params: '--target-ip <IP> --gateway-ip <IP>' },
  { cmd: 'ntp-amplification', desc: 'NTP amplification DDoS', params: '--target-ip <IP>' },
  { cmd: 'ping-of-death', desc: 'Oversized ICMP packet attack', params: '--target-ip <IP>' },
  { cmd: 'smurf-attack', desc: 'ICMP broadcast amplification', params: '--target-ip <IP>' },
  { cmd: 'syn-flood', desc: 'TCP SYN flood attack', params: '--target-ip <IP> --target-port <PORT> --count <N>' },
  { cmd: 'udp-flood', desc: 'UDP packet flooding', params: '--target-ip <IP> --target-port <PORT> --count <N>' },
]

const APP_ATTACKS = [
  { cmd: 'credential-harvester', desc: 'Phishing / credential capture page', params: '--interface <IF> --port <PORT>' },
  { cmd: 'directory-traversal', desc: 'File system path traversal', params: '--target-url <URL>' },
  { cmd: 'ftp-brute-force', desc: 'FTP credential brute-force', params: '--target-ip <IP> --username <USER> --passwords <FILE>' },
  { cmd: 'http-dos', desc: 'Malformed HTTP Denial-of-Service', params: '--target-url <URL> --num-connections <N>' },
  { cmd: 'http-flood', desc: 'High-volume HTTP request flood', params: '--target-url <URL> --count <N>' },
  { cmd: 'rdp-brute-force', desc: 'RDP credential brute-force', params: '--target-ip <IP> --username <USER> --passwords <FILE>' },
  { cmd: 'slowloris', desc: 'Slow HTTP connection exhaustion', params: '--target-ip <IP> --target-port <PORT> --sockets <N>' },
  { cmd: 'sql-injection', desc: 'SQL injection vulnerability test', params: '--target-url <URL>' },
  { cmd: 'ssh-brute-force', desc: 'SSH credential brute-force', params: '--target-ip <IP> --username <USER> --passwords <FILE>' },
  { cmd: 'ssl-strip', desc: 'HTTPS downgrade (SSLstrip) attack', params: '--interface <IF>' },
  { cmd: 'vlan-hopping', desc: 'VLAN double-encapsulation exploit', params: '--interface <IF> --target-vlan <ID>' },
  { cmd: 'xss', desc: 'Cross-site scripting injection test', params: '--target-url <URL> --payload <STRING>' },
  { cmd: 'xxe', desc: 'XML External Entity injection test', params: '--target-url <URL>' },
]

const REPLAY_ATTACKS = [
  { cmd: 'pcap-replay', desc: 'Replay captured PCAP traffic at configurable speed', params: '--pcap-file <FILE> --interface <IF> --rate <MULTIPLIER>' },
]

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

function Docs() {
  const [activeSection, setActiveSection] = useState('overview')
  const [expandedCategories, setExpandedCategories] = useState({ network: true, app: true, replay: true })

  const scrollTo = (id) => {
    const el = document.getElementById(id)
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' })
      setActiveSection(id)
    }
  }

  const toggleCategory = (key) =>
    setExpandedCategories((prev) => ({ ...prev, [key]: !prev[key] }))

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back Button */}
      <Link
        to="/"
        className="inline-flex items-center space-x-2 text-gray-600 hover:text-green-900 mb-6 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span className="font-medium">Back to Home</span>
      </Link>

      {/* Page header */}
      <div className="mb-10">
        <h1 className="text-4xl md:text-5xl font-bold text-black mb-3">Documentation</h1>
        <p className="text-lg text-gray-600 max-w-3xl">
          Everything you need to install, configure, and use <code className="font-mono text-green-700 bg-green-50 px-1.5 py-0.5 rounded border border-green-200">matcha</code> — the MMT-Attacker CLI.
        </p>
      </div>

      <div className="flex gap-8">
        {/* ------------------------------------------------------------------ */}
        {/* Sidebar */}
        {/* ------------------------------------------------------------------ */}
        <aside className="hidden lg:block w-56 flex-shrink-0">
          <nav className="sticky top-24 space-y-1">
            {NAV_ITEMS.map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                onClick={() => scrollTo(id)}
                className={`w-full flex items-center space-x-2.5 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                  activeSection === id
                    ? 'bg-black text-white'
                    : 'text-gray-600 hover:text-black hover:bg-gray-100'
                }`}
              >
                <Icon className="w-4 h-4 flex-shrink-0" />
                <span>{label}</span>
              </button>
            ))}
          </nav>
        </aside>

        {/* ------------------------------------------------------------------ */}
        {/* Main content */}
        {/* ------------------------------------------------------------------ */}
        <main className="flex-1 min-w-0">

          {/* ================================================================ */}
          {/* OVERVIEW */}
          {/* ================================================================ */}
          <Section id="overview" icon={BookOpen} title="Overview">
            <Card className="mb-6">
              <p className="text-gray-700 leading-relaxed mb-4">
                <strong>MMT-Attacker</strong> is an open-source network attack simulation toolkit built by{' '}
                <a href="https://www.montimage.eu" target="_blank" rel="noopener noreferrer" className="text-green-700 hover:underline font-medium">Montimage</a>.
                It provides a single CLI tool called <code className="font-mono bg-gray-100 px-1 rounded">matcha</code> that
                lets security professionals, researchers, and students simulate <strong>26 different attacks</strong> across
                three categories — all in isolated, authorized lab environments.
              </p>
              <p className="text-gray-700 leading-relaxed">
                The goal is to teach <em>how</em> attacks work, not just that they exist, so defenders can build
                more effective countermeasures.
              </p>
            </Card>

            <div className="grid md:grid-cols-3 gap-4 mb-6">
              <Card className="text-center">
                <Network className="w-8 h-8 text-black mx-auto mb-2" />
                <p className="text-2xl font-bold text-black">12</p>
                <p className="text-sm text-gray-600 font-medium">Network-layer attacks</p>
              </Card>
              <Card className="text-center">
                <Globe className="w-8 h-8 text-black mx-auto mb-2" />
                <p className="text-2xl font-bold text-black">13</p>
                <p className="text-sm text-gray-600 font-medium">Application-layer attacks</p>
              </Card>
              <Card className="text-center">
                <Repeat className="w-8 h-8 text-black mx-auto mb-2" />
                <p className="text-2xl font-bold text-black">1</p>
                <p className="text-sm text-gray-600 font-medium">Replay attack</p>
              </Card>
            </div>

            <NoteCard type="warning">
              <strong>Authorized use only.</strong> MMT-Attacker is designed strictly for use on networks and systems
              you own or have explicit written permission to test. Unauthorized use is illegal and unethical.
            </NoteCard>
          </Section>

          {/* ================================================================ */}
          {/* INSTALLATION */}
          {/* ================================================================ */}
          <Section id="installation" icon={Download} title="Installation">
            <Subsection title="Requirements">
              <ul className="list-disc list-inside text-gray-700 space-y-1 text-sm">
                <li>Python 3.8 or later</li>
                <li><code className="font-mono bg-gray-100 px-1 rounded">libpcap</code> (required by Scapy for raw socket support)</li>
                <li>Root / Administrator privileges for most attacks (raw sockets)</li>
              </ul>
            </Subsection>

            <Subsection title="Option 1 — pip (recommended)">
              <CodeBlock code="pip install mmt-attacker" />
              <NoteCard type="tip">
                Use a virtual environment to avoid dependency conflicts:{' '}
                <code className="font-mono">python -m venv .venv &amp;&amp; source .venv/bin/activate</code>
              </NoteCard>
            </Subsection>

            <Subsection title="Option 2 — One-line installer (Linux / macOS)">
              <p className="text-sm text-gray-600 mb-2">
                Automatically detects your OS and package manager, installs system dependencies, then installs from PyPI (falls back to GitHub source).
              </p>
              <CodeBlock code={`curl -sSL https://raw.githubusercontent.com/Montimage/mmt-attacker/main/install.sh | bash
# or with wget
wget -qO- https://raw.githubusercontent.com/Montimage/mmt-attacker/main/install.sh | bash`} />
            </Subsection>

            <Subsection title="Option 3 — From source">
              <CodeBlock code={`git clone https://github.com/Montimage/mmt-attacker.git
cd mmt-attacker
pip install -e .`} />
            </Subsection>

            <Subsection title="Option 4 — Docker">
              <p className="text-sm text-gray-600 mb-2">
                Run matcha in an isolated container without any local Python setup.
              </p>
              <CodeBlock code={`docker build -t matcha .
docker run --rm --cap-add NET_ADMIN --cap-add NET_RAW matcha --help`} />
              <NoteCard type="info">
                See the <button onClick={() => scrollTo('docker')} className="underline text-blue-700 hover:text-blue-900 font-medium">Docker Lab</button> section for a full two-container attacker/target environment.
              </NoteCard>
            </Subsection>

            <Subsection title="Verify the installation">
              <CodeBlock code={`matcha --version
matcha list`} />
            </Subsection>
          </Section>

          {/* ================================================================ */}
          {/* QUICK START */}
          {/* ================================================================ */}
          <Section id="quickstart" icon={Zap} title="Quick Start">
            <p className="text-gray-700 mb-4">
              After installation, three commands get you oriented:
            </p>

            <Subsection title="List all attacks">
              <CodeBlock code={`# Human-readable table
matcha list

# Machine-readable JSON
matcha list -o json`} />
            </Subsection>

            <Subsection title="Inspect a specific attack">
              <CodeBlock code={`matcha info syn-flood
matcha info ssh-brute-force`} />
            </Subsection>

            <Subsection title="Run your first attack (SYN flood example)">
              <NoteCard type="danger">
                Only run this against systems you own or have authorization to test.
                The target must be reachable from your machine and on an isolated network.
              </NoteCard>
              <CodeBlock code={`# Basic SYN flood — 500 packets to a local test server
sudo matcha syn-flood --target-ip 192.168.56.10 --target-port 80 --count 500

# Verbose output with debug logging
sudo matcha -v syn-flood --target-ip 192.168.56.10 --target-port 80 --count 500

# JSON output (useful for scripting / logging)
sudo matcha -o json syn-flood --target-ip 192.168.56.10 --target-port 80 --count 500`} />
            </Subsection>

            <Subsection title="PCAP replay">
              <CodeBlock code={`# Replay a capture file at 2× original speed
sudo matcha pcap-replay --pcap-file capture.pcap --interface eth0 --rate 2.0`} />
            </Subsection>
          </Section>

          {/* ================================================================ */}
          {/* CLI REFERENCE */}
          {/* ================================================================ */}
          <Section id="cli-reference" icon={Terminal} title="CLI Reference">
            <Subsection title="Global options">
              <div className="overflow-x-auto">
                <table className="w-full text-sm border-collapse">
                  <thead>
                    <tr className="bg-gray-100 text-left">
                      <th className="border border-gray-200 px-4 py-2 font-semibold text-black">Flag</th>
                      <th className="border border-gray-200 px-4 py-2 font-semibold text-black">Description</th>
                      <th className="border border-gray-200 px-4 py-2 font-semibold text-black">Default</th>
                    </tr>
                  </thead>
                  <tbody>
                    {[
                      ['-v, --verbose', 'Enable debug-level logging', 'off'],
                      ['-o, --output [text|json]', 'Output format', 'text'],
                      ['--no-color', 'Disable ANSI colour codes', 'off'],
                      ['--version', 'Print version and exit', '—'],
                      ['--help', 'Show help message and exit', '—'],
                    ].map(([flag, desc, def_]) => (
                      <tr key={flag} className="hover:bg-gray-50">
                        <td className="border border-gray-200 px-4 py-2 font-mono text-green-700 text-xs">{flag}</td>
                        <td className="border border-gray-200 px-4 py-2 text-gray-700">{desc}</td>
                        <td className="border border-gray-200 px-4 py-2 text-gray-500">{def_}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Subsection>

            <Subsection title="Built-in commands">
              <div className="space-y-4">
                {[
                  {
                    cmd: 'matcha list',
                    desc: 'Print all registered attacks grouped by category.',
                    example: 'matcha list\nmatcha list -o json',
                  },
                  {
                    cmd: 'matcha info <attack>',
                    desc: 'Show detailed metadata for a single attack: description, category, and all accepted parameters.',
                    example: 'matcha info syn-flood\nmatcha info pcap-replay -o json',
                  },
                  {
                    cmd: 'matcha completions <shell>',
                    desc: 'Generate a shell completion script. Supported shells: bash, zsh, fish.',
                    example: 'matcha completions bash >> ~/.bash_completion\nmatcha completions zsh >> ~/.zsh_completion',
                  },
                  {
                    cmd: 'matcha <attack> [OPTIONS]',
                    desc: 'Execute the named attack. Each attack exposes its own set of options — use --help on any attack for the full parameter list.',
                    example: 'matcha syn-flood --help\nmatcha ssh-brute-force --help',
                  },
                ].map(({ cmd, desc, example }) => (
                  <Card key={cmd} className="!p-4">
                    <code className="text-sm font-mono text-green-700 font-bold">{cmd}</code>
                    <p className="text-sm text-gray-700 mt-1 mb-2">{desc}</p>
                    <CodeBlock code={example} />
                  </Card>
                ))}
              </div>
            </Subsection>
          </Section>

          {/* ================================================================ */}
          {/* ATTACK CATALOGUE */}
          {/* ================================================================ */}
          <Section id="attacks" icon={Shield} title="Attack Catalogue">
            <p className="text-gray-700 mb-6">
              All 26 attacks are listed below with their CLI command and required parameters.
              Run <code className="font-mono bg-gray-100 px-1 rounded text-sm">matcha &lt;attack&gt; --help</code> for the full parameter list of any attack.
            </p>

            {/* Network layer */}
            <div className="mb-4">
              <button
                onClick={() => toggleCategory('network')}
                className="w-full flex items-center justify-between bg-gray-900 text-white px-5 py-3 rounded-lg font-semibold hover:bg-gray-800 transition-colors"
              >
                <div className="flex items-center space-x-2">
                  <Network className="w-4 h-4" />
                  <span>Network-layer attacks (12)</span>
                </div>
                {expandedCategories.network ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
              </button>
              {expandedCategories.network && (
                <div className="overflow-x-auto border border-t-0 border-gray-200 rounded-b-lg">
                  <table className="w-full text-sm border-collapse">
                    <thead>
                      <tr className="bg-gray-50 text-left">
                        <th className="px-4 py-2 font-semibold text-black border-b border-gray-200">Command</th>
                        <th className="px-4 py-2 font-semibold text-black border-b border-gray-200">Description</th>
                        <th className="px-4 py-2 font-semibold text-black border-b border-gray-200 hidden md:table-cell">Key Parameters</th>
                      </tr>
                    </thead>
                    <tbody>
                      {NETWORK_ATTACKS.map((a) => (
                        <tr key={a.cmd} className="hover:bg-gray-50 border-b border-gray-100 last:border-0">
                          <td className="px-4 py-2.5 font-mono text-green-700 font-medium whitespace-nowrap">{a.cmd}</td>
                          <td className="px-4 py-2.5 text-gray-700">{a.desc}</td>
                          <td className="px-4 py-2.5 font-mono text-xs text-gray-500 hidden md:table-cell whitespace-nowrap">{a.params}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>

            {/* Application layer */}
            <div className="mb-4">
              <button
                onClick={() => toggleCategory('app')}
                className="w-full flex items-center justify-between bg-gray-900 text-white px-5 py-3 rounded-lg font-semibold hover:bg-gray-800 transition-colors"
              >
                <div className="flex items-center space-x-2">
                  <Globe className="w-4 h-4" />
                  <span>Application-layer attacks (13)</span>
                </div>
                {expandedCategories.app ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
              </button>
              {expandedCategories.app && (
                <div className="overflow-x-auto border border-t-0 border-gray-200 rounded-b-lg">
                  <table className="w-full text-sm border-collapse">
                    <thead>
                      <tr className="bg-gray-50 text-left">
                        <th className="px-4 py-2 font-semibold text-black border-b border-gray-200">Command</th>
                        <th className="px-4 py-2 font-semibold text-black border-b border-gray-200">Description</th>
                        <th className="px-4 py-2 font-semibold text-black border-b border-gray-200 hidden md:table-cell">Key Parameters</th>
                      </tr>
                    </thead>
                    <tbody>
                      {APP_ATTACKS.map((a) => (
                        <tr key={a.cmd} className="hover:bg-gray-50 border-b border-gray-100 last:border-0">
                          <td className="px-4 py-2.5 font-mono text-green-700 font-medium whitespace-nowrap">{a.cmd}</td>
                          <td className="px-4 py-2.5 text-gray-700">{a.desc}</td>
                          <td className="px-4 py-2.5 font-mono text-xs text-gray-500 hidden md:table-cell whitespace-nowrap">{a.params}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>

            {/* Replay */}
            <div className="mb-4">
              <button
                onClick={() => toggleCategory('replay')}
                className="w-full flex items-center justify-between bg-gray-900 text-white px-5 py-3 rounded-lg font-semibold hover:bg-gray-800 transition-colors"
              >
                <div className="flex items-center space-x-2">
                  <Repeat className="w-4 h-4" />
                  <span>Replay attacks (1)</span>
                </div>
                {expandedCategories.replay ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
              </button>
              {expandedCategories.replay && (
                <div className="overflow-x-auto border border-t-0 border-gray-200 rounded-b-lg">
                  <table className="w-full text-sm border-collapse">
                    <thead>
                      <tr className="bg-gray-50 text-left">
                        <th className="px-4 py-2 font-semibold text-black border-b border-gray-200">Command</th>
                        <th className="px-4 py-2 font-semibold text-black border-b border-gray-200">Description</th>
                        <th className="px-4 py-2 font-semibold text-black border-b border-gray-200 hidden md:table-cell">Key Parameters</th>
                      </tr>
                    </thead>
                    <tbody>
                      {REPLAY_ATTACKS.map((a) => (
                        <tr key={a.cmd} className="hover:bg-gray-50 border-b border-gray-100 last:border-0">
                          <td className="px-4 py-2.5 font-mono text-green-700 font-medium whitespace-nowrap">{a.cmd}</td>
                          <td className="px-4 py-2.5 text-gray-700">{a.desc}</td>
                          <td className="px-4 py-2.5 font-mono text-xs text-gray-500 hidden md:table-cell whitespace-nowrap">{a.params}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </Section>

          {/* ================================================================ */}
          {/* DOCKER LAB */}
          {/* ================================================================ */}
          <Section id="docker" icon={Container} title="Docker Lab">
            <p className="text-gray-700 mb-4">
              The repository ships a <code className="font-mono bg-gray-100 px-1 rounded text-sm">docker-compose.yml</code> that
              spins up a ready-made two-container lab: an <strong>attacker</strong> container with matcha pre-installed and
              a <strong>target</strong> container running nginx, OpenSSH, and vsftpd.
            </p>

            <NoteCard type="tip">
              The two containers share an isolated bridge network called <code className="font-mono">lab</code>.
              Inside the attacker container the target is reachable at hostname <code className="font-mono">target</code>.
            </NoteCard>

            <Subsection title="Start the lab">
              <CodeBlock code={`# Build images and start both containers in the background
docker compose up --build -d

# Check that both containers are running
docker compose ps`} />
            </Subsection>

            <Subsection title="Run an attack from the attacker container">
              <CodeBlock code={`# Open a shell in the attacker container
docker compose exec attacker bash

# Then run any matcha attack — the target hostname resolves automatically
matcha syn-flood --target-ip target --target-port 80 --count 200
matcha ssh-brute-force --target-ip target --username admin --passwords /wordlists/common.txt`} />
            </Subsection>

            <Subsection title="Standalone Docker (no Compose)">
              <CodeBlock code={`# Build just the attacker image
docker build -t matcha .

# Run an attack directly
docker run --rm --cap-add NET_ADMIN --cap-add NET_RAW matcha \\
  syn-flood --target-ip 192.168.1.10 --target-port 80 --count 100`} />
              <NoteCard type="warning">
                The <code className="font-mono">NET_ADMIN</code> and <code className="font-mono">NET_RAW</code> capabilities
                are required for attacks that craft raw packets (Scapy). Without them the attack will fail with a permission error.
              </NoteCard>
            </Subsection>

            <Subsection title="Stop and clean up">
              <CodeBlock code={`docker compose down
# Remove images as well
docker compose down --rmi all`} />
            </Subsection>
          </Section>

          {/* ================================================================ */}
          {/* SHELL COMPLETIONS */}
          {/* ================================================================ */}
          <Section id="completions" icon={Package} title="Shell Completions">
            <p className="text-gray-700 mb-4">
              matcha can generate tab-completion scripts for Bash, Zsh, and Fish so you can auto-complete
              attack names and flags without memorising them.
            </p>

            <Subsection title="Bash">
              <CodeBlock code={`# Generate and persist the completion script
matcha completions bash >> ~/.bash_completion

# Reload your shell (or open a new terminal)
source ~/.bash_completion`} />
            </Subsection>

            <Subsection title="Zsh">
              <CodeBlock code={`# Ensure completions directory exists
mkdir -p ~/.zsh/completions

# Write the completion script
matcha completions zsh >> ~/.zsh/completions/_matcha

# Add to your ~/.zshrc if not already present
echo 'fpath=(~/.zsh/completions $fpath)' >> ~/.zshrc
echo 'autoload -Uz compinit && compinit' >> ~/.zshrc

# Reload
source ~/.zshrc`} />
            </Subsection>

            <Subsection title="Fish">
              <CodeBlock code={`matcha completions fish > ~/.config/fish/completions/matcha.fish`} />
            </Subsection>

            <NoteCard type="tip">
              After installing completions, type <code className="font-mono">matcha </code> and press <kbd className="bg-gray-100 border border-gray-300 rounded px-1.5 py-0.5 text-xs font-mono">Tab</kbd> to see all available attack commands.
            </NoteCard>
          </Section>

          {/* ================================================================ */}
          {/* Ethical use reminder */}
          {/* ================================================================ */}
          <div className="border-2 border-red-300 bg-red-50 rounded-lg p-6 mb-8">
            <div className="flex items-start space-x-3">
              <AlertTriangle className="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-bold text-red-800 mb-2">Ethical &amp; Legal Reminder</h3>
                <p className="text-sm text-red-700 leading-relaxed">
                  MMT-Attacker is an educational and research tool. Always obtain <strong>explicit written
                  authorization</strong> before running any attack against systems or networks you do not own.
                  Unauthorized use may violate local and international laws. Montimage accepts no liability
                  for misuse of this software.
                </p>
              </div>
            </div>
          </div>

          {/* ================================================================ */}
          {/* Footer links */}
          {/* ================================================================ */}
          <div className="flex flex-wrap gap-4 pt-6 border-t-2 border-gray-200">
            <a
              href="https://github.com/Montimage/mmt-attacker"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center space-x-2 bg-black text-white px-5 py-2.5 rounded-lg font-semibold text-sm hover:bg-gray-800 transition-colors"
            >
              <Layers className="w-4 h-4" />
              <span>View on GitHub</span>
            </a>
            <Link
              to="/browse"
              className="inline-flex items-center space-x-2 bg-white border-2 border-gray-300 text-gray-700 px-5 py-2.5 rounded-lg font-semibold text-sm hover:border-black hover:text-black transition-colors"
            >
              <Shield className="w-4 h-4" />
              <span>Browse Attacks</span>
            </Link>
            <Link
              to="/about"
              className="inline-flex items-center space-x-2 bg-white border-2 border-gray-300 text-gray-700 px-5 py-2.5 rounded-lg font-semibold text-sm hover:border-black hover:text-black transition-colors"
            >
              <BookOpen className="w-4 h-4" />
              <span>About</span>
            </Link>
          </div>
        </main>
      </div>
    </div>
  )
}

export default Docs
