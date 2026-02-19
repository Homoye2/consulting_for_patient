import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card'
import { Button } from '../../ui/button'
import { Badge } from '../../ui/badge'
import { Input } from '../../ui/input'
import { Textarea } from '../../ui/textarea'
import { 
  Bell, 
  Send, 
  Users, 
  Calendar, 
  AlertTriangle,
  CheckCircle,
  Clock,
  Mail,
  MessageSquare,
  Smartphone
} from 'lucide-react'
import { AnimatedContainer, AnimatedStagger } from '../../ui/animated-page'
import { format } from 'date-fns'
import { fr } from 'date-fns/locale'
import { adminService } from '../../../services/apiService'

const NotificationItem = ({ notification, onMarkAsRead }) => {
  const getNotificationIcon = (type) => {
    switch (type) {
      case 'appointment': return Calendar
      case 'alert': return AlertTriangle
      case 'message': return MessageSquare
      case 'system': return Bell
      default: return Bell
    }
  }

  const getNotificationColor = (type, isRead) => {
    if (isRead) return 'text-muted-foreground bg-muted/20'
    
    switch (type) {
      case 'alert': return 'text-red-600 bg-red-50'
      case 'appointment': return 'text-blue-600 bg-blue-50'
      case 'message': return 'text-green-600 bg-green-50'
      default: return 'text-primary bg-primary/5'
    }
  }

  const Icon = getNotificationIcon(notification.type)

  return (
    <div className={`p-4 rounded-lg border ${getNotificationColor(notification.type, notification.isRead)}`}>
      <div className="flex items-start space-x-3">
        <Icon className="h-5 w-5 mt-0.5" />
        <div className="flex-1">
          <div className="flex items-center justify-between">
            <h4 className="font-medium">{notification.title}</h4>
            {!notification.isRead && (
              <Badge variant="default" className="text-xs">
                Nouveau
              </Badge>
            )}
          </div>
          <p className="text-sm mt-1">{notification.message}</p>
          <div className="flex items-center justify-between mt-2">
            <p className="text-xs text-muted-foreground">
              {(() => {
                try {
                  if (!notification.timestamp) return 'Date inconnue'
                  const date = new Date(notification.timestamp)
                  if (isNaN(date.getTime())) return 'Date invalide'
                  return format(date, 'dd MMM yyyy à HH:mm', { locale: fr })
                } catch (error) {
                  console.warn('Erreur de formatage de date:', notification.timestamp, error)
                  return 'Date invalide'
                }
              })()}
            </p>
            {!notification.isRead && (
              <Button 
                size="sm" 
                variant="ghost" 
                onClick={() => onMarkAsRead(notification.id)}
              >
                <CheckCircle className="h-3 w-3 mr-1" />
                Marquer comme lu
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export const NotificationCenter = ({ alerts, recentActivity }) => {
  const [notifications, setNotifications] = useState([
    {
      id: 1,
      type: 'alert',
      title: 'Stock faible détecté',
      message: 'Le stock de contraceptifs oraux est en dessous du seuil critique',
      timestamp: new Date(Date.now() - 30 * 60 * 1000),
      isRead: false
    },
    {
      id: 2,
      type: 'appointment',
      title: 'Rendez-vous en attente',
      message: '5 rendez-vous nécessitent une confirmation',
      timestamp: new Date(Date.now() - 60 * 60 * 1000),
      isRead: false
    },
    {
      id: 3,
      type: 'message',
      title: 'Nouveau message de contact',
      message: 'Aïssatou Diallo a envoyé un message via le formulaire de contact',
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000),
      isRead: true
    },
    {
      id: 4,
      type: 'system',
      title: 'Sauvegarde automatique terminée',
      message: 'La sauvegarde quotidienne de la base de données s\'est terminée avec succès',
      timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000),
      isRead: true
    }
  ])

  const [newNotification, setNewNotification] = useState({
    title: '',
    message: '',
    recipients: 'all',
    type: 'email'
  })

  const [sending, setSending] = useState(false)

  const handleMarkAsRead = (notificationId) => {
    setNotifications(prev => 
      prev.map(notif => 
        notif.id === notificationId 
          ? { ...notif, isRead: true }
          : notif
      )
    )
  }

  const handleMarkAllAsRead = () => {
    setNotifications(prev => 
      prev.map(notif => ({ ...notif, isRead: true }))
    )
  }

  const handleSendNotification = async () => {
    if (!newNotification.title || !newNotification.message) {
      alert('Veuillez remplir tous les champs')
      return
    }

    setSending(true)
    try {
      const response = await adminService.broadcastNotification({
        title: newNotification.title,
        message: newNotification.message,
        recipients: newNotification.recipients,
        type: newNotification.type
      })
      
      // Ajouter la notification à la liste
      const notification = {
        id: Date.now(),
        type: 'system',
        title: `Notification envoyée: ${newNotification.title}`,
        message: `${response.data.message}`,
        timestamp: new Date(),
        isRead: false
      }
      
      setNotifications(prev => [notification, ...prev])
      
      // Réinitialiser le formulaire
      setNewNotification({
        title: '',
        message: '',
        recipients: 'all',
        type: 'email'
      })
      
      alert(`Notification envoyée avec succès à ${response.data.recipients_count} utilisateur(s) !`)
    } catch (error) {
      console.error('Erreur lors de l\'envoi:', error)
      alert('Erreur lors de l\'envoi de la notification')
    } finally {
      setSending(false)
    }
  }

  const unreadCount = notifications.filter(n => !n.isRead).length

  return (
    <div className="space-y-6">
      {/* Statistiques des notifications */}
      <AnimatedContainer>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Notifications</CardTitle>
              <Bell className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{notifications.length}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Non lues</CardTitle>
              <AlertTriangle className="h-4 w-4 text-red-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600">{unreadCount}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Alertes actives</CardTitle>
              <Clock className="h-4 w-4 text-yellow-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-yellow-600">{alerts?.length || 0}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Activité récente</CardTitle>
              <Users className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">{recentActivity?.length || 0}</div>
            </CardContent>
          </Card>
        </div>
      </AnimatedContainer>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Centre de notifications */}
        <AnimatedContainer>
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Centre de Notifications</CardTitle>
                  <CardDescription>
                    Toutes les notifications système ({unreadCount} non lues)
                  </CardDescription>
                </div>
                <Button variant="outline" size="sm" onClick={handleMarkAllAsRead}>
                  Tout marquer comme lu
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {notifications.map((notification) => (
                  <NotificationItem
                    key={notification.id}
                    notification={notification}
                    onMarkAsRead={handleMarkAsRead}
                  />
                ))}
              </div>
            </CardContent>
          </Card>
        </AnimatedContainer>

        {/* Envoyer une notification */}
        <AnimatedContainer>
          <Card>
            <CardHeader>
              <CardTitle>Envoyer une Notification</CardTitle>
              <CardDescription>
                Diffuser une notification à tous les utilisateurs
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium">Titre</label>
                <Input
                  value={newNotification.title}
                  onChange={(e) => setNewNotification(prev => ({ ...prev, title: e.target.value }))}
                  placeholder="Titre de la notification"
                />
              </div>

              <div>
                <label className="text-sm font-medium">Message</label>
                <Textarea
                  value={newNotification.message}
                  onChange={(e) => setNewNotification(prev => ({ ...prev, message: e.target.value }))}
                  placeholder="Contenu de la notification"
                  rows={4}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">Destinataires</label>
                  <select
                    value={newNotification.recipients}
                    onChange={(e) => setNewNotification(prev => ({ ...prev, recipients: e.target.value }))}
                    className="w-full px-3 py-2 border border-border rounded-md bg-background"
                  >
                    <option value="all">Tous les utilisateurs</option>
                    <option value="super_admin">Super Administrateurs</option>
                    <option value="admin_hopital">Administrateurs Hôpital</option>
                    <option value="specialiste">Spécialistes</option>
                    <option value="pharmacien">Pharmaciens</option>
                    <option value="employe_pharmacie">Employés Pharmacie</option>
                    <option value="agent_enregistrement">Agents d'enregistrement</option>
                    <option value="patient">Patients</option>
                  </select>
                </div>

                <div>
                  <label className="text-sm font-medium">Type</label>
                  <select
                    value={newNotification.type}
                    onChange={(e) => setNewNotification(prev => ({ ...prev, type: e.target.value }))}
                    className="w-full px-3 py-2 border border-border rounded-md bg-background"
                  >
                    <option value="email">Email</option>
                    <option value="sms">SMS</option>
                    <option value="push">Push</option>
                    <option value="all">Tous les canaux</option>
                  </select>
                </div>
              </div>

              <Button 
                onClick={handleSendNotification} 
                disabled={sending}
                className="w-full"
              >
                {sending ? (
                  <>
                    <Clock className="mr-2 h-4 w-4 animate-spin" />
                    Envoi en cours...
                  </>
                ) : (
                  <>
                    <Send className="mr-2 h-4 w-4" />
                    Envoyer la notification
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </AnimatedContainer>
      </div>
    </div>
  )
}