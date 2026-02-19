import { useState, useEffect } from 'react'
import { stocksService, produitsService } from '../../services/apiService'
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
import { Plus, Search, Edit, Trash2, AlertTriangle } from 'lucide-react'

export const Stocks = () => {
  const [stocks, setStocks] = useState([])
  const [produits, setProduits] = useState([])
  const [alertes, setAlertes] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editingStock, setEditingStock] = useState(null)
  const [formData, setFormData] = useState({
    produit: '',
    quantite: '',
    seuil_alerte: '',
    numero_lot: '',
    date_expiration: '',
    prix_vente: '',
  })

  useEffect(() => {
    fetchStocks()
    fetchProduits()
    fetchAlertes()
  }, [searchTerm])

  const fetchStocks = async () => {
    try {
      setLoading(true)
      const params = searchTerm ? { search: searchTerm } : {}
      const response = await stocksService.getAll(params)
      setStocks(response.data.results || response.data)
    } catch (error) {
      console.error('Erreur lors du chargement des stocks:', error)
      if (error.response?.status === 403) {
        alert('Vous n\'avez pas les permissions nécessaires pour accéder aux stocks. Contactez l\'administrateur.')
        setStocks([])
      }
    } finally {
      setLoading(false)
    }
  }

  const fetchProduits = async () => {
    try {
      const response = await produitsService.getAll()
      setProduits(response.data.results || response.data)
    } catch (error) {
      console.error('Erreur lors du chargement des produits:', error)
      if (error.response?.status === 403) {
        alert('Permissions insuffisantes pour charger les produits.')
        setProduits([])
      }
    }
  }

  const fetchAlertes = async () => {
    try {
      const response = await stocksService.getAlertes()
      setAlertes(response.data)
    } catch (error) {
      console.error('Erreur lors du chargement des alertes:', error)
      if (error.response?.status === 403) {
        console.warn('Permissions insuffisantes pour charger les alertes de stock.')
        setAlertes([])
      }
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const data = {
        ...formData,
        produit: parseInt(formData.produit),
        quantite: parseInt(formData.quantite),
        seuil_alerte: parseInt(formData.seuil_alerte),
        prix_vente: parseFloat(formData.prix_vente),
      }
      if (editingStock) {
        await stocksService.update(editingStock.id, data)
      } else {
        await stocksService.create(data)
      }
      setDialogOpen(false)
      resetForm()
      fetchStocks()
      fetchAlertes()
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error)
      alert('Erreur lors de la sauvegarde')
    }
  }

  const handleEdit = (stock) => {
    setEditingStock(stock)
    setFormData({
      produit: stock.produit?.id || stock.produit || '',
      quantite: stock.quantite || '',
      seuil_alerte: stock.seuil_alerte || '',
      numero_lot: stock.numero_lot || '',
      date_expiration: stock.date_expiration || '',
      prix_vente: stock.prix_vente || '',
    })
    setDialogOpen(true)
  }

  const handleDelete = async (id) => {
    if (confirm('Êtes-vous sûr de vouloir supprimer ce stock ?')) {
      try {
        await stocksService.delete(id)
        fetchStocks()
        fetchAlertes()
      } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        alert('Erreur lors de la suppression')
      }
    }
  }

  const resetForm = () => {
    setEditingStock(null)
    setFormData({
      produit: '',
      quantite: '',
      seuil_alerte: '',
      numero_lot: '',
      date_expiration: '',
      prix_vente: '',
    })
  }

  const isStockLow = (stock) => {
    return stock.quantite <= stock.seuil_alerte
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold">Stocks</h1>
          <p className="text-muted-foreground mt-2">
            Gestion des stocks de produits pharmaceutiques
          </p>
        </div>
        <Dialog open={dialogOpen} onOpenChange={(open) => {
          setDialogOpen(open)
          if (!open) resetForm()
        }}>
          <DialogTrigger asChild>
            <Button onClick={() => resetForm()}>
              <Plus className="h-4 w-4 mr-2" />
              Nouveau stock
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>
                {editingStock ? 'Modifier le stock' : 'Nouveau stock'}
              </DialogTitle>
              <DialogDescription>
                Remplissez les informations du stock
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="produit">Produit *</Label>
                <select
                  id="produit"
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  value={formData.produit}
                  onChange={(e) => setFormData({ ...formData, produit: e.target.value })}
                  required
                >
                  <option value="">Sélectionner un produit</option>
                  {produits.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.nom} - {p.categorie}
                    </option>
                  ))}
                </select>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="quantite">Quantité *</Label>
                  <Input
                    id="quantite"
                    type="number"
                    min="0"
                    value={formData.quantite}
                    onChange={(e) => setFormData({ ...formData, quantite: e.target.value })}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="seuil_alerte">Seuil d'alerte *</Label>
                  <Input
                    id="seuil_alerte"
                    type="number"
                    min="0"
                    value={formData.seuil_alerte}
                    onChange={(e) => setFormData({ ...formData, seuil_alerte: e.target.value })}
                    required
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="numero_lot">Numéro de lot</Label>
                  <Input
                    id="numero_lot"
                    value={formData.numero_lot}
                    onChange={(e) => setFormData({ ...formData, numero_lot: e.target.value })}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="date_expiration">Date d'expiration</Label>
                  <Input
                    id="date_expiration"
                    type="date"
                    value={formData.date_expiration}
                    onChange={(e) => setFormData({ ...formData, date_expiration: e.target.value })}
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="prix_vente">Prix de vente (FCFA)</Label>
                <Input
                  id="prix_vente"
                  type="number"
                  min="0"
                  step="0.01"
                  value={formData.prix_vente}
                  onChange={(e) => setFormData({ ...formData, prix_vente: e.target.value })}
                />
              </div>
              <DialogFooter>
                <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>
                  Annuler
                </Button>
                <Button type="submit">Enregistrer</Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {alertes.length > 0 && (
        <Card className="border-destructive">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-destructive">
              <AlertTriangle className="h-5 w-5" />
              Alertes de stock ({alertes.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {alertes.map((stock) => (
                <div
                  key={stock.id}
                  className="flex items-center justify-between p-3 bg-destructive/10 rounded-lg"
                >
                  <div>
                    <p className="font-medium">{stock.produit?.nom}</p>
                    <p className="text-sm text-muted-foreground">
                      Stock: {stock.quantite} / Seuil: {stock.seuil_alerte}
                    </p>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleEdit(stock)}
                  >
                    Réapprovisionner
                  </Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Search className="h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Rechercher un stock..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="max-w-sm"
            />
          </div>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary"></div>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Produit</TableHead>
                  <TableHead>Catégorie</TableHead>
                  <TableHead>Quantité</TableHead>
                  <TableHead>Seuil</TableHead>
                  <TableHead>Lot</TableHead>
                  <TableHead>Expiration</TableHead>
                  <TableHead>Prix</TableHead>
                  <TableHead>Statut</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {stocks.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={9} className="text-center text-muted-foreground">
                      Aucun stock trouvé
                    </TableCell>
                  </TableRow>
                ) : (
                  stocks.map((stock) => (
                    <TableRow key={stock.id}>
                      <TableCell className="font-medium">
                        {stock.produit?.nom || '-'}
                      </TableCell>
                      <TableCell>{stock.produit?.categorie || '-'}</TableCell>
                      <TableCell>{stock.quantite}</TableCell>
                      <TableCell>{stock.seuil_alerte}</TableCell>
                      <TableCell>{stock.numero_lot || '-'}</TableCell>
                      <TableCell>{stock.date_expiration || '-'}</TableCell>
                      <TableCell>{stock.prix_vente ? `${stock.prix_vente} FCFA` : '-'}</TableCell>
                      <TableCell>
                        {isStockLow(stock) ? (
                          <span className="px-2 py-1 rounded-full text-xs font-medium bg-destructive/20 text-destructive">
                            Alerte
                          </span>
                        ) : stock.quantite === 0 ? (
                          <span className="px-2 py-1 rounded-full text-xs font-medium bg-red-500/20 text-red-500">
                            Rupture
                          </span>
                        ) : (
                          <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-500/20 text-green-500">
                            OK
                          </span>
                        )}
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex justify-end gap-2">
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleEdit(stock)}
                          >
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleDelete(stock.id)}
                          >
                            <Trash2 className="h-4 w-4 text-destructive" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

