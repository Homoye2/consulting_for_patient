import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card'
import { Button } from '../../components/ui/button'
import { Input } from '../../components/ui/input'
import { Label } from '../../components/ui/label'
import { Badge } from '../../components/ui/badge'
import { Textarea } from '../../components/ui/textarea'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from '../../components/ui/table'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '../../components/ui/dialog'
import {
  Truck,
  Plus,
  Search,
  Edit,
  Trash2,
  CheckCircle,
  XCircle,
  UserPlus,
  Eye,
  Mail,
  Phone,
  MapPin
} from 'lucide-react'
import { fournisseursService } from '../../services/apiService'
import { AnimatedContainer } from '../../components/ui/animated-page'
import { format } from 'date-fns'
import { fr } from 'date-fns/locale'

export const Fournisseurs = () => {
  const [fournisseurs, setFournisseurs] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [showDialog, setShowDialog] = useState(false)
  const [showDetailDialog, setShowDetailDialog] = useState(false)
  const [selectedFournisseur, setSelectedFournisseur] = useState(null)
  const [isEditing, setIsEditing] = useState(false)
  const [formData, setFormData] = useState({
    nom: '',
    adresse: '',
    ville: '',
    pays: 'Sénégal',
    telephone: '',
    email: '',
    numero_registre_commerce: '',
    numero_identification_fiscale: '',
    delai_paiement_jours: 30,
    remise_habituelle: 0,
    notes: ''
  })

  useEffect(() => {
    fetchFournisseurs()
  }, [])

  const fetchFournisseurs = async () => {
    try {
      setLoading(true)
      const response = await fournisseursService.getAll()
      const data = Array.isArray(response.data) ? response.data : (response.data?.results || [])
      setFournisseurs(data)
    } catch (error) {
      console.error('Erreur lors du chargement des fournisseurs:', error)
      alert('Erreur lors du chargement des fournisseurs')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    try {
      if (isEditing && selectedFournisseur) {
        await fournisseursService.update(selectedFournisseur.id, formData)
        alert('Fournisseur modifié avec succès')
      } else {
        await fournisseursService.create(formData)
        alert('Fournisseur créé avec succès')
      }
      
      setShowDialog(false)
      resetForm()
      fetchFournisseurs()
    } catch (error) {
      console.error('Erreur:', error)
      alert('Erreur lors de l\'enregistrement')
    }
  }

  const handleEdit = (fournisseur) => {
    setSelectedFournisseur(fournisseur)
    setFormData({
      nom: fournisseur.nom,
      adresse: fournisseur.adresse,
      ville: fournisseur.ville,
      pays: fournisseur.pays,
      telephone: fournisseur.telephone,
      email: fournisseur.email || '',
      numero_registre_commerce: fournisseur.numero_registre_commerce || '',
      numero_identification_fiscale: fournisseur.numero_identification_fiscale || '',
      delai_paiement_jours: fournisseur.delai_paiement_jours,
      remise_habituelle: fournisseur.remise_habituelle,
      notes: fournisseur.notes || ''
    })
    setIsEditing(true)
    setShowDialog(true)
  }

  const handleDelete = async (id) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce fournisseur ?')) return
    
    try {
      await fournisseursService.delete(id)
      alert('Fournisseur supprimé avec succès')
      fetchFournisseurs()
    } catch (error) {
      console.error('Erreur:', error)
      alert('Erreur lors de la suppression')
    }
  }

  const handleToggleActif = async (fournisseur) => {
    try {
      if (fournisseur.actif) {
        await fournisseursService.desactiver(fournisseur.id)
        alert('Fournisseur désactivé avec succès')
      } else {
        await fournisseursService.activer(fournisseur.id)
        alert('Fournisseur activé avec succès')
      }
      fetchFournisseurs()
    } catch (error) {
      console.error('Erreur:', error)
      alert('Erreur lors de la modification du statut')
    }
  }

  const handleCreerCompte = async (fournisseur) => {
    if (!confirm(`Créer un compte utilisateur pour ${fournisseur.nom} ?`)) return
    
    try {
      const response = await fournisseursService.creerCompte(fournisseur.id)
      
      if (response.data.success) {
        alert(
          `Compte créé avec succès!\n\n` +
          `Email: ${response.data.email}\n` +
          `Mot de passe temporaire: ${response.data.temporary_password}\n\n` +
          `Veuillez noter ces informations et les transmettre au fournisseur.`
        )
      }
    } catch (error) {
      console.error('Erreur:', error)
      const errorMsg = error.response?.data?.error || 'Erreur lors de la création du compte'
      alert(errorMsg)
    }
  }

  const handleViewDetail = (fournisseur) => {
    setSelectedFournisseur(fournisseur)
    setShowDetailDialog(true)
  }

  const resetForm = () => {
    setFormData({
      nom: '',
      adresse: '',
      ville: '',
      pays: 'Sénégal',
      telephone: '',
      email: '',
      numero_registre_commerce: '',
      numero_identification_fiscale: '',
      delai_paiement_jours: 30,
      remise_habituelle: 0,
      notes: ''
    })
    setSelectedFournisseur(null)
    setIsEditing(false)
  }

  const filteredFournisseurs = fournisseurs.filter(f =>
    f.nom.toLowerCase().includes(searchTerm.toLowerCase()) ||
    f.ville.toLowerCase().includes(searchTerm.toLowerCase()) ||
    f.email?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const stats = {
    total: fournisseurs.length,
    actifs: fournisseurs.filter(f => f.actif).length,
    inactifs: fournisseurs.filter(f => !f.actif).length
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Chargement des fournisseurs...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 p-6">
      {/* En-tête */}
      <AnimatedContainer>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Gestion des Fournisseurs</h1>
            <p className="text-muted-foreground">
              Gérer les fournisseurs de produits pharmaceutiques
            </p>
          </div>
          <Button onClick={() => {
            resetForm()
            setShowDialog(true)
          }}>
            <Plus className="h-4 w-4 mr-2" />
            Nouveau Fournisseur
          </Button>
        </div>
      </AnimatedContainer>

      {/* Statistiques */}
      <AnimatedContainer>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Fournisseurs</CardTitle>
              <Truck className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.total}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Fournisseurs Actifs</CardTitle>
              <CheckCircle className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{stats.actifs}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Fournisseurs Inactifs</CardTitle>
              <XCircle className="h-4 w-4 text-red-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600">{stats.inactifs}</div>
            </CardContent>
          </Card>
        </div>
      </AnimatedContainer>

      {/* Liste des fournisseurs */}
      <AnimatedContainer>
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Liste des Fournisseurs</CardTitle>
                <CardDescription>
                  {filteredFournisseurs.length} fournisseur(s) trouvé(s)
                </CardDescription>
              </div>
              <div className="relative w-64">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Rechercher..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Nom</TableHead>
                    <TableHead>Contact</TableHead>
                    <TableHead>Localisation</TableHead>
                    <TableHead>Conditions</TableHead>
                    <TableHead>Statut</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredFournisseurs.map((fournisseur) => (
                    <TableRow key={fournisseur.id}>
                      <TableCell>
                        <div>
                          <div className="font-medium">{fournisseur.nom}</div>
                          {fournisseur.numero_identification_fiscale && (
                            <div className="text-sm text-muted-foreground">
                              NIF: {fournisseur.numero_identification_fiscale}
                            </div>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="space-y-1">
                          {fournisseur.email && (
                            <div className="flex items-center text-sm">
                              <Mail className="h-3 w-3 mr-1" />
                              {fournisseur.email}
                            </div>
                          )}
                          <div className="flex items-center text-sm">
                            <Phone className="h-3 w-3 mr-1" />
                            {fournisseur.telephone}
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center text-sm">
                          <MapPin className="h-3 w-3 mr-1" />
                          {fournisseur.ville}, {fournisseur.pays}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="text-sm">
                          <div>Délai: {fournisseur.delai_paiement_jours}j</div>
                          <div>Remise: {fournisseur.remise_habituelle}%</div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge variant={fournisseur.actif ? 'default' : 'secondary'}>
                          {fournisseur.actif ? 'Actif' : 'Inactif'}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center space-x-2">
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleViewDetail(fournisseur)}
                          >
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleEdit(fournisseur)}
                          >
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleToggleActif(fournisseur)}
                          >
                            {fournisseur.actif ? (
                              <XCircle className="h-4 w-4 text-red-600" />
                            ) : (
                              <CheckCircle className="h-4 w-4 text-green-600" />
                            )}
                          </Button>
                          {fournisseur.email && (
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => handleCreerCompte(fournisseur)}
                              title="Créer un compte utilisateur"
                            >
                              <UserPlus className="h-4 w-4" />
                            </Button>
                          )}
                          <Button
                            size="sm"
                            variant="destructive"
                            onClick={() => handleDelete(fournisseur.id)}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>

            {filteredFournisseurs.length === 0 && (
              <div className="text-center py-8">
                <Truck className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground">Aucun fournisseur trouvé</p>
              </div>
            )}
          </CardContent>
        </Card>
      </AnimatedContainer>

      {/* Dialog Créer/Modifier */}
      <Dialog open={showDialog} onOpenChange={setShowDialog}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>
              {isEditing ? 'Modifier le fournisseur' : 'Nouveau fournisseur'}
            </DialogTitle>
            <DialogDescription>
              Remplissez les informations du fournisseur
            </DialogDescription>
          </DialogHeader>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="col-span-2">
                <Label htmlFor="nom">Nom du fournisseur *</Label>
                <Input
                  id="nom"
                  value={formData.nom}
                  onChange={(e) => setFormData({ ...formData, nom: e.target.value })}
                  required
                />
              </div>

              <div className="col-span-2">
                <Label htmlFor="adresse">Adresse *</Label>
                <Textarea
                  id="adresse"
                  value={formData.adresse}
                  onChange={(e) => setFormData({ ...formData, adresse: e.target.value })}
                  required
                  rows={2}
                />
              </div>

              <div>
                <Label htmlFor="ville">Ville *</Label>
                <Input
                  id="ville"
                  value={formData.ville}
                  onChange={(e) => setFormData({ ...formData, ville: e.target.value })}
                  required
                />
              </div>

              <div>
                <Label htmlFor="pays">Pays *</Label>
                <Input
                  id="pays"
                  value={formData.pays}
                  onChange={(e) => setFormData({ ...formData, pays: e.target.value })}
                  required
                />
              </div>

              <div>
                <Label htmlFor="telephone">Téléphone *</Label>
                <Input
                  id="telephone"
                  value={formData.telephone}
                  onChange={(e) => setFormData({ ...formData, telephone: e.target.value })}
                  required
                />
              </div>

              <div>
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                />
              </div>

              <div>
                <Label htmlFor="numero_registre_commerce">N° Registre Commerce</Label>
                <Input
                  id="numero_registre_commerce"
                  value={formData.numero_registre_commerce}
                  onChange={(e) => setFormData({ ...formData, numero_registre_commerce: e.target.value })}
                />
              </div>

              <div>
                <Label htmlFor="numero_identification_fiscale">NIF</Label>
                <Input
                  id="numero_identification_fiscale"
                  value={formData.numero_identification_fiscale}
                  onChange={(e) => setFormData({ ...formData, numero_identification_fiscale: e.target.value })}
                />
              </div>

              <div>
                <Label htmlFor="delai_paiement_jours">Délai de paiement (jours)</Label>
                <Input
                  id="delai_paiement_jours"
                  type="number"
                  value={formData.delai_paiement_jours}
                  onChange={(e) => setFormData({ ...formData, delai_paiement_jours: parseInt(e.target.value) })}
                  min="0"
                />
              </div>

              <div>
                <Label htmlFor="remise_habituelle">Remise habituelle (%)</Label>
                <Input
                  id="remise_habituelle"
                  type="number"
                  step="0.01"
                  value={formData.remise_habituelle}
                  onChange={(e) => setFormData({ ...formData, remise_habituelle: parseFloat(e.target.value) })}
                  min="0"
                  max="100"
                />
              </div>

              <div className="col-span-2">
                <Label htmlFor="notes">Notes</Label>
                <Textarea
                  id="notes"
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  rows={3}
                />
              </div>
            </div>

            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setShowDialog(false)}>
                Annuler
              </Button>
              <Button type="submit">
                {isEditing ? 'Modifier' : 'Créer'}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Dialog Détails */}
      <Dialog open={showDetailDialog} onOpenChange={setShowDetailDialog}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Détails du fournisseur</DialogTitle>
          </DialogHeader>

          {selectedFournisseur && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label className="text-sm font-medium">Nom</Label>
                  <p className="text-sm text-muted-foreground">{selectedFournisseur.nom}</p>
                </div>

                <div>
                  <Label className="text-sm font-medium">Statut</Label>
                  <div className="mt-1">
                    <Badge variant={selectedFournisseur.actif ? 'default' : 'secondary'}>
                      {selectedFournisseur.actif ? 'Actif' : 'Inactif'}
                    </Badge>
                  </div>
                </div>

                <div className="col-span-2">
                  <Label className="text-sm font-medium">Adresse</Label>
                  <p className="text-sm text-muted-foreground">{selectedFournisseur.adresse}</p>
                </div>

                <div>
                  <Label className="text-sm font-medium">Ville</Label>
                  <p className="text-sm text-muted-foreground">{selectedFournisseur.ville}</p>
                </div>

                <div>
                  <Label className="text-sm font-medium">Pays</Label>
                  <p className="text-sm text-muted-foreground">{selectedFournisseur.pays}</p>
                </div>

                <div>
                  <Label className="text-sm font-medium">Téléphone</Label>
                  <p className="text-sm text-muted-foreground">{selectedFournisseur.telephone}</p>
                </div>

                <div>
                  <Label className="text-sm font-medium">Email</Label>
                  <p className="text-sm text-muted-foreground">{selectedFournisseur.email || 'N/A'}</p>
                </div>

                {selectedFournisseur.numero_registre_commerce && (
                  <div>
                    <Label className="text-sm font-medium">N° Registre Commerce</Label>
                    <p className="text-sm text-muted-foreground">{selectedFournisseur.numero_registre_commerce}</p>
                  </div>
                )}

                {selectedFournisseur.numero_identification_fiscale && (
                  <div>
                    <Label className="text-sm font-medium">NIF</Label>
                    <p className="text-sm text-muted-foreground">{selectedFournisseur.numero_identification_fiscale}</p>
                  </div>
                )}

                <div>
                  <Label className="text-sm font-medium">Délai de paiement</Label>
                  <p className="text-sm text-muted-foreground">{selectedFournisseur.delai_paiement_jours} jours</p>
                </div>

                <div>
                  <Label className="text-sm font-medium">Remise habituelle</Label>
                  <p className="text-sm text-muted-foreground">{selectedFournisseur.remise_habituelle}%</p>
                </div>

                {selectedFournisseur.notes && (
                  <div className="col-span-2">
                    <Label className="text-sm font-medium">Notes</Label>
                    <p className="text-sm text-muted-foreground">{selectedFournisseur.notes}</p>
                  </div>
                )}

                <div>
                  <Label className="text-sm font-medium">Date de création</Label>
                  <p className="text-sm text-muted-foreground">
                    {format(new Date(selectedFournisseur.created_at), 'dd MMM yyyy', { locale: fr })}
                  </p>
                </div>

                <div>
                  <Label className="text-sm font-medium">Dernière modification</Label>
                  <p className="text-sm text-muted-foreground">
                    {format(new Date(selectedFournisseur.updated_at), 'dd MMM yyyy', { locale: fr })}
                  </p>
                </div>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  )
}
