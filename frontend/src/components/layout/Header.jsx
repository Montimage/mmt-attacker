import { Link, useLocation, useNavigate } from 'react-router-dom'
import { Menu, X, Home, Github, Search, Grid } from 'lucide-react'
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
    <header className="sticky top-0 z-50 bg-white border-b-3 border-gray-400 shadow-custom-lg backdrop-blur-sm bg-opacity-95">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo and branding - Enhanced with 3D effect */}
          <Link
            to="/"
            className="flex items-center space-x-3 group"
          >
            <div className="relative p-2 bg-white border-2 border-gray-400 rounded-lg shadow-custom-md group-hover:shadow-custom-lg group-hover:-translate-y-0.5 group-hover:border-black transition-all duration-200">
              <img
                src="/logo.svg"
                alt="MMT-Attacker Logo"
                className="w-7 h-7 object-contain"
              />
            </div>
            <div className="flex flex-col">
              <span className="text-xl font-bold text-black group-hover:text-gray-900 transition-colors">
                MMT-Attacker
              </span>
              <span className="text-xs font-medium text-gray-600 hidden sm:block">
                Demo Platform
              </span>
            </div>
          </Link>

          {/* Desktop navigation - Enhanced with pill-style buttons */}
          <nav className="hidden md:flex items-center space-x-2">
            <Link
              to="/"
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-semibold transition-all duration-200 border-2 ${
                isActive('/')
                  ? 'bg-black text-white border-black shadow-custom-md'
                  : 'bg-white text-gray-700 border-gray-300 hover:border-gray-500 hover:shadow-custom hover:-translate-y-0.5'
              }`}
            >
              <Home className="w-4 h-4" />
              <span>Home</span>
            </Link>

            <Link
              to="/browse"
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-semibold transition-all duration-200 border-2 ${
                isActive('/browse')
                  ? 'bg-black text-white border-black shadow-custom-md'
                  : 'bg-white text-gray-700 border-gray-300 hover:border-gray-500 hover:shadow-custom hover:-translate-y-0.5'
              }`}
            >
              <Grid className="w-4 h-4" />
              <span>Browse</span>
            </Link>

            {/* Search Button */}
            <button
              onClick={() => setSearchOpen(!searchOpen)}
              className="flex items-center space-x-2 px-4 py-2 rounded-lg font-semibold transition-all duration-200 bg-white text-gray-700 border-2 border-gray-300 hover:border-gray-500 hover:shadow-custom hover:-translate-y-0.5"
            >
              <Search className="w-4 h-4" />
              <span>Search</span>
            </button>

            <a
              href="https://github.com/montimage/mmt-attacker"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-2 px-4 py-2 rounded-lg font-semibold transition-all duration-200 bg-white text-gray-700 border-2 border-gray-400 hover:border-black hover:shadow-custom-md hover:-translate-y-0.5"
              title="View on GitHub"
            >
              <Github className="w-4 h-4" />
              <span>GitHub</span>
            </a>
          </nav>

          {/* Mobile menu button - Enhanced with 3D effect */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2.5 rounded-lg bg-white border-2 border-gray-400 shadow-custom hover:shadow-custom-md hover:border-black hover:-translate-y-0.5 transition-all duration-200"
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? (
              <X className="w-6 h-6 text-black" />
            ) : (
              <Menu className="w-6 h-6 text-black" />
            )}
          </button>
        </div>

        {/* Search Bar (Desktop) */}
        {searchOpen && (
          <div className="hidden md:block py-4 border-t-2 border-gray-300 animate-fade-in">
            <form onSubmit={handleSearch} className="relative max-w-2xl mx-auto">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <Search className="w-5 h-5 text-gray-500" />
              </div>
              <input
                type="text"
                placeholder="Search for attacks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                autoFocus
                className="w-full pl-12 pr-12 py-3 text-base border-2 border-gray-400 rounded-lg focus:outline-none focus:border-black focus:shadow-custom-md transition-all bg-white font-medium"
              />
              <button
                type="button"
                onClick={() => setSearchOpen(false)}
                className="absolute inset-y-0 right-0 pr-4 flex items-center hover:opacity-70 transition-opacity"
              >
                <X className="w-5 h-5 text-gray-600" />
              </button>
            </form>
          </div>
        )}

        {/* Mobile navigation - Enhanced with better spacing and 3D effects */}
        {mobileMenuOpen && (
          <nav className="md:hidden py-4 border-t-2 border-gray-300 animate-fade-in">
            <div className="flex flex-col space-y-2">
              <Link
                to="/"
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center space-x-3 px-4 py-3 rounded-lg font-semibold transition-all duration-200 border-2 ${
                  isActive('/')
                    ? 'bg-black text-white border-black shadow-custom-md'
                    : 'bg-white text-gray-700 border-gray-300 hover:border-gray-500 hover:shadow-custom'
                }`}
              >
                <Home className="w-5 h-5" />
                <span>Home</span>
              </Link>

              <Link
                to="/browse"
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center space-x-3 px-4 py-3 rounded-lg font-semibold transition-all duration-200 border-2 ${
                  isActive('/browse')
                    ? 'bg-black text-white border-black shadow-custom-md'
                    : 'bg-white text-gray-700 border-gray-300 hover:border-gray-500 hover:shadow-custom'
                }`}
              >
                <Grid className="w-5 h-5" />
                <span>Browse Attacks</span>
              </Link>

              {/* Mobile Search Form */}
              <div className="px-4 py-3">
                <form onSubmit={handleSearch} className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Search className="w-4 h-4 text-gray-500" />
                  </div>
                  <input
                    type="text"
                    placeholder="Search attacks..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2.5 text-sm border-2 border-gray-400 rounded-lg focus:outline-none focus:border-black focus:shadow-custom-md transition-all bg-white"
                  />
                </form>
              </div>

              <a
                href="https://github.com/montimage/mmt-attacker"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center space-x-3 px-4 py-3 rounded-lg font-semibold transition-all duration-200 bg-white text-gray-700 border-2 border-gray-400 hover:border-black hover:shadow-custom-md"
              >
                <Github className="w-5 h-5" />
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
