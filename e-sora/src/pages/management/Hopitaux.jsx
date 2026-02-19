import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { hopitauxService } from '../../services/apiService'
import { Button } from '../../components/ui/button'
import { Input } from '../../components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../../components/ui/table'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '../../components/ui/dialog'
import { Label } from '../../components/ui/label'
import { Textarea } from '../../components/ui/textarea'
import { Plus, Search, Edit, Trash2, Building2, MapPin, Phone, Mail, Eye, Key, CheckCircle, XCircle } from 'lucide-react'
import { AnimatedContainer } from '../../components/ui/animated-page'

export const Hopitaux = () => {
  const [hopitaux, setHopitaux] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editingHopital, setEditingHopital] = useState(null)
  const [formData, setFormData] = useState({
    nom: '',
    code_hopital: '',
    adresse: '',
    ville: '',
    pays: 'Sénégal',
    telephone: '',
    email: '',
    description: '',
    actif: true
  })

  useEffect(() => {
    fetchHopitaux()
  }, [searchTerm])

  const fetchHopitaux = async () => {
    try {
      setLoading(true)
      const params = searchTerm ? { search: searchTerm } : {}
      const response = await hopitauxService.getAll(params)
      setHopitaux(response.data.results || response.data)

    } catch (error) {
      console.error('Erreur lors du chargement des hôpitaux:', error)
      if (error.response?.status === 403) {
        alert('Vous n\'avez pas les permissions nécessaires pour accéder aux hôpitaux.')
        setHopitaux([])
      }
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editingHopital) {
        await hopitauxService.update(editingHopital.id, formData)
      } else {
        await hopitauxService.create(formData)
      }
      setDialogOpen(false)
      resetForm()
      fetchHopitaux()
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error)
      
      // Afficher les erreurs spécifiques du serveur
      if (error.response?.data) {
        const errors = error.response.data
        let errorMessage = 'Erreur lors de la sauvegarde:\n'
        
        if (typeof errors === 'object') {
          Object.keys(errors).forEach(field => {
            if (Array.isArray(errors[field])) {
              errorMessage += `${field}: ${errors[field].join(', ')}\n`
            } else {
              errorMessage += `${field}: ${errors[field]}\n`
            }
          })
        } else {
          errorMessage += errors
        }
        
        alert(errorMessage)
      } else {
        alert('Erreur lors de la sauvegarde')
      }
    }
  }

  const handleEdit = (hopital) => {
    setEditingHopital(hopital)
    setFormData({
      nom: hopital.nom,
      code_hopital: hopital.code_hopital || '',
      adresse: hopital.adresse || '',
      ville: hopital.ville || '',
      pays: hopital.pays || 'Sénégal',
      telephone: hopital.telephone || '',
      email: hopital.email || '',
      description: hopital.description || '',
      actif: hopital.actif
    })
    setDialogOpen(true)
  }

  const handleDelete = async (id) => {
    if (confirm('Êtes-vous sûr de vouloir supprimer cet hôpital ?')) {
      try {
        await hopitauxService.delete(id)
        fetchHopitaux()
      } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        alert('Erreur lors de la suppression')
      }
    }
  }

  const handleResetPassword = async (hopital) => {
    if (confirm(`Êtes-vous sûr de vouloir réinitialiser le mot de passe de l'administrateur de ${hopital.nom} ?\n\nLe nouveau mot de passe sera "admin123".`)) {
      try {
        const response = await hopitauxService.resetAdminPassword(hopital.id)
        alert(`Mot de passe réinitialisé avec succès !\n\nEmail: ${response.data.admin_email}\nMot de passe: admin123`)
      } catch (error) {
        console.error('Erreur lors de la réinitialisation:', error)
        if (error.response?.data?.error) {
          alert(`Erreur: ${error.response.data.error}`)
        } else {
          alert('Erreur lors de la réinitialisation du mot de passe')
        }
      }
    }
  }

  const handleToggleStatus = async (hopital) => {
    try {
      let response;
      if (hopital.actif) {
        response = await hopitauxService.suspendre(hopital.id)
        alert(response.data.message || 'Hôpital suspendu avec succès')
      } else {
        response = await hopitauxService.activer(hopital.id)
        alert(response.data.message || 'Hôpital activé avec succès')
      }
      fetchHopitaux()
    } catch (error) {
      console.error('Erreur lors du changement de statut:', error)
      if (error.response?.data?.error) {
        alert(`Erreur: ${error.response.data.error}`)
      } else {
        alert('Erreur lors du changement de statut')
      }
    }
  }

  const resetForm = () => {
    setFormData({
      nom: '',
      code_hopital: '',
      adresse: '',
      ville: '',
      pays: 'Sénégal',
      telephone: '',
      email: '',
      description: '',
      actif: true
    })
    setEditingHopital(null)
  }

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <AnimatedContainer>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Gestion des Hôpitaux</h1>
            <p className="text-muted-foreground mt-2">
              Gérez les établissements hospitaliers du réseau
            </p>
          </div>
          <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
            <DialogTrigger asChild>
              <Button onClick={resetForm}>
                <Plus className="h-4 w-4 mr-2" />
                Nouvel Hôpital
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[600px]">
              <DialogHeader>
                <DialogTitle>
                  {editingHopital ? 'Modifier l\'hôpital' : 'Nouvel hôpital'}
                </DialogTitle>
                <DialogDescription>
                  {editingHopital 
                    ? 'Modifiez les informations de l\'hôpital'
                    : 'Ajoutez un nouvel établissement hospitalier'
                  }
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="nom">Nom de l'hôpital *</Label>
                    <Input
                      id="nom"
                      value={formData.nom}
                      onChange={(e) => handleInputChange('nom', e.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="code_hopital">Code hôpital *</Label>
                    <Input
                      id="code_hopital"
                      value={formData.code_hopital}
                      onChange={(e) => handleInputChange('code_hopital', e.target.value)}
                      placeholder="Ex: CHAND001"
                      required
                    />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="ville">Ville *</Label>
                    <Input
                      id="ville"
                      value={formData.ville}
                      onChange={(e) => handleInputChange('ville', e.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="pays">Pays</Label>
                    <Input
                      id="pays"
                      value={formData.pays}
                      onChange={(e) => handleInputChange('pays', e.target.value)}
                    />
                  </div>
                </div>
                <div>
                  <Label htmlFor="adresse">Adresse *</Label>
                  <Input
                    id="adresse"
                    value={formData.adresse}
                    onChange={(e) => handleInputChange('adresse', e.target.value)}
                    required
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="telephone">Téléphone *</Label>
                    <Input
                      id="telephone"
                      value={formData.telephone}
                      onChange={(e) => handleInputChange('telephone', e.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="email">Email *</Label>
                    <Input
                      id="email"
                      type="email"
                      value={formData.email}
                      onChange={(e) => handleInputChange('email', e.target.value)}
                      required
                    />
                  </div>
                </div>
                <div>
                  <Label htmlFor="description">Description</Label>
                  <Textarea
                    id="description"
                    value={formData.description}
                    onChange={(e) => handleInputChange('description', e.target.value)}
                    rows={3}
                  />
                </div>
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="actif"
                    checked={formData.actif}
                    onChange={(e) => handleInputChange('actif', e.target.checked)}
                  />
                  <Label htmlFor="actif">Hôpital actif</Label>
                </div>
                <DialogFooter>
                  <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>
                    Annuler
                  </Button>
                  <Button type="submit">
                    {editingHopital ? 'Modifier' : 'Créer'}
                  </Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </div>
      </AnimatedContainer>

      <AnimatedContainer delay={0.1}>
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Building2 className="h-5 w-5" />
              Liste des Hôpitaux ({hopitaux.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-2 mb-4">
              <Search className="h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Rechercher un hôpital..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="max-w-sm"
              />
            </div>
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Nom</TableHead>
                    <TableHead>Contact</TableHead>
                    <TableHead>Adresse</TableHead>
                    <TableHead>Administrateur</TableHead>
                    <TableHead>Statut</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {hopitaux.map((hopital) => (
                    <TableRow key={hopital.id}>
                      <TableCell className="font-medium">
                        <div className="flex items-center gap-2">
                          <Building2 className="h-4 w-4 text-muted-foreground" />
                          <div>
                            <div>{hopital.nom}</div>
                            {hopital.code_hopital && (
                              <div className="text-xs text-muted-foreground">
                                Code: {hopital.code_hopital}
                              </div>
                            )}
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="space-y-1">
                          {hopital.telephone && (
                            <div className="flex items-center gap-1 text-sm">
                              <Phone className="h-3 w-3" />
                              {hopital.telephone}
                            </div>
                          )}
                          {hopital.email && (
                            <div className="flex items-center gap-1 text-sm">
                              <Mail className="h-3 w-3" />
                              {hopital.email}
                            </div>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="space-y-1">
                          {hopital.adresse && (
                            <div className="text-sm">{hopital.adresse}</div>
                          )}
                          {hopital.ville && (
                            <div className="flex items-center gap-1 text-sm text-muted-foreground">
                              <MapPin className="h-3 w-3" />
                              {hopital.ville}
                            </div>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        {hopital.admin_hopital_email ? (
                          <div className="text-sm">
                            <div className="font-medium">{hopital.admin_hopital_nom || 'Admin'}</div>
                            <div className="text-muted-foreground">{hopital.admin_hopital_email}</div>
                          </div>
                        ) : (
                          <span className="text-sm text-muted-foreground">Aucun admin</span>
                        )}
                      </TableCell>
                      <TableCell>
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                          hopital.actif 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {hopital.actif ? 'Actif' : 'Inactif'}
                        </span>
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex items-center justify-end gap-2">
                          <Link to={`/hopitaux/${hopital.id}`}>
                            <Button
                              variant="outline"
                              size="sm"
                              title="Voir les détails"
                            >
                              <Eye className="h-4 w-4" />
                            </Button>
                          </Link>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleEdit(hopital)}
                            title="Modifier l'hôpital"
                          >
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleToggleStatus(hopital)}
                            title={hopital.actif ? 'Suspendre l\'hôpital' : 'Activer l\'hôpital'}
                          >
                            {hopital.actif ? (
                              <XCircle className="h-4 w-4 text-red-600" />
                            ) : (
                              <CheckCircle className="h-4 w-4 text-green-600" />
                            )}
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleResetPassword(hopital)}
                            title="Réinitialiser le mot de passe admin"
                            className="text-orange-600 hover:text-orange-700"
                          >
                            <Key className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="destructive"
                            size="sm"
                            onClick={() => handleDelete(hopital.id)}
                            title="Supprimer l'hôpital"
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
              {hopitaux.length === 0 && (
                <div className="text-center py-8">
                  <Building2 className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-muted-foreground">
                    {searchTerm ? 'Aucun hôpital trouvé' : 'Aucun hôpital enregistré'}
                  </p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </AnimatedContainer>
    </div>
  )
}