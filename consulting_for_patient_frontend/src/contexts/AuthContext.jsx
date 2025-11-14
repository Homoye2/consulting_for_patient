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
      setUser(currentUser)
    }
    setLoading(false)
  }, [])

  const login = async (email, password) => {
    try {
      const { user } = await authService.login(email, password)
      setUser(user)
      return { success: true }
    } catch (error) {
      console.error('Erreur de connexion:', error)
      let errorMessage = 'Erreur de connexion'
      
      if (error.response) {
        // Erreur de réponse du serveur
        const data = error.response.data
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

  const logout = () => {
    authService.logout()
    setUser(null)
  }

  const value = {
    user,
    login,
    logout,
    isAuthenticated: !!user,
    loading,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

