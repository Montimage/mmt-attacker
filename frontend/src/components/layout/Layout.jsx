import { useState } from 'react'
import { useLocation } from 'react-router-dom'
import Header from './Header'
import Footer from './Footer'
import Sidebar from './Sidebar'
import ScrollToTop from '../common/ScrollToTop'
import { Menu } from 'lucide-react'

function Layout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const location = useLocation()

  // Check if we're on an attack page (should show sidebar)
  const showSidebar = location.pathname.startsWith('/attacks/') || location.pathname === '/'

  return (
    <div className="min-h-screen flex flex-col bg-white">
      <Header />

      <div className="flex flex-1">
        {/* Sidebar toggle button for mobile */}
        {showSidebar && (
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="fixed bottom-6 right-6 lg:hidden z-50 bg-green-900 text-white p-4 rounded-full shadow-custom-lg hover:bg-green-800 transition-colors"
            aria-label="Toggle sidebar"
          >
            <Menu className="w-6 h-6" />
          </button>
        )}

        {/* Sidebar */}
        {showSidebar && (
          <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
        )}

        {/* Main content */}
        <main className={`flex-1 ${showSidebar ? 'lg:ml-0' : ''}`}>
          {children}
        </main>
      </div>

      <Footer />

      {/* Scroll to top button */}
      <ScrollToTop />
    </div>
  )
}

export default Layout
