import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { pharmaciesService, stocksService, commandesService, produitsService } from '../../services/apiService'
import { Button } from '../../components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../../components/ui/table'
import { 
  ArrowLeft, 
  Pill, 
  MapPin, 
  Phone, 
  Mail, 
  Package, 
  ShoppingCart, 
  AlertTriangle,
  Activity,
  TrendingUp,
  TrendingDown,
  CheckCircle,
  Clock,
  XCircle
} from 'lucide-react'
import { AnimatedContainer, AnimatedStagger } from '../../components/ui/animated-page'
import { format } from 'date-fns'
import { fr } from 'date-fns/locale'

const StatCard = ({ title, value, description, icon: Icon, color = "primary" }) => {
  const colorClasses = {
    primary: "text-primary border-primary/20 bg-primary/5",
    success: "text-green-600 border-green-200 bg-green-50",
    warning: "text-yellow-600 border-yellow-200 bg-yellow-50",
    danger: "text-red-600 border-red-200 bg-red-50",
    info: "text-blue-600 border-blue-200 bg-blue-50"
  }

  return (
    <Card className={`hover:shadow-lg transition-all ${colorClasses[color]}`}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <Icon className="h-4 w-4" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {description && (
          <p className="text-xs text-muted-foreground mt-1">{description}</p>
        )}
      </CardContent>
    </Card>
  )
}

export const PharmacieDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [pharmacie, setPharmacie] = useState(null)
  const [stocks, setStocks] = useState([])
  const [commandes, setCommandes] = useState([])
  const [produits, setProduits] = useState([])
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({
    totalStocks: 0,
    totalCommandes: 0,
    totalProduits: 0,
    stocksAlertes: 0,
    commandesEnCours: 0,
    commandesLivrees: 0,
    commandesAnnulees: 0
  })

  useEffect(() => {
    fetchPharmacieData()
  }, [id])

  const fetchPharmacieData = async () => {
    try {
      setLoading(true)
      
      // Récupérer les informations de la pharmacie
      const pharmacieResponse = await pharmaciesService.getById(id)
      setPharmacie(pharmacieResponse.data)
      
      // Récupérer les données liées à la pharmacie en parallèle
      const [
        stocksResponse,
        commandesResponse,
        produitsResponse
      ] = await Promise.all([
        stocksService.getAll({ pharmacie: id }).catch(() => ({ data: [] })),
        commandesService.getAll({ pharmacie: id }).catch(() => ({ data: [] })),
        produitsService.getAll({ pharmacie: id }).catch(() => ({ data: [] }))
      ])

      const stocksData = Array.isArray(stocksResponse.data) ? stocksResponse.data : (stocksResponse.data?.results || [])
      const commandesData = Array.isArray(commandesResponse.data) ? commandesResponse.data : (commandesResponse.data?.results || [])
      const produitsData = Array.isArray(produitsResponse.data) ? produitsResponse.data : (produitsResponse.data?.results || [])

      setStocks(stocksData)
      setCommandes(commandesData)
      setProduits(produitsData)

      // Calculer les statistiques
      const stocksAlertes = stocksData.filter(stock => stock.quantite <= stock.seuil_alerte).length
      const commandesEnCours = commandesData.filter(cmd => cmd.statut === 'en_cours').length
      const commandesLivrees = commandesData.filter(cmd => cmd.statut === 'livree').length
      const commandesAnnulees = commandesData.filter(cmd => cmd.statut === 'annulee').length

      setStats({
        totalStocks: stocksData.length,
        totalCommandes: commandesData.length,
        totalProduits: produitsData.length,
        stocksAlertes,
        commandesEnCours,
        commandesLivrees,
        commandesAnnulees
      })

    } catch (error) {
      console.error('Erreur lors du chargement des données de la pharmacie:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString) => {
    try {
      if (!dateString) return 'Date inconnue'
      const date = new Date(dateString)
      if (isNaN(date.getTime())) return 'Date invalide'
      return format(date, 'dd MMM yyyy à HH:mm', { locale: fr })
    } catch (error) {
      return 'Date invalide'
    }
  }

  const getStatutColor = (statut) => {
    switch (statut) {
      case 'livree': return 'text-green-600 bg-green-100'
      case 'en_cours': return 'text-yellow-600 bg-yellow-100'
      case 'annulee': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getStockStatus = (stock) => {
    if (stock.quantite <= 0) return { color: 'danger', text: 'Rupture' }
    if (stock.quantite <= stock.seuil_alerte) return { color: 'warning', text: 'Alerte' }
    return { color: 'success', text: 'Normal' }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    )
  }

  if (!pharmacie) {
    return (
      <div className="text-center py-8">
        <p className="text-muted-foreground">Pharmacie non trouvée</p>
        <Button onClick={() => navigate('/pharmacies')} className="mt-4">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Retour aux pharmacies
        </Button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <AnimatedContainer>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button
              variant="outline"
              onClick={() => navigate('/pharmacies')}
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Retour
            </Button>
            <div>
              <h1 className="text-3xl font-bold flex items-center gap-2">
                <Pill className="h-8 w-8 text-primary" />
                {pharmacie.nom}
              </h1>
              <p className="text-muted-foreground mt-1">
                Détails et inventaire de la pharmacie
              </p>
            </div>
          </div>
          <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
            pharmacie.actif 
              ? 'bg-green-100 text-green-800' 
              : 'bg-red-100 text-red-800'
          }`}>
            {pharmacie.actif ? 'Active' : 'Inactive'}
          </span>
        </div>
      </AnimatedContainer>

      {/* Informations de base */}
      <AnimatedContainer delay={0.1}>
        <Card>
          <CardHeader>
            <CardTitle>Informations de la pharmacie</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {pharmacie.adresse && (
                <div className="flex items-center gap-2">
                  <MapPin className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">{pharmacie.adresse}</span>
                </div>
              )}
              {pharmacie.telephone && (
                <div className="flex items-center gap-2">
                  <Phone className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">{pharmacie.telephone}</span>
                </div>
              )}
              {pharmacie.email && (
                <div className="flex items-center gap-2">
                  <Mail className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">{pharmacie.email}</span>
                </div>
              )}
              <div className="flex items-center gap-2">
                <Activity className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">ID: {pharmacie.id}</span>
              </div>
            </div>
            {pharmacie.description && (
              <div className="mt-4">
                <p className="text-sm text-muted-foreground">{pharmacie.description}</p>
              </div>
            )}
          </CardContent>
        </Card>
      </AnimatedContainer>

      {/* Statistiques */}
      <AnimatedStagger className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4" staggerDelay={0.1}>
        <StatCard
          title="Stocks"
          value={stats.totalStocks}
          description={`${stats.stocksAlertes} en alerte`}
          icon={Package}
          color={stats.stocksAlertes > 0 ? "warning" : "primary"}
        />
        <StatCard
          title="Produits"
          value={stats.totalProduits}
          description="Références disponibles"
          icon={Pill}
          color="info"
        />
        <StatCard
          title="Commandes"
          value={stats.totalCommandes}
          description={`${stats.commandesEnCours} en cours`}
          icon={ShoppingCart}
          color="success"
        />
        <StatCard
          title="Alertes"
          value={stats.stocksAlertes}
          description="Stocks faibles"
          icon={AlertTriangle}
          color={stats.stocksAlertes > 0 ? "danger" : "success"}
        />
      </AnimatedStagger>

      {/* Détails par onglets */}
      <AnimatedContainer delay={0.3}>
        <Tabs defaultValue="stocks" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="stocks">Stocks ({stats.totalStocks})</TabsTrigger>
            <TabsTrigger value="produits">Produits ({stats.totalProduits})</TabsTrigger>
            <TabsTrigger value="commandes">Commandes ({stats.totalCommandes})</TabsTrigger>
          </TabsList>

          <TabsContent value="stocks" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Gestion des stocks</CardTitle>
              </CardHeader>
              <CardContent>
                {stocks.length > 0 ? (
                  <div className="rounded-md border">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Produit</TableHead>
                          <TableHead>Quantité</TableHead>
                          <TableHead>Seuil d'alerte</TableHead>
                          <TableHead>Statut</TableHead>
                          <TableHead>Dernière MAJ</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {stocks.map((stock) => {
                          const status = getStockStatus(stock)
                          return (
                            <TableRow key={stock.id}>
                              <TableCell className="font-medium">
                                {stock.produit_nom || stock.methode_nom || 'Produit'}
                              </TableCell>
                              <TableCell>
                                <span className={`font-semibold ${
                                  stock.quantite <= 0 ? 'text-red-600' : 
                                  stock.quantite <= stock.seuil_alerte ? 'text-yellow-600' : 
                                  'text-green-600'
                                }`}>
                                  {stock.quantite}
                                </span>
                              </TableCell>
                              <TableCell>{stock.seuil_alerte || stock.seuil || 'N/A'}</TableCell>
                              <TableCell>
                                <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                                  status.color === 'success' ? 'bg-green-100 text-green-800' :
                                  status.color === 'warning' ? 'bg-yellow-100 text-yellow-800' :
                                  'bg-red-100 text-red-800'
                                }`}>
                                  {status.color === 'success' && <CheckCircle className="h-3 w-3 mr-1" />}
                                  {status.color === 'warning' && <AlertTriangle className="h-3 w-3 mr-1" />}
                                  {status.color === 'danger' && <XCircle className="h-3 w-3 mr-1" />}
                                  {status.text}
                                </span>
                              </TableCell>
                              <TableCell>{formatDate(stock.updated_at)}</TableCell>
                            </TableRow>
                          )
                        })}
                      </TableBody>
                    </Table>
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <Package className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                    <p className="text-muted-foreground">Aucun stock enregistré</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="produits" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Catalogue des produits</CardTitle>
              </CardHeader>
              <CardContent>
                {produits.length > 0 ? (
                  <div className="rounded-md border">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Nom</TableHead>
                          <TableHead>Catégorie</TableHead>
                          <TableHead>Prix</TableHead>
                          <TableHead>Statut</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {produits.map((produit) => (
                          <TableRow key={produit.id}>
                            <TableCell className="font-medium">
                              {produit.nom}
                            </TableCell>
                            <TableCell>{produit.categorie || 'N/A'}</TableCell>
                            <TableCell>
                              {produit.prix ? `${produit.prix} FCFA` : 'N/A'}
                            </TableCell>
                            <TableCell>
                              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                                produit.actif 
                                  ? 'bg-green-100 text-green-800' 
                                  : 'bg-red-100 text-red-800'
                              }`}>
                                {produit.actif ? 'Disponible' : 'Indisponible'}
                              </span>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <Pill className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                    <p className="text-muted-foreground">Aucun produit enregistré</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="commandes" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <StatCard
                title="Livrées"
                value={stats.commandesLivrees}
                icon={CheckCircle}
                color="success"
              />
              <StatCard
                title="En cours"
                value={stats.commandesEnCours}
                icon={Clock}
                color="warning"
              />
              <StatCard
                title="Annulées"
                value={stats.commandesAnnulees}
                icon={XCircle}
                color="danger"
              />
            </div>
            
            <Card>
              <CardHeader>
                <CardTitle>Historique des commandes</CardTitle>
              </CardHeader>
              <CardContent>
                {commandes.length > 0 ? (
                  <div className="rounded-md border">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>N° Commande</TableHead>
                          <TableHead>Date</TableHead>
                          <TableHead>Montant</TableHead>
                          <TableHead>Statut</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {commandes.map((commande) => (
                          <TableRow key={commande.id}>
                            <TableCell className="font-medium">
                              CMD-{commande.id}
                            </TableCell>
                            <TableCell>{formatDate(commande.date_commande)}</TableCell>
                            <TableCell>
                              {commande.montant_total ? `${commande.montant_total} FCFA` : 'N/A'}
                            </TableCell>
                            <TableCell>
                              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatutColor(commande.statut)}`}>
                                {commande.statut === 'livree' && <CheckCircle className="h-3 w-3 mr-1" />}
                                {commande.statut === 'en_cours' && <Clock className="h-3 w-3 mr-1" />}
                                {commande.statut === 'annulee' && <XCircle className="h-3 w-3 mr-1" />}
                                {commande.statut === 'livree' ? 'Livrée' : 
                                 commande.statut === 'en_cours' ? 'En cours' : 
                                 commande.statut === 'annulee' ? 'Annulée' : commande.statut}
                              </span>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <ShoppingCart className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                    <p className="text-muted-foreground">Aucune commande enregistrée</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </AnimatedContainer>
    </div>
  )
}