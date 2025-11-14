import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card'
import { Calendar, FileText, Clock, CheckCircle2, XCircle } from 'lucide-react'
import { Link } from 'react-router-dom'
import { rendezVousService, consultationsService } from '../../services/apiService'
import { format } from 'date-fns'

export const PatientDashboard = () => {
  const [stats, setStats] = useState({
    totalRendezVous: 0,
    rendezVousAvenir: 0,
    totalConsultations: 0,
  })
  const [loading, setLoading] = useState(true)
  const [recentRendezVous, setRecentRendezVous] = useState([])
  const [recentConsultations, setRecentConsultations] = useState([])

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      // Récupérer les rendez-vous et consultations du patient
      // Le backend filtre automatiquement les données du patient connecté
      const [rdvRes, consultationsRes] = await Promise.all([
        rendezVousService.getAll(),
        consultationsService.getAll(),
      ])

      const rendezVous = Array.isArray(rdvRes.data) ? rdvRes.data : (rdvRes.data?.results || [])
      const consultations = Array.isArray(consultationsRes.data) ? consultationsRes.data : (consultationsRes.data?.results || [])

      const maintenant = new Date()
      const rendezVousAvenir = rendezVous.filter(rdv => {
        const dateRdv = new Date(rdv.datetime)
        return dateRdv >= maintenant && rdv.statut !== 'annule'
      })

      setStats({
        totalRendezVous: rendezVous.length,
        rendezVousAvenir: rendezVousAvenir.length,
        totalConsultations: consultations.length,
      })

      setRecentRendezVous(rendezVous.slice(0, 3))
      setRecentConsultations(consultations.slice(0, 3))
    } catch (error) {
      console.error('Erreur lors du chargement des données:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatutBadge = (statut) => {
    const badges = {
      confirme: { icon: CheckCircle2, className: 'bg-green-500/10 text-green-600', label: 'Confirmé' },
      en_attente: { icon: Clock, className: 'bg-yellow-500/10 text-yellow-600', label: 'En attente' },
      annule: { icon: XCircle, className: 'bg-red-500/10 text-red-600', label: 'Annulé' },
    }
    return badges[statut] || badges.en_attente
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl md:text-4xl font-bold mb-2">Bienvenue sur votre espace patient</h1>
        <p className="text-muted-foreground">
          Gérez vos rendez-vous et consultez vos consultations
        </p>
      </div>

      {/* Statistiques */}
      <div className="grid gap-4 md:grid-cols-3 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Rendez-vous</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalRendezVous}</div>
            <p className="text-xs text-muted-foreground">
              {stats.rendezVousAvenir} à venir
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Consultations</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalConsultations}</div>
            <p className="text-xs text-muted-foreground">
              Consultations effectuées
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Rendez-vous à venir</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.rendezVousAvenir}</div>
            <p className="text-xs text-muted-foreground">
              Prochains rendez-vous
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Rendez-vous récents */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Rendez-vous récents</CardTitle>
                <CardDescription>Vos derniers rendez-vous</CardDescription>
              </div>
              <Link to="/patient/rendez-vous">
                <button className="text-sm text-primary hover:underline">Voir tout</button>
              </Link>
            </div>
          </CardHeader>
          <CardContent>
            {recentRendezVous.length > 0 ? (
              <div className="space-y-4">
                {recentRendezVous.map((rdv) => {
                  const badge = getStatutBadge(rdv.statut)
                  const BadgeIcon = badge.icon
                  return (
                    <div key={rdv.id} className="flex items-center justify-between p-3 border rounded-lg">
                      <div>
                        <p className="font-medium">
                          {format(new Date(rdv.datetime), "dd MMMM yyyy 'à' HH:mm")}
                        </p>
                        <p className="text-sm text-muted-foreground">{rdv.professionnel_nom}</p>
                      </div>
                      <div className={`flex items-center gap-1 px-2 py-1 rounded-full text-xs ${badge.className}`}>
                        <BadgeIcon className="h-3 w-3" />
                        <span>{badge.label}</span>
                      </div>
                    </div>
                  )
                })}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground text-center py-4">
                Aucun rendez-vous pour le moment
              </p>
            )}
          </CardContent>
        </Card>

        {/* Consultations récentes */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Consultations récentes</CardTitle>
                <CardDescription>Vos dernières consultations</CardDescription>
              </div>
              <Link to="/patient/consultations">
                <button className="text-sm text-primary hover:underline">Voir tout</button>
              </Link>
            </div>
          </CardHeader>
          <CardContent>
            {recentConsultations.length > 0 ? (
              <div className="space-y-4">
                {recentConsultations.map((consultation) => (
                  <div key={consultation.id} className="p-3 border rounded-lg">
                    <p className="font-medium">
                      {format(new Date(consultation.date), "dd MMMM yyyy")}
                    </p>
                    <p className="text-sm text-muted-foreground">
                      {consultation.professionnel_nom}
                    </p>
                    {consultation.methode_prescite_nom && (
                      <p className="text-sm text-primary mt-1">
                        Méthode: {consultation.methode_prescite_nom}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground text-center py-4">
                Aucune consultation pour le moment
              </p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

