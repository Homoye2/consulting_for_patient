import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../../../components/ui/card'
import { Button } from '../../../components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../../components/ui/tabs'
import { 
  Users, 
  Calendar, 
  FileText, 
  UserCog,
  Activity,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Clock,
  Bell,
  ChevronDown
} from 'lucide-react'
import { 
  statistiquesService, 
  usersService, 
  patientsService,
  rendezVousService,
  consultationsService,
  contactMessagesService,
  adminService
} from '../../../services/apiService'
import { AnimatedContainer, AnimatedStagger } from '../../../components/ui/animated-page'
import { 
  SystemOverview,
  UserManagement,
  DataAnalytics,
  SystemSettings,
  SecurityPanel,
  NotificationCenter
} from '../../../components/dashboard/super-admin'
import { LandingPageManager } from '../../../components/dashboard/super-admin/LandingPageManager'

const StatCard = ({ title, value, description, icon: Icon, trend, color = "primary" }) => {
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
        <CardTitle className="text-xs sm:text-sm font-medium truncate pr-2">{title}</CardTitle>
        <Icon className="h-4 w-4 flex-shrink-0" />
      </CardHeader>
      <CardContent className="pt-0">
        <div className="text-xl sm:text-2xl font-bold">{value}</div>
        {description && (
          <p className="text-xs text-muted-foreground mt-1 line-clamp-2">{description}</p>
        )}
        {trend && (
          <div className={`flex items-center mt-2 text-xs ${trend.positive ? 'text-green-600' : 'text-red-600'}`}>
            <TrendingUp className={`h-3 w-3 mr-1 flex-shrink-0 ${trend.positive ? '' : 'rotate-180'}`} />
            <span className="truncate">{trend.value}% vs mois dernier</span>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export const SuperAdminDashboard = () => {
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState(null)
  const [systemHealth, setSystemHealth] = useState(null)
  const [recentActivity, setRecentActivity] = useState([])
  const [alerts, setAlerts] = useState([])
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      
      // Récupérer les statistiques de base en gérant les erreurs individuellement
      const promises = [
        statistiquesService.getGeneral().catch(err => ({ data: null, error: err })),
        usersService.getAll({ limit: 1 }).catch(err => ({ data: { count: 0 }, error: err })),
        patientsService.getAll({ limit: 1 }).catch(err => ({ data: { count: 0 }, error: err })),
        rendezVousService.getAll({ limit: 10 }).catch(err => ({ data: { results: [], count: 0 }, error: err })),
        consultationsService.getAll({ limit: 1 }).catch(err => ({ data: { count: 0 }, error: err })),
        contactMessagesService.getAll({ limit: 5 }).catch(err => ({ data: { results: [] }, error: err })),
        adminService.getSystemHealth().catch(err => ({ data: null, error: err })),
        adminService.getRecentActivity({ limit: 10 }).catch(err => ({ data: [], error: err })),
        adminService.getSystemAlerts().catch(err => ({ data: [], error: err }))
      ]

      const [
        generalStats,
        usersData,
        patientsData,
        rendezVousData,
        consultationsData,
        messagesData,
        systemHealthData,
        recentActivityData,
        systemAlertsData
      ] = await Promise.all(promises)

      // Calculer les statistiques avancées avec gestion d'erreur
      const totalUsers = usersData.data?.count || usersData.data?.length || 0
      const totalPatients = patientsData.data?.count || patientsData.data?.length || 0
      const totalConsultations = consultationsData.data?.count || consultationsData.data?.length || 0
      
      const rendezVousArray = Array.isArray(rendezVousData.data) ? rendezVousData.data : (rendezVousData.data?.results || [])
      const totalRendezVous = rendezVousData.data?.count || rendezVousArray.length || 0
      
      // Analyser les rendez-vous récents
      const today = new Date()
      const thisWeek = rendezVousArray.filter(rdv => {
        try {
          const rdvDate = new Date(rdv.datetime)
          const diffTime = Math.abs(today - rdvDate)
          const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
          return diffDays <= 7
        } catch {
          return false
        }
      })

      const confirmedRdv = rendezVousArray.filter(rdv => rdv.statut === 'confirme').length
      const pendingRdv = rendezVousArray.filter(rdv => rdv.statut === 'en_attente').length
      const cancelledRdv = rendezVousArray.filter(rdv => rdv.statut === 'annule').length

      setStats({
        totalUsers,
        totalPatients,
        totalRendezVous,
        totalConsultations,
        thisWeekRdv: thisWeek.length,
        confirmedRdv,
        pendingRdv,
        cancelledRdv,
        generalStats: generalStats.data
      })

      // Utiliser les vraies données de santé du système
      setSystemHealth(systemHealthData.data || {
        database: { status: 'unknown', responseTime: 'N/A' },
        api: { status: 'unknown', responseTime: 'N/A' },
        storage: { status: 'unknown', usage: 'N/A' },
        memory: { status: 'unknown', usage: 'N/A' }
      })

      // Utiliser l'activité récente réelle
      setRecentActivity(recentActivityData.data || [])

      // Utiliser les alertes système réelles
      setAlerts(systemAlertsData.data || [])

    } catch (error) {
      console.error('Erreur lors du chargement des données:', error)
      // Initialiser avec des valeurs par défaut en cas d'erreur globale
      setStats({
        totalUsers: 0,
        totalPatients: 0,
        totalRendezVous: 0,
        totalConsultations: 0,
        thisWeekRdv: 0,
        confirmedRdv: 0,
        pendingRdv: 0,
        cancelledRdv: 0,
        generalStats: null
      })
      setSystemHealth({
        database: { status: 'unknown', responseTime: 'N/A' },
        api: { status: 'error', responseTime: 'N/A' },
        storage: { status: 'unknown', usage: 'N/A' },
        memory: { status: 'unknown', usage: 'N/A' }
      })
      setRecentActivity([])
      setAlerts([{
        id: 'api-error',
        type: 'danger',
        message: 'Erreur de connexion aux services',
        action: 'Vérifier la configuration'
      }])
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Chargement du dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4 sm:space-y-6 p-4 sm:p-6">
      <AnimatedContainer>
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold">Dashboard Super Admin</h1>
            <p className="text-muted-foreground text-sm sm:text-base">
              Vue d'ensemble complète du système de planification familiale
            </p>
          </div>
          <Button onClick={fetchDashboardData} variant="outline" className="w-full sm:w-auto">
            <Activity className="h-4 w-4 mr-2" />
            Actualiser
          </Button>
        </div>
      </AnimatedContainer>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        {/* Desktop tabs - hidden on mobile */}
        <TabsList className="hidden md:grid w-full grid-cols-7">
          <TabsTrigger value="overview">Vue d'ensemble</TabsTrigger>
          <TabsTrigger value="users">Utilisateurs</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
          <TabsTrigger value="settings">Paramètres</TabsTrigger>
          <TabsTrigger value="security">Sécurité</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
          <TabsTrigger value="leading_page">Leading Page</TabsTrigger>
        </TabsList>

        {/* Mobile dropdown - visible only on mobile */}
        <div className="md:hidden mb-6">
          <div className="relative">
            <select
              value={activeTab}
              onChange={(e) => setActiveTab(e.target.value)}
              className="w-full appearance-none bg-background border border-input rounded-md px-3 py-2 pr-8 text-sm focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
            >
              <option value="overview">Vue d'ensemble</option>
              <option value="users">Utilisateurs</option>
              <option value="analytics">Analytics</option>
              <option value="settings">Paramètres</option>
              <option value="security">Sécurité</option>
              <option value="notifications">Notifications</option>
              <option value="leading_page">Leading Page</option>
            </select>
            <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
          </div>
        </div>

        <TabsContent value="overview" className="space-y-4 sm:space-y-6">
          {/* Statistiques principales */}
          <AnimatedStagger className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-6" staggerDelay={0.1}>
            <StatCard
              title="Total Utilisateurs"
              value={stats?.totalUsers || 0}
              description="Tous les utilisateurs actifs"
              icon={Users}
              trend={{ positive: true, value: 12 }}
              color="primary"
            />
            <StatCard
              title="Patients Enregistrés"
              value={stats?.totalPatients || 0}
              description="Patientes dans le système"
              icon={UserCog}
              trend={{ positive: true, value: 8 }}
              color="success"
            />
            <StatCard
              title="Rendez-vous"
              value={stats?.totalRendezVous || 0}
              description="Total des rendez-vous"
              icon={Calendar}
              trend={{ positive: false, value: 3 }}
              color="info"
            />
            <StatCard
              title="Consultations"
              value={stats?.totalConsultations || 0}
              description="Consultations effectuées"
              icon={FileText}
              trend={{ positive: true, value: 15 }}
              color="warning"
            />
          </AnimatedStagger>

          {/* Statistiques détaillées */}
          <AnimatedStagger className="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-6" staggerDelay={0.1}>
            <StatCard
              title="RDV Confirmés"
              value={stats?.confirmedRdv || 0}
              description="Cette semaine"
              icon={CheckCircle}
              color="success"
            />
            <StatCard
              title="RDV En Attente"
              value={stats?.pendingRdv || 0}
              description="Nécessitent confirmation"
              icon={Clock}
              color="warning"
            />
            <StatCard
              title="RDV Annulés"
              value={stats?.cancelledRdv || 0}
              description="Ce mois-ci"
              icon={AlertTriangle}
              color="danger"
            />
          </AnimatedStagger>

          <div className="mt-4 sm:mt-6">
            <SystemOverview 
              systemHealth={systemHealth}
              recentActivity={recentActivity}
              alerts={alerts}
            />
          </div>
        </TabsContent>

        <TabsContent value="users">
          <UserManagement />
        </TabsContent>

        <TabsContent value="analytics">
          <DataAnalytics stats={stats} />
        </TabsContent>

        <TabsContent value="settings">
          <SystemSettings />
        </TabsContent>

        <TabsContent value="security">
          <SecurityPanel />
        </TabsContent>

        <TabsContent value="notifications">
          <NotificationCenter alerts={alerts} recentActivity={recentActivity} />
        </TabsContent>

        <TabsContent value="leading_page">
          <LandingPageManager />
        </TabsContent>
      </Tabs>
    </div>
  )
}