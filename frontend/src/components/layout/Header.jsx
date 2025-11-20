import { Link } from 'react-router-dom'
import { Shield, Menu, X } from 'lucide-react'
import { useState } from 'react'

function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <header className="sticky top-0 z-50 bg-white border-b-2 border-gray-200 shadow-custom">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and branding */}
          <Link to="/" className="flex items-center space-x-3 hover:opacity-80 transition-opacity">
            <Shield className="w-8 h-8 text-green-900" />
            <span className="text-xl font-bold text-black">MMT-Attacker Demo</span>
          </Link>

          {/* Desktop navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            <Link to="/" className="text-gray-700 hover:text-green-900 font-medium transition-colors">
              Home
            </Link>
            <a
              href="https://github.com/montimage/mmt-attacker"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-700 hover:text-green-900 font-medium transition-colors"
            >
              Documentation
            </a>
          </nav>

          {/* Mobile menu button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? (
              <X className="w-6 h-6 text-gray-700" />
            ) : (
              <Menu className="w-6 h-6 text-gray-700" />
            )}
          </button>
        </div>

        {/* Mobile navigation */}
        {mobileMenuOpen && (
          <nav className="md:hidden py-4 border-t border-gray-200">
            <div className="flex flex-col space-y-3">
              <Link
                to="/"
                onClick={() => setMobileMenuOpen(false)}
                className="text-gray-700 hover:text-green-900 font-medium transition-colors py-2"
              >
                Home
              </Link>
              <a
                href="https://github.com/montimage/mmt-attacker"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-700 hover:text-green-900 font-medium transition-colors py-2"
              >
                Documentation
              </a>
            </div>
          </nav>
        )}
      </div>
    </header>
  )
}

export default Header
