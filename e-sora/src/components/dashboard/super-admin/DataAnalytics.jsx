import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card'
import { 
  BarChart3, 
  PieChart, 
  TrendingUp, 
  Calendar,
  Users,
  FileText,
  Activity,
  Clock
} from 'lucide-react'
import { AnimatedContainer, AnimatedStagger } from '../../ui/animated-page'
import { analyticsService } from '../../../services/apiService'

const ChartPlaceholder = ({ title, type, description, data }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          {type === 'bar' ? <BarChart3 className="h-5 w-5" /> : <PieChart className="h-5 w-5" />}
          {title}
        </CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-64 bg-muted/20 rounded-lg flex items-center justify-center">
          {data ? (
            <div className="w-full h-full p-4">
              {type === 'bar' && data.labels && (
                <div className="flex items-end justify-around h-full gap-2">
                  {data.data.map((value, index) => {
                    const maxValue = Math.max(...data.data)
                    const height = (value / maxValue) * 100
                    return (
                      <div key={index} className="flex flex-col items-center flex-1">
                        <div className="text-xs font-semibold mb-1">{value}</div>
                        <div 
                          className="w-full bg-primary rounded-t transition-all"
                          style={{ height: `${height}%`, minHeight: '20px' }}
                        />
                        <div className="text-xs text-muted-foreground mt-2 truncate w-full text-center">
                          {data.labels[index]}
                        </div>
                      </div>
                    )
                  })}
                </div>
              )}
              {type === 'pie' && data.labels && (
                <div className="space-y-2">
                  {data.labels.map((label, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div 
                          className="w-3 h-3 rounded-full"
                          style={{ backgroundColor: data.colors?.[index] || '#6B7280' }}
                        />
                        <span className="text-sm">{label}</span>
                      </div>
                      <span className="font-semibold">{data.data[index]}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <div className="text-center">
              <Activity className="h-12 w-12 text-muted-foreground mx-auto mb-2 animate-pulse" />
              <p className="text-sm text-muted-foreground">Chargement des données...</p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}

const MetricCard = ({ title, value, change, icon: Icon, color = "primary" }) => {
  const colorClasses = {
    primary: "text-primary",
    success: "text-green-600",
    warning: "text-yellow-600",
    danger: "text-red-600"
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <Icon className={`h-4 w-4 ${colorClasses[color]}`} />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {change && (
          <div className={`flex items-center mt-1 text-xs ${
            change.positive ? 'text-green-600' : 'text-red-600'
          }`}>
            <TrendingUp className={`h-3 w-3 mr-1 ${change.positive ? '' : 'rotate-180'}`} />
            {change.value}% vs période précédente
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export const DataAnalytics = ({ stats }) => {
  const [loading, setLoading] = useState(true)
  const [analyticsData, setAnalyticsData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await analyticsService.getDashboard()
      console.log('Analytics data received:', response.data)
      setAnalyticsData(response.data)
    } catch (error) {
      console.error('Erreur lors du chargement des analytics:', error)
      setError('Impossible de charger les analytics. Vérifiez votre connexion.')
      setAnalyticsData(null)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Chargement des analytics...</p>
        </div>
      </div>
    )
  }

  if (error || !analyticsData) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <Activity className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <p className="text-red-600 font-semibold mb-2">{error || 'Erreur de chargement'}</p>
          <button 
            onClick={fetchAnalytics}
            className="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90"
          >
            Réessayer
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Métriques clés */}
      <AnimatedContainer>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            title="Taux de conversion"
            value={`${analyticsData.taux_conversion}%`}
            icon={TrendingUp}
            color="success"
          />
          <MetricCard
            title="Satisfaction patient"
            value={analyticsData.satisfaction_patient > 0 ? `${analyticsData.satisfaction_patient}/5` : 'N/A'}
            icon={Users}
            color="primary"
          />
          <MetricCard
            title="Temps moyen consultation"
            value={analyticsData.temps_moyen_consultation > 0 ? `${analyticsData.temps_moyen_consultation} min` : 'N/A'}
            icon={Clock}
            color="warning"
          />
          <MetricCard
            title="Taux d'annulation"
            value={`${analyticsData.taux_annulation}%`}
            icon={FileText}
            color="danger"
          />
        </div>
      </AnimatedContainer>

      {/* Métriques brutes (pour debug) */}
      {analyticsData.meta && (
        <AnimatedContainer>
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Statistiques globales</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-sm">
                <div>
                  <p className="text-muted-foreground">Total RDV</p>
                  <p className="font-bold text-lg">{analyticsData.meta.total_rdv}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">RDV Confirmés</p>
                  <p className="font-bold text-lg">{analyticsData.meta.rdv_confirmes}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">RDV Terminés</p>
                  <p className="font-bold text-lg">{analyticsData.meta.rdv_termines}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">Consultations</p>
                  <p className="font-bold text-lg">{analyticsData.meta.total_consultations}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">Utilisateurs</p>
                  <p className="font-bold text-lg">{analyticsData.meta.total_utilisateurs}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </AnimatedContainer>
      )}

      {/* Graphiques */}
      <AnimatedStagger className="grid grid-cols-1 lg:grid-cols-2 gap-6" staggerDelay={0.2}>
        <ChartPlaceholder
          title="Consultations par mois"
          type="bar"
          description="Évolution du nombre de consultations sur les 6 derniers mois"
          data={analyticsData.consultations_par_mois}
        />
        
        <ChartPlaceholder
          title="Rendez-vous par statut"
          type="pie"
          description="Répartition des rendez-vous selon leur statut"
          data={analyticsData.rendez_vous_par_statut}
        />
        
        <ChartPlaceholder
          title="Utilisateurs par rôle"
          type="pie"
          description="Distribution des utilisateurs selon leur rôle dans le système"
          data={analyticsData.utilisateurs_par_role}
        />
        
        <ChartPlaceholder
          title="Activité hebdomadaire"
          type="bar"
          description="Nombre d'actions effectuées par jour de la semaine"
          data={analyticsData.activite_hebdomadaire && analyticsData.activite_hebdomadaire.length > 0 ? {
            labels: analyticsData.activite_hebdomadaire.map(d => d.jour),
            data: analyticsData.activite_hebdomadaire.map(d => d.total)
          } : null}
        />
      </AnimatedStagger>

      {/* Tableau de données détaillées */}
      <AnimatedContainer>
        <Card>
          <CardHeader>
            <CardTitle>Données détaillées</CardTitle>
            <CardDescription>
              Analyse approfondie des métriques système
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <h4 className="font-semibold mb-3">Consultations par mois</h4>
                <div className="space-y-2">
                  {analyticsData.consultations_par_mois?.labels?.length > 0 ? (
                    analyticsData.consultations_par_mois.labels.map((label, index) => (
                      <div key={index} className="flex justify-between items-center">
                        <span className="text-sm text-muted-foreground">{label}</span>
                        <span className="font-medium">{analyticsData.consultations_par_mois.data[index]}</span>
                      </div>
                    ))
                  ) : (
                    <p className="text-sm text-muted-foreground">Aucune donnée disponible</p>
                  )}
                </div>
              </div>
              
              <div>
                <h4 className="font-semibold mb-3">Rendez-vous par statut</h4>
                <div className="space-y-2">
                  {analyticsData.rendez_vous_par_statut?.labels?.length > 0 ? (
                    analyticsData.rendez_vous_par_statut.labels.map((label, index) => (
                      <div key={index} className="flex justify-between items-center">
                        <div className="flex items-center gap-2">
                          <div 
                            className="w-3 h-3 rounded-full"
                            style={{ backgroundColor: analyticsData.rendez_vous_par_statut.colors[index] }}
                          />
                          <span className="text-sm text-muted-foreground">{label}</span>
                        </div>
                        <span className="font-medium">{analyticsData.rendez_vous_par_statut.data[index]}</span>
                      </div>
                    ))
                  ) : (
                    <p className="text-sm text-muted-foreground">Aucune donnée disponible</p>
                  )}
                </div>
              </div>
              
              <div>
                <h4 className="font-semibold mb-3">Utilisateurs par rôle</h4>
                <div className="space-y-2">
                  {analyticsData.utilisateurs_par_role?.labels?.length > 0 ? (
                    analyticsData.utilisateurs_par_role.labels.map((label, index) => (
                      <div key={index} className="flex justify-between items-center">
                        <div className="flex items-center gap-2">
                          <div 
                            className="w-3 h-3 rounded-full"
                            style={{ backgroundColor: analyticsData.utilisateurs_par_role.colors[index] }}
                          />
                          <span className="text-sm text-muted-foreground">{label}</span>
                        </div>
                        <span className="font-medium">{analyticsData.utilisateurs_par_role.data[index]}</span>
                      </div>
                    ))
                  ) : (
                    <p className="text-sm text-muted-foreground">Aucune donnée disponible</p>
                  )}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </AnimatedContainer>
    </div>
  )
}