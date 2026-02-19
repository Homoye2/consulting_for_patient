import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { statistiquesService } from '../../../services/apiService'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../../components/ui/card'
import { Users, Calendar, FileText, AlertTriangle, TrendingUp } from 'lucide-react'
import { cn } from '../../../lib/utils'
import { useAuth } from '../../../contexts/AuthContext'
import { AnimatedContainer, AnimatedStagger } from '../../../components/ui/animated-page'

const StatCard = ({ title, value, description, icon: Icon, href }) => {
  const content = (
    <Card className={cn(
      "hover:shadow-lg transition-shadow",
      href && "cursor-pointer"
    )}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <Icon className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {description && (
          <p className="text-xs text-muted-foreground mt-1">{description}</p>
        )}
      </CardContent>
    </Card>
  )

  if (href) {
    return <Link to={href}>{content}</Link>
  }
  return content
}

export const UserDashboard = () => {
  const { user } = useAuth()
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await statistiquesService.getGeneral()
        setStats(response.data)
      } catch (error) {
        console.error('Erreur lors du chargement des statistiques:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
  }, [])

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
        <div>
          <h1 className="text-3xl font-bold">Tableau de bord</h1>
          <p className="text-muted-foreground mt-2">
            Vue d'ensemble de votre activité
          </p>
        </div>
      </AnimatedContainer>

      <AnimatedStagger className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <StatCard
          title="Total Patients"
          value={stats?.total_patients || 0}
          description="Patients enregistrés"
          icon={Users}
          href="/patients"
        />
        <StatCard
          title="Consultations"
          value={stats?.total_consultations || 0}
          description={`${stats?.consultations_30j || 0} ce mois`}
          icon={FileText}
          href="/consultations"
        />
        <StatCard
          title="Rendez-vous"
          value={stats?.total_rendez_vous || 0}
          description={`${stats?.rendez_vous_a_venir || 0} à venir`}
          icon={Calendar}
          href="/rendez-vous"
        />
      </AnimatedStagger>

      <AnimatedStagger className="grid gap-4 md:grid-cols-2" staggerDelay={0.15}>
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              Activité récente
            </CardTitle>
            <CardDescription>
              Consultations des 30 derniers jours
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{stats?.consultations_30j || 0}</div>
            <p className="text-sm text-muted-foreground mt-2">
              Consultations effectuées ce mois
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-destructive" />
              Alertes
            </CardTitle>
            <CardDescription>
              Éléments nécessitant votre attention
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {stats?.rendez_vous_a_venir > 0 && (
                <div className="flex items-center justify-between p-2 bg-primary/10 rounded">
                  <span className="text-sm">Rendez-vous à venir</span>
                  <span className="font-semibold text-primary">
                    {stats.rendez_vous_a_venir}
                  </span>
                </div>
              )}
              {!stats?.rendez_vous_a_venir && (
                <p className="text-sm text-muted-foreground">
                  Aucune alerte pour le moment
                </p>
              )}
            </div>
          </CardContent>
        </Card>
      </AnimatedStagger>
    </div>
  )
}