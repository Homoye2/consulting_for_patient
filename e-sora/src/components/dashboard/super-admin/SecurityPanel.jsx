import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card'
import { Button } from '../../ui/button'
import { Badge } from '../../ui/badge'
import { 
  Shield, 
  AlertTriangle, 
  Lock, 
  Eye, 
  Activity,
  UserX,
  Clock,
  Globe,
  Smartphone
} from 'lucide-react'
import { AnimatedContainer, AnimatedStagger } from '../../ui/animated-page'
import { format } from 'date-fns'
import { fr } from 'date-fns/locale'
import { adminService } from '../../../services/apiService'

const SecurityAlert = ({ alert }) => {
  const getAlertIcon = (severity) => {
    switch (severity) {
      case 'high': return AlertTriangle
      case 'medium': return Shield
      case 'low': return Eye
      default: return Activity
    }
  }

  const getAlertColor = (severity) => {
    switch (severity) {
      case 'high': return 'text-red-600 bg-red-100 border-red-200'
      case 'medium': return 'text-yellow-600 bg-yellow-100 border-yellow-200'
      case 'low': return 'text-blue-600 bg-blue-100 border-blue-200'
      default: return 'text-gray-600 bg-gray-100 border-gray-200'
    }
  }

  const Icon = getAlertIcon(alert.severity)

  return (
    <div className={`p-4 rounded-lg border ${getAlertColor(alert.severity)}`}>
      <div className="flex items-start space-x-3">
        <Icon className="h-5 w-5 mt-0.5" />
        <div className="flex-1">
          <h4 className="font-medium">{alert.title}</h4>
          <p className="text-sm mt-1">{alert.description}</p>
          <p className="text-xs mt-2 opacity-75">
            {(() => {
              try {
                if (!alert.timestamp) return 'Date inconnue'
                const date = new Date(alert.timestamp)
                if (isNaN(date.getTime())) return 'Date invalide'
                return format(date, 'dd MMM yyyy à HH:mm', { locale: fr })
              } catch (error) {
                console.warn('Erreur de formatage de date:', alert.timestamp, error)
                return 'Date invalide'
              }
            })()}
          </p>
        </div>
        <Badge variant="outline">
          {alert.severity === 'high' ? 'Critique' : 
           alert.severity === 'medium' ? 'Moyen' : 'Faible'}
        </Badge>
      </div>
    </div>
  )
}

const LoginAttempt = ({ attempt }) => {
  const getStatusIcon = (success) => {
    return success ? Shield : UserX
  }

  const getStatusColor = (success) => {
    return success ? 'text-green-600' : 'text-red-600'
  }

  const Icon = getStatusIcon(attempt.success)

  return (
    <div className="flex items-center space-x-3 p-3 rounded-lg hover:bg-muted/50">
      <Icon className={`h-4 w-4 ${getStatusColor(attempt.success)}`} />
      <div className="flex-1">
        <div className="flex items-center justify-between">
          <span className="font-medium">{attempt.email}</span>
          <Badge variant={attempt.success ? 'default' : 'destructive'}>
            {attempt.success ? 'Succès' : 'Échec'}
          </Badge>
        </div>
        <div className="flex items-center space-x-4 text-sm text-muted-foreground mt-1">
          <span className="flex items-center">
            <Globe className="h-3 w-3 mr-1" />
            {attempt.ip}
          </span>
          <span className="flex items-center">
            <Smartphone className="h-3 w-3 mr-1" />
            {attempt.userAgent}
          </span>
          <span className="flex items-center">
            <Clock className="h-3 w-3 mr-1" />
            {(() => {
              try {
                if (!attempt.timestamp) return 'Heure inconnue'
                const date = new Date(attempt.timestamp)
                if (isNaN(date.getTime())) return 'Heure invalide'
                return format(date, 'HH:mm', { locale: fr })
              } catch (error) {
                console.warn('Erreur de formatage d\'heure:', attempt.timestamp, error)
                return 'Heure invalide'
              }
            })()}
          </span>
        </div>
      </div>
    </div>
  )
}

export const SecurityPanel = () => {
  const [securityAlerts, setSecurityAlerts] = useState([])
  const [loginAttempts, setLoginAttempts] = useState([])
  const [securityStats, setSecurityStats] = useState({
    totalAttempts: 0,
    successfulLogins: 0,
    failedAttempts: 0,
    blockedIPs: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchSecurityData()
  }, [])

  const fetchSecurityData = async () => {
    try {
      setLoading(true)
      
      const [statsResponse, alertsResponse, attemptsResponse] = await Promise.all([
        adminService.getSecurityStats(),
        adminService.getSecurityAlerts(),
        adminService.getLoginAttempts({ limit: 20 })
      ])
      
      setSecurityStats(statsResponse.data)
      setSecurityAlerts(alertsResponse.data)
      setLoginAttempts(attemptsResponse.data)
    } catch (error) {
      console.error('Erreur lors du chargement des données de sécurité:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleBlockIP = (ip) => {
    if (confirm(`Êtes-vous sûr de vouloir bloquer l'IP ${ip} ?`)) {
      alert(`IP ${ip} bloquée avec succès`)
      // TODO: Implémenter l'API de blocage d'IP
    }
  }

  const handleClearAlerts = () => {
    if (confirm('Êtes-vous sûr de vouloir effacer toutes les alertes ?')) {
      setSecurityAlerts([])
      // TODO: Implémenter l'API de suppression des alertes
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Chargement des données de sécurité...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Statistiques de sécurité */}
      <AnimatedContainer>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Tentatives totales</CardTitle>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{securityStats.totalAttempts}</div>
              <p className="text-xs text-muted-foreground">Dernières 24h</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Connexions réussies</CardTitle>
              <Shield className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{securityStats.successfulLogins}</div>
              <p className="text-xs text-muted-foreground">
                {Math.round((securityStats.successfulLogins / securityStats.totalAttempts) * 100)}% du total
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Tentatives échouées</CardTitle>
              <AlertTriangle className="h-4 w-4 text-red-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600">{securityStats.failedAttempts}</div>
              <p className="text-xs text-muted-foreground">
                {Math.round((securityStats.failedAttempts / securityStats.totalAttempts) * 100)}% du total
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">IPs bloquées</CardTitle>
              <Lock className="h-4 w-4 text-purple-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-purple-600">{securityStats.blockedIPs}</div>
              <p className="text-xs text-muted-foreground">Actives</p>
            </CardContent>
          </Card>
        </div>
      </AnimatedContainer>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Alertes de sécurité */}
        <AnimatedContainer>
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Alertes de Sécurité</CardTitle>
                  <CardDescription>Événements de sécurité récents</CardDescription>
                </div>
                <Button variant="outline" size="sm" onClick={handleClearAlerts}>
                  Effacer tout
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {securityAlerts.length > 0 ? (
                  securityAlerts.map((alert) => (
                    <SecurityAlert key={alert.id} alert={alert} />
                  ))
                ) : (
                  <div className="text-center py-8">
                    <Shield className="h-12 w-12 text-green-600 mx-auto mb-4" />
                    <p className="text-muted-foreground">Aucune alerte de sécurité</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </AnimatedContainer>

        {/* Tentatives de connexion récentes */}
        <AnimatedContainer>
          <Card>
            <CardHeader>
              <CardTitle>Tentatives de Connexion</CardTitle>
              <CardDescription>Activité de connexion récente</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {loginAttempts.map((attempt) => (
                  <LoginAttempt key={attempt.id} attempt={attempt} />
                ))}
              </div>
            </CardContent>
          </Card>
        </AnimatedContainer>
      </div>

      {/* Actions de sécurité */}
      <AnimatedContainer>
        <Card>
          <CardHeader>
            <CardTitle>Actions de Sécurité</CardTitle>
            <CardDescription>Outils de gestion de la sécurité</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Button variant="outline" className="h-20 flex-col">
                <Lock className="h-6 w-6 mb-2" />
                Gérer les IPs bloquées
              </Button>
              <Button variant="outline" className="h-20 flex-col">
                <Eye className="h-6 w-6 mb-2" />
                Audit des connexions
              </Button>
              <Button variant="outline" className="h-20 flex-col">
                <Shield className="h-6 w-6 mb-2" />
                Rapport de sécurité
              </Button>
            </div>
          </CardContent>
        </Card>
      </AnimatedContainer>
    </div>
  )
}