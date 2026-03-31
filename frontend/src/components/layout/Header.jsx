import { Link, useLocation, useNavigate } from 'react-router-dom'
import { Menu, X, Github, Search, Grid, Terminal } from 'lucide-react'
import { useState } from 'react'

function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [searchOpen, setSearchOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const location = useLocation()
  const navigate = useNavigate()

  const isActive = (path) => location.pathname === path

  const handleSearch = (e) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      navigate(`/browse?search=${encodeURIComponent(searchQuery.trim())}`)
      setSearchOpen(false)
      setSearchQuery('')
    }
  }

  return (
    <header className="sticky top-0 z-50 bg-slate-900 border-b border-slate-700 shadow-custom-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and branding */}
          <Link
            to="/"
            className="flex items-center space-x-3 group"
          >
            <img
              src="/logo.svg"
              alt="MMT-Attacker Logo"
              className="h-9 w-auto object-contain group-hover:opacity-80 transition-opacity duration-200"
            />
            <div className="flex flex-col">
              <span className="text-lg font-bold text-white group-hover:text-green-400 transition-colors">
                MMT-Attacker
              </span>
              <span className="text-xs font-medium text-slate-400 hidden sm:block">
                Demo Platform
              </span>
            </div>
          </Link>

          {/* Desktop navigation */}
          <nav className="hidden md:flex items-center space-x-2">
            <Link
              to="/browse"
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium text-sm transition-all duration-200 ${
                isActive('/browse')
                  ? 'bg-green-600 text-white shadow-custom-md'
                  : 'text-slate-300 hover:text-white hover:bg-slate-800'
              }`}
            >
              <Grid className="w-4 h-4" />
              <span>Attacks</span>
            </Link>

            <button
              onClick={() => setSearchOpen(!searchOpen)}
              className="flex items-center space-x-2 px-4 py-2 rounded-lg font-medium text-sm text-slate-300 hover:text-white hover:bg-slate-800 transition-all duration-200"
            >
              <Search className="w-4 h-4" />
              <span>Search</span>
            </button>

            <a
              href="https://github.com/montimage/mmt-attacker"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-2 px-4 py-2 rounded-lg font-medium text-sm text-slate-300 hover:text-white hover:bg-slate-800 transition-all duration-200"
              title="View on GitHub"
            >
              <Github className="w-4 h-4" />
              <span>GitHub</span>
            </a>

            <div className="flex items-center space-x-1 ml-2 px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700">
              <Terminal className="w-3.5 h-3.5 text-green-400" />
              <code className="text-xs text-green-400 font-mono">matcha</code>
            </div>
          </nav>

          {/* Mobile menu button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 transition-all duration-200"
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? (
              <X className="w-5 h-5" />
            ) : (
              <Menu className="w-5 h-5" />
            )}
          </button>
        </div>

        {/* Search Bar (Desktop) */}
        {searchOpen && (
          <div className="hidden md:block py-3 border-t border-slate-700 animate-fade-in">
            <form onSubmit={handleSearch} className="relative max-w-2xl mx-auto">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <Search className="w-4 h-4 text-slate-400" />
              </div>
              <input
                type="text"
                placeholder="Search for attacks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                autoFocus
                className="w-full pl-11 pr-10 py-2.5 text-sm border border-slate-600 rounded-lg focus:outline-none focus:border-green-500 focus:ring-1 focus:ring-green-500 transition-all bg-slate-800 text-white placeholder-slate-400"
              />
              <button
                type="button"
                onClick={() => setSearchOpen(false)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-white transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </form>
          </div>
        )}

        {/* Mobile navigation */}
        {mobileMenuOpen && (
          <nav className="md:hidden py-3 border-t border-slate-700 animate-fade-in">
            <div className="flex flex-col space-y-1">
              <Link
                to="/browse"
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center space-x-3 px-4 py-2.5 rounded-lg font-medium text-sm transition-all duration-200 ${
                  isActive('/browse')
                    ? 'bg-green-600 text-white'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800'
                }`}
              >
                <Grid className="w-4 h-4" />
                <span>Attacks</span>
              </Link>

              <div className="px-4 py-2">
                <form onSubmit={handleSearch} className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Search className="w-4 h-4 text-slate-400" />
                  </div>
                  <input
                    type="text"
                    placeholder="Search attacks..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 text-sm border border-slate-600 rounded-lg focus:outline-none focus:border-green-500 bg-slate-800 text-white placeholder-slate-400"
                  />
                </form>
              </div>

              <a
                href="https://github.com/montimage/mmt-attacker"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center space-x-3 px-4 py-2.5 rounded-lg font-medium text-sm text-slate-300 hover:text-white hover:bg-slate-800 transition-all duration-200"
              >
                <Github className="w-4 h-4" />
                <span>View on GitHub</span>
              </a>
            </div>
          </nav>
        )}
      </div>
    </header>
  )
}

export default Header
