import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card'
import { Button } from '../../components/ui/button'
import { Input } from '../../components/ui/input'
import { Label } from '../../components/ui/label'
import { Textarea } from '../../components/ui/textarea'
import { Save, Loader2, User } from 'lucide-react'
import { useAuth } from '../../contexts/AuthContext'
import { patientsService, usersService } from '../../services/apiService'

export const PatientProfile = () => {
  const { user } = useAuth()
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [patientData, setPatientData] = useState(null)
  const [formData, setFormData] = useState({
    nom: '',
    prenom: '',
    dob: '',
    sexe: 'F',
    telephone: '',
    email: '',
    adresse: '',
    antecedents: '',
    allergies: '',
  })

  useEffect(() => {
    fetchPatientData()
  }, [])

  const fetchPatientData = async () => {
    try {
      setLoading(true)
      // Récupérer les données du patient via l'utilisateur connecté
      const userData = JSON.parse(localStorage.getItem('user'))
      const patientId = userData?.patient_id

      if (patientId) {
        const response = await patientsService.getById(patientId)
        const patient = response.data
        setPatientData(patient)
        setFormData({
          nom: patient.nom || '',
          prenom: patient.prenom || '',
          dob: patient.dob ? patient.dob.split('T')[0] : '',
          sexe: patient.sexe || 'F',
          telephone: patient.telephone || '',
          email: patient.email || user?.email || '',
          adresse: patient.adresse || '',
          antecedents: patient.antecedents || '',
          allergies: patient.allergies || '',
        })
      }
    } catch (error) {
      console.error('Erreur lors du chargement du profil:', error)
      alert('Erreur lors du chargement du profil')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      setSaving(true)
      const userData = JSON.parse(localStorage.getItem('user'))
      const patientId = userData?.patient_id

      if (!patientId) {
        alert('Erreur: Profil patient non trouvé')
        return
      }

      // Mettre à jour le patient
      await patientsService.update(patientId, formData)

      // Mettre à jour aussi l'email de l'utilisateur si changé
      if (formData.email !== user?.email) {
        try {
          await usersService.update(user.id, { email: formData.email })
        } catch (error) {
          console.error('Erreur lors de la mise à jour de l\'email:', error)
        }
      }

      alert('Profil mis à jour avec succès !')
      // Recharger les données
      await fetchPatientData()
    } catch (error) {
      console.error('Erreur lors de la mise à jour:', error)
      alert('Erreur lors de la mise à jour du profil')
    } finally {
      setSaving(false)
    }
  }

  const handleChange = (field, value) => {
    setFormData({ ...formData, [field]: value })
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-3xl md:text-4xl font-bold mb-2">Mon profil</h1>
        <p className="text-muted-foreground">
          Gérez vos informations personnelles
        </p>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="grid gap-6 md:grid-cols-2">
          {/* Informations personnelles */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="h-5 w-5" />
                Informations personnelles
              </CardTitle>
              <CardDescription>Vos informations de base</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="nom">Nom</Label>
                  <Input
                    id="nom"
                    value={formData.nom}
                    onChange={(e) => handleChange('nom', e.target.value)}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="prenom">Prénom</Label>
                  <Input
                    id="prenom"
                    value={formData.prenom}
                    onChange={(e) => handleChange('prenom', e.target.value)}
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="dob">Date de naissance</Label>
                  <Input
                    id="dob"
                    type="date"
                    value={formData.dob}
                    onChange={(e) => handleChange('dob', e.target.value)}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="sexe">Sexe</Label>
                  <select
                    id="sexe"
                    value={formData.sexe}
                    onChange={(e) => handleChange('sexe', e.target.value)}
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    required
                  >
                    <option value="F">Féminin</option>
                    <option value="M">Masculin</option>
                  </select>
                </div>
              </div>

              <div>
                <Label htmlFor="telephone">Téléphone</Label>
                <Input
                  id="telephone"
                  value={formData.telephone}
                  onChange={(e) => handleChange('telephone', e.target.value)}
                  placeholder="+221 77 123 45 67"
                />
              </div>

              <div>
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => handleChange('email', e.target.value)}
                  required
                />
              </div>

              <div>
                <Label htmlFor="adresse">Adresse</Label>
                <Textarea
                  id="adresse"
                  value={formData.adresse}
                  onChange={(e) => handleChange('adresse', e.target.value)}
                  rows={3}
                  placeholder="Votre adresse complète"
                />
              </div>
            </CardContent>
          </Card>

          {/* Informations médicales */}
          <Card>
            <CardHeader>
              <CardTitle>Informations médicales</CardTitle>
              <CardDescription>Vos antécédents et allergies</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="antecedents">Antécédents médicaux</Label>
                <Textarea
                  id="antecedents"
                  value={formData.antecedents}
                  onChange={(e) => handleChange('antecedents', e.target.value)}
                  rows={5}
                  placeholder="Listez vos antécédents médicaux (maladies chroniques, interventions chirurgicales, etc.)"
                />
              </div>

              <div>
                <Label htmlFor="allergies">Allergies</Label>
                <Textarea
                  id="allergies"
                  value={formData.allergies}
                  onChange={(e) => handleChange('allergies', e.target.value)}
                  rows={4}
                  placeholder="Listez vos allergies (médicaments, aliments, etc.)"
                />
              </div>

              {patientData && (
                <div className="pt-4 border-t">
                  <div className="text-sm text-muted-foreground">
                    <p><strong>Âge:</strong> {patientData.age} ans</p>
                    <p className="mt-2"><strong>Membre depuis:</strong> {new Date(patientData.created_at).toLocaleDateString('fr-FR')}</p>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        <div className="mt-6 flex justify-end gap-4">
          <Button
            type="button"
            variant="outline"
            onClick={() => fetchPatientData()}
          >
            Annuler
          </Button>
          <Button type="submit" disabled={saving}>
            {saving ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Sauvegarde...
              </>
            ) : (
              <>
                <Save className="mr-2 h-4 w-4" />
                Enregistrer les modifications
              </>
            )}
          </Button>
        </div>
      </form>
    </div>
  )
}

