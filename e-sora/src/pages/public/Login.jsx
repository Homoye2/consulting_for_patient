import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'
import { Button } from '../../components/ui/button'
import { Input } from '../../components/ui/input'
import { Label } from '../../components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card'
import { Heart, AlertCircle } from 'lucide-react'
import { AnimatedContainer } from '../../components/ui/animated-page'

export const Login = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isPharmacienBlocked, setIsPharmacienBlocked] = useState(false)
  const [isSuperAdminRequired, setIsSuperAdminRequired] = useState(false)
  const [loading, setLoading] = useState(false)
  const [googleLoading, setGoogleLoading] = useState(false)
  const { login, googleLogin } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    // Initialiser Google Sign-In quand le script est chargé
    const initGoogleSignIn = () => {
      if (window.google && window.google.accounts && window.google.accounts.id) {
        const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID
        if (clientId) {
          window.google.accounts.id.initialize({
            client_id: clientId,
            callback: handleGoogleSignIn,
          })

          // Rendre le bouton Google
          const buttonDiv = document.getElementById('google-signin-button')
          if (buttonDiv) {
            window.google.accounts.id.renderButton(buttonDiv, {
              theme: 'outline',
              size: 'large',
              width: '100%',
              text: 'signin_with',
              locale: 'fr',
            })
          }
        }
      }
    }

    // Attendre que le script Google soit chargé
    if (window.google) {
      initGoogleSignIn()
    } else {
      // Attendre le chargement du script
      const checkGoogle = setInterval(() => {
        if (window.google) {
          initGoogleSignIn()
          clearInterval(checkGoogle)
        }
      }, 100)

      return () => clearInterval(checkGoogle)
    }
  }, [])

  const handleGoogleSignIn = async (response) => {
    setError('')
    setGoogleLoading(true)
    setIsPharmacienBlocked(false)
    setIsSuperAdminRequired(false)

    try {
      // response.credential contient le JWT ID token de Google
      const result = await googleLogin(response.credential)
      setGoogleLoading(false)

      if (result.success) {
        const currentUser = JSON.parse(localStorage.getItem('user'))
        if (currentUser?.patient_profile || currentUser?.is_patient) {
          navigate('/patient/dashboard')
        } else {
          navigate('/dashboard')
        }
      } else {
        if (result.isSuperAdminRequired) {
          setIsSuperAdminRequired(true)
          setError(result.error || 'Accès refusé')
        } else if (result.isPharmacienBlocked) {
          setIsPharmacienBlocked(true)
          setError(result.error || 'Accès refusé')
        } else {
          setIsPharmacienBlocked(false)
          setIsSuperAdminRequired(false)
          setError(result.error || 'Erreur de connexion Google')
        }
      }
    } catch (err) {
      setGoogleLoading(false)
      setError('Erreur lors de la connexion Google')
    }
  }


  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    setIsPharmacienBlocked(false)
    setIsSuperAdminRequired(false)

    const result = await login(email, password)
    setLoading(false)

    if (result.success) {
      // Rediriger les patients vers leur interface, les autres vers le dashboard
      const currentUser = JSON.parse(localStorage.getItem('user'))
      if (currentUser?.patient_profile || currentUser?.is_patient) {
        navigate('/patient/dashboard')
      } else {
        navigate('/dashboard')
      }
    } else {
      // Vérifier le type d'erreur
      if (result.isSuperAdminRequired) {
        setIsSuperAdminRequired(true)
        setError(result.error || 'Accès refusé')
      } else if (result.isPharmacienBlocked) {
        setIsPharmacienBlocked(true)
        setError(result.error || 'Accès refusé')
      } else {
        setIsPharmacienBlocked(false)
        setIsSuperAdminRequired(false)
        setError(result.error || 'Erreur de connexion')
      }
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background via-background to-primary/10 p-4">
      <AnimatedContainer>
        <Card className="w-full max-w-md">
        <CardHeader className="space-y-1 text-center">
          <div className="flex justify-center mb-4">
            <div className="rounded-full bg-primary/20 p-3">
              <Heart className="h-8 w-8 text-primary" />
            </div>
          </div>
          <CardTitle className="text-3xl font-bold">Connexion Super Admin</CardTitle>
          <CardDescription>
            Accès réservé aux Super Administrateurs pour la gestion de planification familiale
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className={`text-sm p-4 rounded-md ${
                isSuperAdminRequired
                  ? 'bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-800 text-red-900 dark:text-red-100'
                  : isPharmacienBlocked 
                    ? 'bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-800 text-blue-900 dark:text-blue-100' 
                    : 'bg-destructive/10 text-destructive border border-destructive/20'
              }`}>
                <div className="flex items-start gap-2">
                  {(isPharmacienBlocked || isSuperAdminRequired) && (
                    <AlertCircle className="h-5 w-5 mt-0.5 flex-shrink-0" />
                  )}
                  <div className="flex-1">
                    <div className="font-semibold mb-1">
                      {isSuperAdminRequired 
                        ? 'Accès réservé aux Super Administrateurs' 
                        : isPharmacienBlocked 
                          ? 'Accès réservé aux pharmaciens' 
                          : 'Erreur de connexion'}
                    </div>
                    <div className={
                      isSuperAdminRequired 
                        ? 'text-red-800 dark:text-red-200' 
                        : isPharmacienBlocked 
                          ? 'text-blue-800 dark:text-blue-200' 
                          : ''
                    }>
                      {error}
                    </div>
                    {isSuperAdminRequired && (
                      <div className="mt-3 text-xs opacity-90 italic">
                        Seuls les Super Administrateurs peuvent accéder à cette application de gestion.
                      </div>
                    )}
                    {isPharmacienBlocked && (
                      <div className="mt-3 text-xs opacity-90 italic">
                        Veuillez utiliser l'application dédiée aux pharmacies pour accéder à votre espace de gestion.
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="votre@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={loading}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Mot de passe</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={loading}
              />
            </div>
            <Button type="submit" className="w-full" disabled={loading || googleLoading}>
              {loading ? 'Connexion...' : 'Se connecter'}
            </Button>
            
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-card px-2 text-muted-foreground">Ou continuer avec</span>
              </div>
            </div>

            <div id="google-signin-button" className="w-full"></div>
            {!import.meta.env.VITE_GOOGLE_CLIENT_ID && (
              <p className="text-xs text-muted-foreground text-center">
                Google Sign-In n'est pas configuré
              </p>
            )}

            <Button onClick={() => navigate('/')} className="w-full bg-gray-500 text-white" disabled={loading || googleLoading}>
              Retour à la page d'accueil  
            </Button>
          </form>
        </CardContent>
      </Card>
      </AnimatedContainer>
    </div>
  )
}

