import { Link } from 'react-router-dom'
import { AlertTriangle, Mail, Globe, Github } from 'lucide-react'

function Footer() {
  return (
    <footer className="bg-slate-900 border-t border-slate-700 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        {/* Legal Disclaimer */}
        <div className="bg-slate-800 border border-amber-500/30 rounded-xl p-5 mb-8">
          <div className="flex items-start space-x-3">
            <AlertTriangle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="text-sm font-bold text-amber-400 mb-1">Legal Disclaimer</h3>
              <p className="text-slate-400 text-xs leading-relaxed">
                This tool is for <strong className="text-green-400">EDUCATIONAL AND TESTING PURPOSES ONLY</strong>. Users must obtain proper authorization before testing, use in controlled environments only, follow responsible disclosure practices, comply with all applicable laws and regulations, and accept full responsibility for any consequences. Improper use may be illegal and result in criminal charges.
              </p>
            </div>
          </div>
        </div>

        {/* Footer content */}
        <div className="grid md:grid-cols-3 gap-8">
          {/* Contact Information */}
          <div>
            <h4 className="text-sm font-bold text-white mb-4 uppercase tracking-wider">Montimage</h4>
            <div className="space-y-2 text-sm text-slate-400">
              <div className="flex items-center space-x-2">
                <Globe className="w-4 h-4 text-green-400 flex-shrink-0" />
                <a
                  href="https://www.montimage.eu"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-green-400 transition-colors"
                >
                  www.montimage.eu
                </a>
              </div>
              <div className="flex items-center space-x-2">
                <Mail className="w-4 h-4 text-green-400 flex-shrink-0" />
                <a
                  href="mailto:contact@montimage.eu"
                  className="hover:text-green-400 transition-colors"
                >
                  contact@montimage.eu
                </a>
              </div>
              <p className="mt-2 text-slate-500">39 rue Bobillot, 75013 Paris, France</p>
            </div>
          </div>

          {/* Resources */}
          <div>
            <h4 className="text-sm font-bold text-white mb-4 uppercase tracking-wider">Resources</h4>
            <div className="space-y-2 text-sm">
              <a
                href="https://github.com/montimage/mmt-attacker"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center space-x-2 text-slate-400 hover:text-green-400 transition-colors"
              >
                <Github className="w-3.5 h-3.5" />
                <span>GitHub Repository</span>
              </a>
              <a
                href="https://github.com/montimage/mmt-attacker/issues"
                target="_blank"
                rel="noopener noreferrer"
                className="block text-slate-400 hover:text-green-400 transition-colors"
              >
                Report Issues
              </a>
              <a
                href="mailto:developer@montimage.eu"
                className="block text-slate-400 hover:text-green-400 transition-colors"
              >
                Technical Support
              </a>
            </div>
          </div>

          {/* Legal */}
          <div>
            <h4 className="text-sm font-bold text-white mb-4 uppercase tracking-wider">Legal</h4>
            <div className="space-y-2 text-sm">
              <Link
                to="/about"
                className="block text-slate-400 hover:text-green-400 transition-colors"
              >
                About Us
              </Link>
              <Link
                to="/privacy"
                className="block text-slate-400 hover:text-green-400 transition-colors"
              >
                Privacy Policy
              </Link>
              <Link
                to="/gdpr"
                className="block text-slate-400 hover:text-green-400 transition-colors"
              >
                GDPR Compliance
              </Link>
            </div>
          </div>
        </div>

        {/* Copyright */}
        <div className="mt-8 pt-6 border-t border-slate-800 text-center text-xs text-slate-500">
          <p>&copy; {new Date().getFullYear()} Montimage. All rights reserved.</p>
          <p className="mt-1">This software is proprietary. Unauthorized use is strictly prohibited.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
