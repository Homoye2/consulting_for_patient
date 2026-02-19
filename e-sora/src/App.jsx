import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import { ThemeProvider } from './contexts/ThemeContext'
import { ProtectedRoute } from './components/ProtectedRoute'
import { Layout } from './components/layouts'
import { LandingPage, Login, ServiceDetail } from './pages/public'
import { Dashboard } from './pages/Dashboard'
import { 
  Patients, 
  PatientDetail,
  Consultations, 
  ConsultationDetail,
  RendezVous, 
  RendezVousDetail,
  Stocks, 
  Utilisateurs,
  Hopitaux,
  HopitalDetail,
  Pharmacies,
  PharmacieDetail,
  Fournisseurs,
  Parametres
} from './pages/management'
import { PatientLayout } from './components/patient/PatientLayout'
import { PatientDashboard } from './pages/patient/PatientDashboard'
import { PatientRendezVous } from './pages/patient/PatientRendezVous'
import { PatientConsultations } from './pages/patient/PatientConsultations'
import { PatientContact } from './pages/patient/PatientContact'
import { PatientProfile } from './pages/patient/PatientProfile'
import { PaginationDemo } from './components/ui/pagination-demo'

// Composant pour protéger les routes selon le rôle
const RoleProtectedRoute = ({ children, allowedRoles = [] }) => {
  const { user } = useAuth()
  
  if (allowedRoles.length > 0 && !allowedRoles.includes(user?.role)) {
    return <Navigate to="/dashboard" replace />
  }
  
  return children
}

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
        path="/service/:id"
        element={<ServiceDetail />}
      />
      <Route
        path="/test-pagination"
        element={<PaginationDemo />}
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
        path="/patients/:id"
        element={
          <ProtectedRoute>
            <Layout>
              <PatientDetail />
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
        path="/consultations/:id"
        element={
          <ProtectedRoute>
            <Layout>
              <ConsultationDetail />
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
        path="/rendez-vous/:id"
        element={
          <ProtectedRoute>
            <Layout>
              <RendezVousDetail />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/stocks"
        element={
          <ProtectedRoute>
            <RoleProtectedRoute allowedRoles={['administrateur', 'pharmacien', 'reception']}>
              <Layout>
                <Stocks />
              </Layout>
            </RoleProtectedRoute>
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
      <Route
        path="/hopitaux"
        element={
          <ProtectedRoute>
            <Layout>
              <Hopitaux />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/hopitaux/:id"
        element={
          <ProtectedRoute>
            <Layout>
              <HopitalDetail />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/pharmacies"
        element={
          <ProtectedRoute>
            <Layout>
              <Pharmacies />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/pharmacies/:id"
        element={
          <ProtectedRoute>
            <Layout>
              <PharmacieDetail />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/fournisseurs"
        element={
          <ProtectedRoute>
            <Layout>
              <Fournisseurs />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/parametres"
        element={
          <ProtectedRoute>
            <Layout>
              <Parametres />
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
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter future={{ v7_relativeSplatPath: true }}>
          <AppRoutes />
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  )
}

export default App