import { createContext, useContext, useState, useEffect } from 'react'
import { authService } from '../services/authService'

const AuthContext = createContext(null)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const currentUser = authService.getCurrentUser()
    if (currentUser && authService.isAuthenticated()) {
      // Vérifier si l'utilisateur connecté est Super Admin
      if (currentUser.role !== 'super_admin') {
        // Déconnecter immédiatement si ce n'est pas un Super Admin
        authService.logout()
        setUser(null)
      } else {
        setUser(currentUser)
      }
    }
    setLoading(false)
  }, [])

  const login = async (email, password) => {
    try {
      const { user } = await authService.login(email, password)
      
      // Vérifier si l'utilisateur est Super Admin
      if (user.role !== 'super_admin') {
        // Déconnecter immédiatement si ce n'est pas un Super Admin
        authService.logout()
        return {
          success: false,
          error: 'Accès refusé. Seuls les Super Administrateurs peuvent accéder à cette application.',
          isSuperAdminRequired: true
        }
      }
      
      setUser(user)
      return { success: true }
    } catch (error) {
      console.error('Erreur de connexion:', error)
      let errorMessage = 'Erreur de connexion'
      
      if (error.response) {
        // Erreur de réponse du serveur
        const data = error.response.data
        
        // Vérifier si c'est un blocage pour pharmacien
        // Le message peut être dans detail, non_field_errors, ou directement dans data
        let pharmacienMessage = null
        if (data.detail && typeof data.detail === 'string' && data.detail.includes('pharmacien')) {
          pharmacienMessage = data.detail
        } else if (data.non_field_errors) {
          const errorText = Array.isArray(data.non_field_errors) 
            ? data.non_field_errors[0] 
            : data.non_field_errors
          if (typeof errorText === 'string' && errorText.includes('pharmacien')) {
            pharmacienMessage = errorText
          }
        }
        
        if (pharmacienMessage) {
          return {
            success: false,
            error: pharmacienMessage,
            isPharmacienBlocked: true
          }
        }
        
        if (data.detail) {
          errorMessage = data.detail
        } else if (data.non_field_errors) {
          errorMessage = Array.isArray(data.non_field_errors) 
            ? data.non_field_errors[0] 
            : data.non_field_errors
        } else if (data.email) {
          errorMessage = Array.isArray(data.email) ? data.email[0] : data.email
        } else if (data.password) {
          errorMessage = Array.isArray(data.password) ? data.password[0] : data.password
        } else {
          errorMessage = `Erreur ${error.response.status}: ${JSON.stringify(data)}`
        }
      } else if (error.request) {
        // Pas de réponse du serveur
        errorMessage = 'Impossible de se connecter au serveur. Vérifiez que le backend est démarré.'
      } else {
        // Erreur de configuration
        errorMessage = error.message || 'Erreur de connexion'
      }
      
      return {
        success: false,
        error: errorMessage,
      }
    }
  }

  const googleLogin = async (token) => {
    try {
      const { user } = await authService.googleLogin(token)
      
      // Vérifier si l'utilisateur est Super Admin
      if (user.role !== 'super_admin') {
        // Déconnecter immédiatement si ce n'est pas un Super Admin
        authService.logout()
        return {
          success: false,
          error: 'Accès refusé. Seuls les Super Administrateurs peuvent accéder à cette application.',
          isSuperAdminRequired: true
        }
      }
      
      setUser(user)
      return { success: true }
    } catch (error) {
      console.error('Erreur de connexion Google:', error)
      let errorMessage = 'Erreur de connexion Google'
      
      if (error.response) {
        const data = error.response.data
        
        // Vérifier si c'est un blocage pour pharmacien
        if (data.pharmacien_blocked || (data.error && data.error.includes('pharmacien'))) {
          return {
            success: false,
            error: data.error || 'Les pharmaciens doivent utiliser l\'application dédiée aux pharmacies.',
            isPharmacienBlocked: true
          }
        }
        
        errorMessage = data.error || data.detail || `Erreur ${error.response.status}`
      } else if (error.request) {
        errorMessage = 'Impossible de se connecter au serveur. Vérifiez que le backend est démarré.'
      } else {
        errorMessage = error.message || 'Erreur de connexion Google'
      }
      
      return {
        success: false,
        error: errorMessage,
      }
    }
  }

  const logout = () => {
    authService.logout()
    setUser(null)
  }

  const updateUser = (updatedUser) => {
    setUser(updatedUser)
    // Mettre à jour aussi dans le localStorage
    localStorage.setItem('user', JSON.stringify(updatedUser))
  }

  const value = {
    user,
    login,
    googleLogin,
    logout,
    updateUser,
    isAuthenticated: !!user,
    loading,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

