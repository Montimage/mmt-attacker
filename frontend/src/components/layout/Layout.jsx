import Header from './Header'
import Footer from './Footer'
import ScrollToTop from '../common/ScrollToTop'

function Layout({ children }) {
  return (
    <div className="min-h-screen flex flex-col bg-white">
      <Header />

      {/* Main content */}
      <main className="flex-1">
        {children}
      </main>

      <Footer />

      {/* Scroll to top button */}
      <ScrollToTop />
    </div>
  )
}

export default Layout
