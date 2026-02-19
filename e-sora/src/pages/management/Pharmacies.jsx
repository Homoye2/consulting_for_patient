import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { pharmaciesService } from '../../services/apiService'
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
import { Badge } from '../../components/ui/badge'
import { Plus, Search, Edit, Trash2, Pill, MapPin, Phone, Mail, Eye, Key, CheckCircle, XCircle, Activity } from 'lucide-react'
import { AnimatedContainer, AnimatedStagger } from '../../components/ui/animated-page'
import { useToast } from '../../components/ui/toast'

export const Pharmacies = () => {
  const [pharmacies, setPharmacies] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editingPharmacie, setEditingPharmacie] = useState(null)
  const { showToast, ToastContainer } = useToast()
  const [formData, setFormData] = useState({
    nom: '',
    adresse: '',
    ville: '',
    pays: 'Sénégal',
    telephone: '',
    email: '',
    description: '',
    actif: true
  })

  // Statistiques
  const stats = {
    total: pharmacies.length,
    actives: pharmacies.filter(p => p.actif).length,
    inactives: pharmacies.filter(p => !p.actif).length
  }

  useEffect(() => {
    fetchPharmacies()
  }, [searchTerm])

  const fetchPharmacies = async () => {
    try {
      setLoading(true)
      const params = searchTerm ? { search: searchTerm } : {}
      const response = await pharmaciesService.getAll(params)
      console.log("pharmacie :",response)
      setPharmacies(response.data.results || response.data)
    } catch (error) {
      console.error('Erreur lors du chargement des pharmacies:', error)
      if (error.response?.status === 403) {
        showToast('Vous n\'avez pas les permissions nécessaires pour accéder aux pharmacies.', 'error')
        setPharmacies([])
      } else {
        showToast('Erreur lors du chargement des pharmacies', 'error')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editingPharmacie) {
        await pharmaciesService.update(editingPharmacie.id, formData)
        showToast('Pharmacie modifiée avec succès', 'success')
      } else {
        await pharmaciesService.create(formData)
        showToast('Pharmacie créée avec succès. Mot de passe par défaut: admin123', 'success')
      }
      setDialogOpen(false)
      resetForm()
      fetchPharmacies()
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error)
      showToast(error.response?.data?.error || 'Erreur lors de la sauvegarde', 'error')
    }
  }

  const handleEdit = (pharmacie) => {
    setEditingPharmacie(pharmacie)
    setFormData({
      nom: pharmacie.nom,
      adresse: pharmacie.adresse || '',
      ville: pharmacie.ville || '',
      pays: pharmacie.pays || 'Sénégal',
      telephone: pharmacie.telephone || '',
      email: pharmacie.email || '',
      description: pharmacie.description || '',
      actif: pharmacie.actif
    })
    setDialogOpen(true)
  }

  const handleDelete = async (id) => {
    if (confirm('Êtes-vous sûr de vouloir supprimer cette pharmacie ?')) {
      try {
        await pharmaciesService.delete(id)
        showToast('Pharmacie supprimée avec succès', 'success')
        fetchPharmacies()
      } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        showToast('Erreur lors de la suppression', 'error')
      }
    }
  }

  const handleToggleStatus = async (pharmacie) => {
    try {
      let response;
      if (pharmacie.actif) {
        response = await pharmaciesService.suspendre(pharmacie.id)
        showToast(response.data.message || 'Pharmacie suspendue avec succès', 'success')
      } else {
        response = await pharmaciesService.activer(pharmacie.id)
        showToast(response.data.message || 'Pharmacie activée avec succès', 'success')
      }
      fetchPharmacies()
    } catch (error) {
      console.error('Erreur lors du changement de statut:', error)
      showToast('Erreur lors du changement de statut', 'error')
    }
  }

  const handleResetPassword = async (pharmacie) => {
    if (confirm(`Réinitialiser le mot de passe de l'administrateur de ${pharmacie.nom} ?\nLe nouveau mot de passe sera: admin123`)) {
      try {
        await pharmaciesService.resetAdminPassword(pharmacie.id)
        showToast('Mot de passe réinitialisé avec succès (admin123)', 'success')
      } catch (error) {
        console.error('Erreur lors de la réinitialisation:', error)
        showToast(error.response?.data?.error || 'Erreur lors de la réinitialisation', 'error')
      }
    }
  }

  const resetForm = () => {
    setFormData({
      nom: '',
      adresse: '',
      ville: '',
      pays: 'Sénégal',
      telephone: '',
      email: '',
      description: '',
      actif: true
    })
    setEditingPharmacie(null)
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
            <h1 className="text-3xl font-bold">Gestion des Pharmacies</h1>
            <p className="text-muted-foreground mt-2">
              Gérez les pharmacies partenaires du réseau
            </p>
          </div>
          <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
            <DialogTrigger asChild>
              <Button onClick={resetForm}>
                <Plus className="h-4 w-4 mr-2" />
                Nouvelle Pharmacie
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[600px]">
              <DialogHeader>
                <DialogTitle>
                  {editingPharmacie ? 'Modifier la pharmacie' : 'Nouvelle pharmacie'}
                </DialogTitle>
                <DialogDescription>
                  {editingPharmacie 
                    ? 'Modifiez les informations de la pharmacie'
                    : 'Ajoutez une nouvelle pharmacie partenaire. Un compte administrateur sera créé automatiquement.'
                  }
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="nom">Nom de la pharmacie *</Label>
                    <Input
                      id="nom"
                      value={formData.nom}
                      onChange={(e) => handleInputChange('nom', e.target.value)}
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
                      placeholder="admin@pharmacie.com"
                    />
                    <p className="text-xs text-muted-foreground mt-1">
                      Utilisé pour la connexion de l'administrateur
                    </p>
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
                    <Label htmlFor="ville">Ville</Label>
                    <Input
                      id="ville"
                      value={formData.ville}
                      onChange={(e) => handleInputChange('ville', e.target.value)}
                      placeholder="Dakar"
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
                  <Label htmlFor="telephone">Téléphone *</Label>
                  <Input
                    id="telephone"
                    value={formData.telephone}
                    onChange={(e) => handleInputChange('telephone', e.target.value)}
                    required
                  />
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
                  <Label htmlFor="actif">Pharmacie active</Label>
                </div>
                {!editingPharmacie && (
                  <div className="bg-blue-50 border border-blue-200 p-3 rounded">
                    <p className="text-sm text-blue-800">
                      <strong>Note:</strong> Un compte administrateur sera créé avec l'email fourni et le mot de passe par défaut: <strong>admin123</strong>
                    </p>
                  </div>
                )}
                <DialogFooter>
                  <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>
                    Annuler
                  </Button>
                  <Button type="submit">
                    {editingPharmacie ? 'Modifier' : 'Créer'}
                  </Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </div>
      </AnimatedContainer>

      {/* Statistiques */}
      <AnimatedStagger className="grid grid-cols-1 md:grid-cols-3 gap-6" staggerDelay={0.1}>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Pharmacies</CardTitle>
            <Pill className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total}</div>
            <p className="text-xs text-muted-foreground">Pharmacies enregistrées</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pharmacies Actives</CardTitle>
            <CheckCircle className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{stats.actives}</div>
            <p className="text-xs text-muted-foreground">En activité</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pharmacies Inactives</CardTitle>
            <XCircle className="h-4 w-4 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">{stats.inactives}</div>
            <p className="text-xs text-muted-foreground">Suspendues</p>
          </CardContent>
        </Card>
      </AnimatedStagger>

      <AnimatedContainer delay={0.1}>
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Pill className="h-5 w-5" />
              Liste des Pharmacies ({pharmacies.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-2 mb-4">
              <Search className="h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Rechercher une pharmacie..."
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
                    <TableHead>Administrateur</TableHead>
                    <TableHead>Contact</TableHead>
                    <TableHead>Localisation</TableHead>
                    <TableHead>Statut</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {pharmacies.map((pharmacie) => (
                    <TableRow key={pharmacie.id}>
                      <TableCell className="font-medium">
                        <div className="flex items-center gap-2">
                          <Pill className="h-4 w-4 text-muted-foreground" />
                          {pharmacie.nom}
                        </div>
                      </TableCell>
                      <TableCell>
                        {pharmacie.user_email ? (
                          <div className="flex items-center gap-1 text-sm">
                            <Mail className="h-3 w-3" />
                            {pharmacie.user_email}
                          </div>
                        ) : (
                          <span className="text-xs text-muted-foreground italic">Non assigné</span>
                        )}
                      </TableCell>
                      <TableCell>
                        <div className="space-y-1">
                          {pharmacie.telephone && (
                            <div className="flex items-center gap-1 text-sm">
                              <Phone className="h-3 w-3" />
                              {pharmacie.telephone}
                            </div>
                          )}
                          {pharmacie.email && (
                            <div className="flex items-center gap-1 text-sm">
                              <Mail className="h-3 w-3" />
                              {pharmacie.email}
                            </div>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        {pharmacie.adresse && (
                          <div className="flex items-center gap-1 text-sm">
                            <MapPin className="h-3 w-3" />
                            <div>
                              {pharmacie.adresse}
                              {pharmacie.ville && <div className="text-xs text-muted-foreground">{pharmacie.ville}</div>}
                            </div>
                          </div>
                        )}
                      </TableCell>
                      <TableCell>
                        <Badge variant={pharmacie.actif ? 'default' : 'secondary'} className={
                          pharmacie.actif 
                            ? 'bg-green-100 text-green-800 hover:bg-green-200' 
                            : 'bg-red-100 text-red-800 hover:bg-red-200'
                        }>
                          {pharmacie.actif ? (
                            <>
                              <CheckCircle className="h-3 w-3 mr-1" />
                              Active
                            </>
                          ) : (
                            <>
                              <XCircle className="h-3 w-3 mr-1" />
                              Inactive
                            </>
                          )}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex items-center justify-end gap-2">
                          <Link to={`/pharmacies/${pharmacie.id}`}>
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
                            onClick={() => handleEdit(pharmacie)}
                            title="Modifier"
                          >
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleToggleStatus(pharmacie)}
                            title={pharmacie.actif ? 'Suspendre' : 'Activer'}
                          >
                            {pharmacie.actif ? (
                              <XCircle className="h-4 w-4 text-red-600" />
                            ) : (
                              <CheckCircle className="h-4 w-4 text-green-600" />
                            )}
                          </Button>
                          {pharmacie.user_email && (
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => handleResetPassword(pharmacie)}
                              title="Réinitialiser le mot de passe"
                            >
                              <Key className="h-4 w-4 text-blue-600" />
                            </Button>
                          )}
                          <Button
                            variant="destructive"
                            size="sm"
                            onClick={() => handleDelete(pharmacie.id)}
                            title="Supprimer"
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
              {pharmacies.length === 0 && (
                <div className="text-center py-8">
                  <Pill className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-muted-foreground">
                    {searchTerm ? 'Aucune pharmacie trouvée' : 'Aucune pharmacie enregistrée'}
                  </p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </AnimatedContainer>
      
      <ToastContainer />
    </div>
  )
}