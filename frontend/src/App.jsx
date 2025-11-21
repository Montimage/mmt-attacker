import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import Home from './pages/Home'
import Browse from './pages/Browse'
import About from './pages/About'
import Privacy from './pages/Privacy'
import GDPR from './pages/GDPR'
import AttackPageTemplate from './pages/attacks/AttackPageTemplate'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/browse" element={<Browse />} />
          <Route path="/about" element={<About />} />
          <Route path="/privacy" element={<Privacy />} />
          <Route path="/gdpr" element={<GDPR />} />
          <Route path="/attacks/:attackId" element={<AttackPageTemplate />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
