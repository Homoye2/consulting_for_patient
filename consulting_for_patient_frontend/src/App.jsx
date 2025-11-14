import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import { ProtectedRoute } from './components/ProtectedRoute'
import { Layout } from './components/Layout'
import { LandingPage } from './pages/LandingPage'
import { Login } from './pages/Login'
import { Dashboard } from './pages/Dashboard'
import { Patients } from './pages/Patients'
import { Consultations } from './pages/Consultations'
import { RendezVous } from './pages/RendezVous'
import { Stocks } from './pages/Stocks'
import { Utilisateurs } from './pages/Utilisateurs'

const AppRoutes = () => {
  const { isAuthenticated } = useAuth()

  return (
    <Routes>
      <Route
        path="/"
        element={<LandingPage />}
      />
      <Route
        path="/login"
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <Login />}
      />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Layout>
              <Dashboard />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/patients"
        element={
          <ProtectedRoute>
            <Layout>
              <Patients />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/consultations"
        element={
          <ProtectedRoute>
            <Layout>
              <Consultations />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/rendez-vous"
        element={
          <ProtectedRoute>
            <Layout>
              <RendezVous />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/stocks"
        element={
          <ProtectedRoute>
            <Layout>
              <Stocks />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/utilisateurs"
        element={
          <ProtectedRoute>
            <Layout>
              <Utilisateurs />
            </Layout>
          </ProtectedRoute>
        }
      />
    </Routes>
  )
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
