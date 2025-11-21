import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import Home from './pages/Home'
import AttackPageTemplate from './pages/attacks/AttackPageTemplate'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/attacks/:attackId" element={<AttackPageTemplate />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
