import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from './context/ThemeContext'
import Layout from './components/layout/Layout'
import Home from './pages/Home'
import Browse from './pages/Browse'
import About from './pages/About'
import Docs from './pages/Docs'
import Privacy from './pages/Privacy'
import GDPR from './pages/GDPR'
import AttackPageTemplate from './pages/attacks/AttackPageTemplate'

function App() {
  return (
    <ThemeProvider>
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/browse" element={<Browse />} />
          <Route path="/about" element={<About />} />
          <Route path="/docs" element={<Docs />} />
          <Route path="/privacy" element={<Privacy />} />
          <Route path="/gdpr" element={<GDPR />} />
          <Route path="/attacks/:attackId" element={<AttackPageTemplate />} />
        </Routes>
      </Layout>
    </Router>
    </ThemeProvider>
  )
}

export default App
