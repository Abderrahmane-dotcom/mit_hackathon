import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from '@/components/ui/toaster'
import Navigation from '@/components/Navigation'
import Home from '@/pages/Home'
import Upload from '@/pages/Upload'
import Dashboard from '@/pages/Dashboard'
import Report from '@/pages/Report'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background">
        <Navigation />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/report" element={<Report />} />
        </Routes>
        <Toaster />
      </div>
    </Router>
  )
}

export default App
