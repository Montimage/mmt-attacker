import { Link } from 'react-router-dom'
import { AlertTriangle, Mail, Globe } from 'lucide-react'

function Footer() {
  return (
    <footer className="bg-gray-50 border-t-2 border-gray-300 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Legal Disclaimer */}
        <div className="bg-white border-2 border-gray-400 rounded-lg shadow-custom-md p-6 mb-6">
          <div className="flex items-start space-x-3">
            <AlertTriangle className="w-6 h-6 text-black flex-shrink-0 mt-1" />
            <div>
              <h3 className="text-lg font-bold text-black mb-2">Legal Disclaimer</h3>
              <p className="text-gray-700 text-sm leading-relaxed">
                This tool is for <strong className="text-green-600">EDUCATIONAL AND TESTING PURPOSES ONLY</strong>. Users must obtain proper authorization before testing, use in controlled environments only, follow responsible disclosure practices, comply with all applicable laws and regulations, and accept full responsibility for any consequences. Improper use may be illegal and result in criminal charges.
              </p>
            </div>
          </div>
        </div>

        {/* Footer content */}
        <div className="grid md:grid-cols-3 gap-8">
          {/* Contact Information */}
          <div>
            <h4 className="text-lg font-bold text-black mb-4">Montimage</h4>
            <div className="space-y-2 text-sm text-gray-600">
              <div className="flex items-center space-x-2">
                <Globe className="w-4 h-4 text-black" />
                <a
                  href="https://www.montimage.eu"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-black hover:font-semibold transition-all"
                >
                  www.montimage.eu
                </a>
              </div>
              <div className="flex items-center space-x-2">
                <Mail className="w-4 h-4 text-black" />
                <a
                  href="mailto:contact@montimage.eu"
                  className="hover:text-black hover:font-semibold transition-all"
                >
                  contact@montimage.eu
                </a>
              </div>
              <p className="mt-2">39 rue Bobillot, 75013 Paris, France</p>
            </div>
          </div>

          {/* Resources */}
          <div>
            <h4 className="text-lg font-bold text-black mb-4">Resources</h4>
            <div className="space-y-2 text-sm">
              <a
                href="https://github.com/montimage/mmt-attacker"
                target="_blank"
                rel="noopener noreferrer"
                className="block text-gray-600 hover:text-black hover:font-semibold transition-all"
              >
                GitHub Repository
              </a>
              <a
                href="https://github.com/montimage/mmt-attacker/issues"
                target="_blank"
                rel="noopener noreferrer"
                className="block text-gray-600 hover:text-black hover:font-semibold transition-all"
              >
                Report Issues
              </a>
              <a
                href="mailto:developer@montimage.eu"
                className="block text-gray-600 hover:text-black hover:font-semibold transition-all"
              >
                Technical Support
              </a>
            </div>
          </div>

          {/* Legal */}
          <div>
            <h4 className="text-lg font-bold text-black mb-4">Legal</h4>
            <div className="space-y-2 text-sm">
              <Link
                to="/about"
                className="block text-gray-600 hover:text-black hover:font-semibold transition-all"
              >
                About Us
              </Link>
              <Link
                to="/privacy"
                className="block text-gray-600 hover:text-black hover:font-semibold transition-all"
              >
                Privacy Policy
              </Link>
              <Link
                to="/gdpr"
                className="block text-gray-600 hover:text-black hover:font-semibold transition-all"
              >
                GDPR Compliance
              </Link>
            </div>
          </div>
        </div>

        {/* Copyright */}
        <div className="mt-8 pt-6 border-t border-gray-300 text-center text-sm text-gray-600">
          <p>&copy; {new Date().getFullYear()} Montimage. All rights reserved.</p>
          <p className="mt-1">This software is proprietary. Unauthorized use is strictly prohibited.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
