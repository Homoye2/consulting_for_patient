import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card'
import { Button } from '../../components/ui/button'
import { Input } from '../../components/ui/input'
import { Label } from '../../components/ui/label'
import { User, Lock, Save, Eye, EyeOff } from 'lucide-react'
import { usersService } from '../../services/apiService'
import { useAuth } from '../../contexts/AuthContext'
import api from '../../lib/api'

export default function Parametres() {
  const { user, updateUser } = useAuth()
  const [loading, setLoading] = useState(false)
  const [showCurrentPassword, setShowCurrentPassword] = useState(false)
  const [showNewPassword, setShowNewPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  
  // Formulaire d'informations personnelles
  const [profileForm, setProfileForm] = useState({
    nom: '',
    email: ''
  })
  
  // Formulaire de changement de mot de passe
  const [passwordForm, setPasswordForm] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  })
  
  const [errors, setErrors] = useState({})
  const [successMessage, setSuccessMessage] = useState('')

  useEffect(() => {
    console.log("user :",user)
    if (user) {
      setProfileForm({
        nom: user.nom || '',
        email: user.email || ''
      })
    }
  }, [user])

  const handleProfileUpdate = async (e) => {
    e.preventDefault()
    setLoading(true)
    setErrors({})
    setSuccessMessage('')

    try {
      const response = await usersService.update(user.id, {
        nom: profileForm.nom,
        email: profileForm.email
      })


      // Mettre à jour le contexte utilisateur
      updateUser({
        ...user,
        nom: response.data.nom,
        email: response.data.email
      })

      setSuccessMessage('Informations mises à jour avec succès !')
      
      // Effacer le message après 3 secondes
      setTimeout(() => setSuccessMessage(''), 3000)
    } catch (error) {
      console.error('Erreur lors de la mise à jour du profil:', error)
      
      if (error.response?.data) {
        setErrors(error.response.data)
      } else {
        setErrors({ general: 'Une erreur est survenue lors de la mise à jour.' })
      }
    } finally {
      setLoading(false)
    }
  }

  const handlePasswordChange = async (e) => {
    e.preventDefault()
    setLoading(true)
    setErrors({})
    setSuccessMessage('')

    // Validation côté client
    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
      setErrors({ confirmPassword: 'Les mots de passe ne correspondent pas.' })
      setLoading(false)
      return
    }

    if (passwordForm.newPassword.length < 8) {
      setErrors({ newPassword: 'Le mot de passe doit contenir au moins 8 caractères.' })
      setLoading(false)
      return
    }

    try {
      await api.post('/auth/change-password/', {
        current_password: passwordForm.currentPassword,
        new_password: passwordForm.newPassword
      })

      setSuccessMessage('Mot de passe modifié avec succès !')
      
      // Réinitialiser le formulaire
      setPasswordForm({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      })
      
      // Effacer le message après 3 secondes
      setTimeout(() => setSuccessMessage(''), 3000)
    } catch (error) {
      console.error('Erreur lors du changement de mot de passe:', error)
      
      if (error.response?.data) {
        if (error.response.data.current_password) {
          setErrors({ currentPassword: error.response.data.current_password[0] })
        } else if (error.response.data.new_password) {
          setErrors({ newPassword: error.response.data.new_password[0] })
        } else if (error.response.data.error) {
          setErrors({ general: error.response.data.error })
        } else {
          setErrors({ general: 'Une erreur est survenue.' })
        }
      } else {
        setErrors({ general: 'Une erreur est survenue lors du changement de mot de passe.' })
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* En-tête */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Paramètres</h1>
        <p className="text-gray-600">
          Gérez vos informations personnelles et votre sécurité
        </p>
      </div>

      {/* Messages de succès */}
      {successMessage && (
        <div className="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded-lg">
          {successMessage}
        </div>
      )}

      {/* Erreurs générales */}
      {errors.general && (
        <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg">
          {errors.general}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Informations personnelles */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <User className="h-5 w-5" />
              Informations personnelles
            </CardTitle>
            <CardDescription>
              Modifiez vos informations de profil
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleProfileUpdate} className="space-y-4">
              <div>
                <Label htmlFor="nom">Nom complet *</Label>
                <Input
                  id="nom"
                  type="text"
                  value={profileForm.nom}
                  onChange={(e) => setProfileForm({ ...profileForm, nom: e.target.value })}
                  required
                  className={errors.nom ? 'border-red-500' : ''}
                />
                {errors.nom && (
                  <p className="text-sm text-red-600 mt-1">{errors.nom[0]}</p>
                )}
              </div>

              <div>
                <Label htmlFor="email">Email *</Label>
                <Input
                  id="email"
                  type="email"
                  value={profileForm.email}
                  onChange={(e) => setProfileForm({ ...profileForm, email: e.target.value })}
                  required
                  className={errors.email ? 'border-red-500' : ''}
                />
                {errors.email && (
                  <p className="text-sm text-red-600 mt-1">{errors.email[0]}</p>
                )}
              </div>

              <div>
                <Label>Rôle</Label>
                <Input
                  type="text"
                  value={user?.role === 'super_admin' ? 'Super Administrateur' : user?.role || ''}
                  disabled
                  className="bg-gray-100"
                />
              </div>

              <Button
                type="submit"
                disabled={loading}
                className="w-full"
              >
                <Save className="h-4 w-4 mr-2" />
                {loading ? 'Enregistrement...' : 'Enregistrer les modifications'}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Changement de mot de passe */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Lock className="h-5 w-5" />
              Sécurité
            </CardTitle>
            <CardDescription>
              Modifiez votre mot de passe
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handlePasswordChange} className="space-y-4">
              <div>
                <Label htmlFor="currentPassword">Mot de passe actuel *</Label>
                <div className="relative">
                  <Input
                    id="currentPassword"
                    type={showCurrentPassword ? 'text' : 'password'}
                    value={passwordForm.currentPassword}
                    onChange={(e) => setPasswordForm({ ...passwordForm, currentPassword: e.target.value })}
                    required
                    className={errors.currentPassword ? 'border-red-500' : ''}
                  />
                  <button
                    type="button"
                    onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                  >
                    {showCurrentPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
                {errors.currentPassword && (
                  <p className="text-sm text-red-600 mt-1">{errors.currentPassword}</p>
                )}
              </div>

              <div>
                <Label htmlFor="newPassword">Nouveau mot de passe *</Label>
                <div className="relative">
                  <Input
                    id="newPassword"
                    type={showNewPassword ? 'text' : 'password'}
                    value={passwordForm.newPassword}
                    onChange={(e) => setPasswordForm({ ...passwordForm, newPassword: e.target.value })}
                    required
                    minLength={8}
                    className={errors.newPassword ? 'border-red-500' : ''}
                  />
                  <button
                    type="button"
                    onClick={() => setShowNewPassword(!showNewPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                  >
                    {showNewPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
                {errors.newPassword && (
                  <p className="text-sm text-red-600 mt-1">{errors.newPassword}</p>
                )}
                <p className="text-xs text-gray-500 mt-1">
                  Minimum 8 caractères
                </p>
              </div>

              <div>
                <Label htmlFor="confirmPassword">Confirmer le nouveau mot de passe *</Label>
                <div className="relative">
                  <Input
                    id="confirmPassword"
                    type={showConfirmPassword ? 'text' : 'password'}
                    value={passwordForm.confirmPassword}
                    onChange={(e) => setPasswordForm({ ...passwordForm, confirmPassword: e.target.value })}
                    required
                    minLength={8}
                    className={errors.confirmPassword ? 'border-red-500' : ''}
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                  >
                    {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
                {errors.confirmPassword && (
                  <p className="text-sm text-red-600 mt-1">{errors.confirmPassword}</p>
                )}
              </div>

              <Button
                type="submit"
                disabled={loading}
                className="w-full"
              >
                <Lock className="h-4 w-4 mr-2" />
                {loading ? 'Modification...' : 'Changer le mot de passe'}
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>

      {/* Informations du compte */}
      <Card>
        <CardHeader>
          <CardTitle>Informations du compte</CardTitle>
          <CardDescription>
            Détails de votre compte
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label className="text-gray-600">Statut du compte</Label>
              <p className="font-medium">
                {!user?.is_patient ? (
                  <span className="text-green-600">Actif</span>
                ) : (
                  <span className="text-red-600">Inactif</span>
                )}
              </p>
            </div>
            <div>
              <Label className="text-gray-600">Type de compte</Label>
              <p className="font-medium">
                {user?.role === 'super_admin' ? 'Super Administrateur' : user?.role || 'N/A'}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
