import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { AlertCircle } from 'lucide-react'
import { Button } from './ui/button'

export const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading, user } = useAuth()

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  // Vérifier si l'utilisateur est Super Admin
  if (user?.role !== 'super_admin') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background via-background to-primary/10 p-4">
        <Card className="w-full max-w-md">
          <CardHeader className="space-y-1 text-center">
            <div className="flex justify-center mb-4">
              <div className="rounded-full bg-red-100 dark:bg-red-900/20 p-3">
                <AlertCircle className="h-8 w-8 text-red-600 dark:text-red-400" />
              </div>
            </div>
            <CardTitle className="text-2xl font-bold">Accès refusé</CardTitle>
            <CardDescription>
              Réservé aux Super Administrateurs
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-800 text-red-900 dark:text-red-100 text-sm p-4 rounded-md">
              <div className="font-semibold mb-2">Accès non autorisé</div>
              <div>
                Seuls les Super Administrateurs peuvent accéder à cette application de gestion.
              </div>
              <div className="mt-3 text-xs opacity-90 italic">
                {user?.role === 'pharmacien' 
                  ? 'Veuillez utiliser l\'application dédiée aux pharmacies.'
                  : 'Contactez votre administrateur système pour obtenir les droits d\'accès nécessaires.'
                }
              </div>
            </div>
            <Button 
              onClick={() => {
                // Déconnexion et redirection
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                localStorage.removeItem('user')
                window.location.href = '/login'
              }}
              className="w-full"
              variant="outline"
            >
              Se déconnecter
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return children
}

