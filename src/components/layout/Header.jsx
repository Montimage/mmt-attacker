import { Link, useLocation, useNavigate } from 'react-router-dom'
import { Menu, X, Github, Search, Grid, Terminal, BookOpen, Sun, Moon } from 'lucide-react'
import { useState } from 'react'
import { useTheme } from '../../context/ThemeContext'

function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [searchOpen, setSearchOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const location = useLocation()
  const navigate = useNavigate()
  const { isDark, toggleTheme } = useTheme()

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
    <header className="sticky top-0 z-50 bg-gray-900 border-b-2 border-gray-700 shadow-custom">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and branding */}
          <Link
            to="/"
            className="flex items-center space-x-3 group"
          >
            <img
              src="/logo.svg"
              alt="MAG Logo"
              className="h-9 w-auto object-contain group-hover:opacity-80 transition-opacity duration-200"
            />
            <div className="flex flex-col">
              <span className="text-lg font-bold text-gray-100 group-hover:text-green-400 transition-colors">
                MAG
              </span>
              <span className="text-xs font-medium text-gray-400 hidden sm:block">
                Montimage Attack Generator
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
                  : 'text-gray-300 hover:text-gray-100 hover:bg-gray-800'
              }`}
            >
              <Grid className="w-4 h-4" />
              <span>Attacks</span>
            </Link>

            <Link
              to="/docs"
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium text-sm transition-all duration-200 ${
                isActive('/docs')
                  ? 'bg-green-600 text-white shadow-custom-md'
                  : 'text-gray-300 hover:text-gray-100 hover:bg-gray-800'
              }`}
            >
              <BookOpen className="w-4 h-4" />
              <span>Docs</span>
            </Link>

            <button
              onClick={() => setSearchOpen(!searchOpen)}
              className="flex items-center space-x-2 px-4 py-2 rounded-lg font-medium text-sm text-gray-300 hover:text-gray-100 hover:bg-gray-800 transition-all duration-200"
            >
              <Search className="w-4 h-4" />
              <span>Search</span>
            </button>

            <a
              href="https://github.com/montimage/mmt-attacker"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-2 px-4 py-2 rounded-lg font-medium text-sm text-gray-300 hover:text-gray-100 hover:bg-gray-800 transition-all duration-200"
              title="View on GitHub"
            >
              <Github className="w-4 h-4" />
              <span>GitHub</span>
            </a>

            <div className="flex items-center space-x-1 ml-2 px-3 py-1.5 rounded-lg bg-gray-800 border border-gray-600">
              <Terminal className="w-3.5 h-3.5 text-green-500" />
              <code className="text-xs text-green-400 font-mono font-semibold">mag</code>
            </div>

            {/* Theme toggle */}
            <button
              onClick={toggleTheme}
              className="ml-1 p-2 rounded-lg text-gray-400 hover:text-gray-100 hover:bg-gray-800 transition-all duration-200"
              aria-label="Toggle theme"
              title={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
            >
              {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </button>
          </nav>

          {/* Mobile: theme toggle + menu button */}
          <div className="md:hidden flex items-center space-x-1">
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg text-gray-400 hover:text-gray-100 hover:bg-gray-800 transition-all duration-200"
              aria-label="Toggle theme"
            >
              {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-gray-400 hover:text-gray-100 hover:bg-gray-800 transition-all duration-200"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? (
                <X className="w-5 h-5" />
              ) : (
                <Menu className="w-5 h-5" />
              )}
            </button>
          </div>
        </div>

        {/* Search Bar (Desktop) */}
        {searchOpen && (
          <div className="hidden md:block py-3 border-t border-gray-700 animate-fade-in">
            <form onSubmit={handleSearch} className="relative max-w-2xl mx-auto">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <Search className="w-4 h-4 text-gray-500" />
              </div>
              <input
                type="text"
                placeholder="Search for attacks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                autoFocus
                className="w-full pl-11 pr-10 py-2.5 text-sm border-2 border-gray-600 rounded-lg focus:outline-none focus:border-green-500 focus:ring-1 focus:ring-green-500 transition-all bg-gray-800 text-gray-100 placeholder-gray-500"
              />
              <button
                type="button"
                onClick={() => setSearchOpen(false)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-500 hover:text-gray-300 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </form>
          </div>
        )}

        {/* Mobile navigation */}
        {mobileMenuOpen && (
          <nav className="md:hidden py-3 border-t border-gray-700 animate-fade-in">
            <div className="flex flex-col space-y-1">
              <Link
                to="/browse"
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center space-x-3 px-4 py-2.5 rounded-lg font-medium text-sm transition-all duration-200 ${
                  isActive('/browse')
                    ? 'bg-green-600 text-white'
                    : 'text-gray-300 hover:text-gray-100 hover:bg-gray-800'
                }`}
              >
                <Grid className="w-4 h-4" />
                <span>Attacks</span>
              </Link>

              <Link
                to="/docs"
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center space-x-3 px-4 py-2.5 rounded-lg font-medium text-sm transition-all duration-200 ${
                  isActive('/docs')
                    ? 'bg-green-600 text-white'
                    : 'text-gray-300 hover:text-gray-100 hover:bg-gray-800'
                }`}
              >
                <BookOpen className="w-4 h-4" />
                <span>Docs</span>
              </Link>

              <div className="px-4 py-2">
                <form onSubmit={handleSearch} className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Search className="w-4 h-4 text-gray-500" />
                  </div>
                  <input
                    type="text"
                    placeholder="Search attacks..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 text-sm border-2 border-gray-600 rounded-lg focus:outline-none focus:border-green-500 bg-gray-800 text-gray-100 placeholder-gray-500"
                  />
                </form>
              </div>

              <a
                href="https://github.com/montimage/mmt-attacker"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center space-x-3 px-4 py-2.5 rounded-lg font-medium text-sm text-gray-300 hover:text-gray-100 hover:bg-gray-800 transition-all duration-200"
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
