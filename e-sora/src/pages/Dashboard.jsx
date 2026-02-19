
import { useAuth } from '../contexts/AuthContext'
import { SuperAdminDashboard } from './dashboard/super-admin'
import { UserDashboard } from './dashboard/user'

export const Dashboard = () => {
  const { user } = useAuth()

  // Si l'utilisateur est super admin, afficher le dashboard super admin
  if (user?.role === 'super_admin') {
    return <SuperAdminDashboard />
  }

  // Sinon, afficher le dashboard utilisateur normal
  return <UserDashboard />
}