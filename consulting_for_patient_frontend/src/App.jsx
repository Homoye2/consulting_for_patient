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
import { PatientLayout } from './components/patient/PatientLayout'
import { PatientDashboard } from './pages/patient/PatientDashboard'
import { PatientRendezVous } from './pages/patient/PatientRendezVous'
import { PatientConsultations } from './pages/patient/PatientConsultations'
import { PatientContact } from './pages/patient/PatientContact'
import { PatientProfile } from './pages/patient/PatientProfile'

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
      {/* Routes Patient */}
      <Route
        path="/patient/dashboard"
        element={
          <ProtectedRoute>
            <PatientLayout>
              <PatientDashboard />
            </PatientLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/patient/rendez-vous"
        element={
          <ProtectedRoute>
            <PatientLayout>
              <PatientRendezVous />
            </PatientLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/patient/consultations"
        element={
          <ProtectedRoute>
            <PatientLayout>
              <PatientConsultations />
            </PatientLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/patient/contact"
        element={
          <ProtectedRoute>
            <PatientLayout>
              <PatientContact />
            </PatientLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/patient/profile"
        element={
          <ProtectedRoute>
            <PatientLayout>
              <PatientProfile />
            </PatientLayout>
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
