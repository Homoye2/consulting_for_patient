import { useState, useEffect } from 'react'
import { stocksService, methodesService, mouvementsService } from '../services/apiService'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../components/ui/table'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '../components/ui/dialog'
import { Label } from '../components/ui/label'
import { Plus, Search, Edit, Trash2, AlertTriangle, Package } from 'lucide-react'
import { format } from 'date-fns'

export const Stocks = () => {
  const [stocks, setStocks] = useState([])
  const [methodes, setMethodes] = useState([])
  const [alertes, setAlertes] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [dialogOpen, setDialogOpen] = useState(false)
  const [mouvementDialogOpen, setMouvementDialogOpen] = useState(false)
  const [editingStock, setEditingStock] = useState(null)
  const [selectedStock, setSelectedStock] = useState(null)
  const [formData, setFormData] = useState({
    methode: '',
    quantite: '',
    seuil: '',
  })
  const [mouvementData, setMouvementData] = useState({
    type_mouvement: 'entree',
    quantite: '',
    motif: '',
  })

  useEffect(() => {
    fetchStocks()
    fetchMethodes()
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
    } finally {
      setLoading(false)
    }
  }

  const fetchMethodes = async () => {
    try {
      const response = await methodesService.getAll()
      setMethodes(response.data.results || response.data)
    } catch (error) {
      console.error('Erreur lors du chargement des méthodes:', error)
    }
  }

  const fetchAlertes = async () => {
    try {
      const response = await stocksService.getAlertes()
      setAlertes(response.data)
    } catch (error) {
      console.error('Erreur lors du chargement des alertes:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const data = {
        ...formData,
        methode: parseInt(formData.methode),
        quantite: parseInt(formData.quantite),
        seuil: parseInt(formData.seuil),
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

  const handleMouvement = async (e) => {
    e.preventDefault()
    try {
      const data = {
        ...mouvementData,
        stock_item: selectedStock.id,
        quantite: parseInt(mouvementData.quantite),
      }
      await mouvementsService.create(data)
      setMouvementDialogOpen(false)
      setMouvementData({
        type_mouvement: 'entree',
        quantite: '',
        motif: '',
      })
      fetchStocks()
      fetchAlertes()
    } catch (error) {
      console.error('Erreur lors de l\'enregistrement du mouvement:', error)
      alert('Erreur lors de l\'enregistrement du mouvement')
    }
  }

  const handleEdit = (stock) => {
    setEditingStock(stock)
    setFormData({
      methode: stock.methode?.id || stock.methode || '',
      quantite: stock.quantite || '',
      seuil: stock.seuil || '',
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
      methode: '',
      quantite: '',
      seuil: '',
    })
  }

  const isStockLow = (stock) => {
    return stock.quantite <= stock.seuil
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold">Stocks</h1>
          <p className="text-muted-foreground mt-2">
            Gestion des stocks de méthodes contraceptives
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
          <DialogContent>
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
                <Label htmlFor="methode">Méthode contraceptive *</Label>
                <select
                  id="methode"
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  value={formData.methode}
                  onChange={(e) => setFormData({ ...formData, methode: e.target.value })}
                  required
                >
                  <option value="">Sélectionner une méthode</option>
                  {methodes.map((m) => (
                    <option key={m.id} value={m.id}>
                      {m.nom}
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
                  <Label htmlFor="seuil">Seuil d'alerte *</Label>
                  <Input
                    id="seuil"
                    type="number"
                    min="0"
                    value={formData.seuil}
                    onChange={(e) => setFormData({ ...formData, seuil: e.target.value })}
                    required
                  />
                </div>
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
                    <p className="font-medium">{stock.methode?.nom}</p>
                    <p className="text-sm text-muted-foreground">
                      Stock: {stock.quantite} / Seuil: {stock.seuil}
                    </p>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => {
                      setSelectedStock(stock)
                      setMouvementDialogOpen(true)
                    }}
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
                  <TableHead>Méthode</TableHead>
                  <TableHead>Quantité</TableHead>
                  <TableHead>Seuil</TableHead>
                  <TableHead>Statut</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {stocks.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center text-muted-foreground">
                      Aucun stock trouvé
                    </TableCell>
                  </TableRow>
                ) : (
                  stocks.map((stock) => (
                    <TableRow key={stock.id}>
                      <TableCell className="font-medium">
                        {stock.methode?.nom || '-'}
                      </TableCell>
                      <TableCell>{stock.quantite}</TableCell>
                      <TableCell>{stock.seuil}</TableCell>
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
                            onClick={() => {
                              setSelectedStock(stock)
                              setMouvementDialogOpen(true)
                            }}
                            title="Mouvement de stock"
                          >
                            <Package className="h-4 w-4" />
                          </Button>
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

      <Dialog open={mouvementDialogOpen} onOpenChange={setMouvementDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Mouvement de stock</DialogTitle>
            <DialogDescription>
              Enregistrer un mouvement pour {selectedStock?.methode?.nom}
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleMouvement} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="type_mouvement">Type de mouvement *</Label>
              <select
                id="type_mouvement"
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                value={mouvementData.type_mouvement}
                onChange={(e) => setMouvementData({ ...mouvementData, type_mouvement: e.target.value })}
                required
              >
                <option value="entree">Entrée</option>
                <option value="sortie">Sortie</option>
                <option value="inventaire">Inventaire</option>
                <option value="perte">Perte</option>
              </select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="quantite">Quantité *</Label>
              <Input
                id="quantite"
                type="number"
                min="1"
                value={mouvementData.quantite}
                onChange={(e) => setMouvementData({ ...mouvementData, quantite: e.target.value })}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="motif">Motif</Label>
              <textarea
                id="motif"
                className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                value={mouvementData.motif}
                onChange={(e) => setMouvementData({ ...mouvementData, motif: e.target.value })}
              />
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setMouvementDialogOpen(false)}>
                Annuler
              </Button>
              <Button type="submit">Enregistrer</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  )
}

