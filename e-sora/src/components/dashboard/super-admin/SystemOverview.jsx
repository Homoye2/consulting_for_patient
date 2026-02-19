import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card'
import { Badge } from '../../ui/badge'
import { Button } from '../../ui/button'
import { 
  Database, 
  Server, 
  HardDrive, 
  Cpu, 
  AlertTriangle, 
  CheckCircle, 
  Clock,
  Bell,
  Calendar,
  FileText,
  Users
} from 'lucide-react'
import { AnimatedContainer, AnimatedStagger } from '../../ui/animated-page'
import { format } from 'date-fns'
import { fr } from 'date-fns/locale'

const SystemHealthCard = ({ title, status, responseTime, usage, icon: Icon }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy': return 'text-green-600 bg-green-100'
      case 'warning': return 'text-yellow-600 bg-yellow-100'
      case 'error': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'healthy': return CheckCircle
      case 'warning': return AlertTriangle
      case 'error': return AlertTriangle
      default: return Clock
    }
  }

  const StatusIcon = getStatusIcon(status)

  return (
    <Card className="h-full">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-xs sm:text-sm font-medium truncate pr-2">{title}</CardTitle>
        <Icon className="h-4 w-4 text-muted-foreground flex-shrink-0" />
      </CardHeader>
      <CardContent className="pt-0">
        <div className="flex items-center space-x-2 mb-2">
          <StatusIcon className={`h-3 w-3 sm:h-4 sm:w-4 flex-shrink-0 ${getStatusColor(status).split(' ')[0]}`} />
          <Badge variant="secondary" className={`${getStatusColor(status)} text-xs px-2 py-1`}>
            {status === 'healthy' ? 'Sain' : status === 'warning' ? 'Attention' : 'Erreur'}
          </Badge>
        </div>
        {responseTime && (
          <p className="text-xs text-muted-foreground">
            Temps: {responseTime}
          </p>
        )}
        {usage && (
          <p className="text-xs text-muted-foreground">
            Usage: {usage}
          </p>
        )}
      </CardContent>
    </Card>
  )
}

const ActivityItem = ({ activity }) => {
  const getActivityIcon = (type) => {
    switch (type) {
      case 'message': return Bell
      case 'appointment': return Calendar
      case 'consultation': return FileText
      case 'user': return Users
      default: return Clock
    }
  }

  const formatTimestamp = (timestamp) => {
    try {
      if (!timestamp) return 'Date inconnue'
      const date = new Date(timestamp)
      if (isNaN(date.getTime())) return 'Date invalide'
      return format(date, 'dd MMM yyyy à HH:mm', { locale: fr })
    } catch (error) {
      console.warn('Erreur de formatage de date:', timestamp, error)
      return 'Date invalide'
    }
  }

  const Icon = getActivityIcon(activity.type)

  return (
    <div className="flex items-start space-x-3 p-2 sm:p-3 rounded-lg hover:bg-muted/50 transition-colors">
      <div className="bg-primary/10 p-1.5 sm:p-2 rounded-full flex-shrink-0">
        <Icon className="h-3 w-3 sm:h-4 sm:w-4 text-primary" />
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-xs sm:text-sm font-medium line-clamp-2">{activity.description}</p>
        <p className="text-xs text-muted-foreground mt-1">
          {formatTimestamp(activity.timestamp)}
        </p>
      </div>
    </div>
  )
}

const AlertItem = ({ alert }) => {
  const getAlertColor = (type) => {
    switch (type) {
      case 'danger': return 'border-red-200 bg-red-50'
      case 'warning': return 'border-yellow-200 bg-yellow-50'
      case 'info': return 'border-blue-200 bg-blue-50'
      default: return 'border-gray-200 bg-gray-50'
    }
  }

  return (
    <div className={`p-3 sm:p-4 rounded-lg border ${getAlertColor(alert.type)}`}>
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 sm:gap-4">
        <div className="flex items-start sm:items-center space-x-2 flex-1 min-w-0">
          <AlertTriangle className={`h-4 w-4 flex-shrink-0 mt-0.5 sm:mt-0 ${
            alert.type === 'danger' ? 'text-red-600' : 
            alert.type === 'warning' ? 'text-yellow-600' : 'text-blue-600'
          }`} />
          <p className="text-xs sm:text-sm font-medium line-clamp-2">{alert.message}</p>
        </div>
        <Button size="sm" variant="outline" className="w-full sm:w-auto text-xs">
          {alert.action}
        </Button>
      </div>
    </div>
  )
}

export const SystemOverview = ({ systemHealth, recentActivity, alerts }) => {
  return (
    <div className="space-y-4 sm:space-y-6">
      {/* Santé du système */}
      <AnimatedContainer>
        <Card>
          <CardHeader className="pb-3 sm:pb-6">
            <CardTitle className="text-lg sm:text-xl">Santé du Système</CardTitle>
            <CardDescription className="text-sm">État en temps réel des composants système</CardDescription>
          </CardHeader>
          <CardContent>
            <AnimatedStagger className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4" staggerDelay={0.1}>
              <SystemHealthCard
                title="Base de données"
                status={systemHealth?.database?.status}
                responseTime={systemHealth?.database?.responseTime}
                icon={Database}
              />
              <SystemHealthCard
                title="API"
                status={systemHealth?.api?.status}
                responseTime={systemHealth?.api?.responseTime}
                icon={Server}
              />
              <SystemHealthCard
                title="Stockage"
                status={systemHealth?.storage?.status}
                usage={systemHealth?.storage?.usage}
                icon={HardDrive}
              />
              <SystemHealthCard
                title="Mémoire"
                status={systemHealth?.memory?.status}
                usage={systemHealth?.memory?.usage}
                icon={Cpu}
              />
            </AnimatedStagger>
          </CardContent>
        </Card>
      </AnimatedContainer>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-4 sm:gap-6">
        {/* Activité récente */}
        <AnimatedContainer>
          <Card className="h-full">
            <CardHeader className="pb-3 sm:pb-6">
              <CardTitle className="text-lg sm:text-xl">Activité Récente</CardTitle>
              <CardDescription className="text-sm">Dernières actions dans le système</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-1 sm:space-y-2 max-h-80 overflow-y-auto">
                {recentActivity.length > 0 ? (
                  recentActivity.map((activity) => (
                    <ActivityItem key={activity.id} activity={activity} />
                  ))
                ) : (
                  <p className="text-xs sm:text-sm text-muted-foreground text-center py-6 sm:py-8">
                    Aucune activité récente
                  </p>
                )}
              </div>
            </CardContent>
          </Card>
        </AnimatedContainer>

        {/* Alertes système */}
        <AnimatedContainer>
          <Card className="h-full">
            <CardHeader className="pb-3 sm:pb-6">
              <CardTitle className="text-lg sm:text-xl">Alertes Système</CardTitle>
              <CardDescription className="text-sm">Notifications importantes nécessitant attention</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 sm:space-y-3 max-h-80 overflow-y-auto">
                {alerts.length > 0 ? (
                  alerts.map((alert) => (
                    <AlertItem key={alert.id} alert={alert} />
                  ))
                ) : (
                  <div className="text-center py-6 sm:py-8">
                    <CheckCircle className="h-6 w-6 sm:h-8 sm:w-8 text-green-600 mx-auto mb-2" />
                    <p className="text-xs sm:text-sm text-muted-foreground">
                      Aucune alerte système
                    </p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </AnimatedContainer>
      </div>
    </div>
  )
}