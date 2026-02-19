import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { 
  rendezVousService, 
  patientsService,
  consultationsService,
  hopitauxService
} from '../../services/apiService'
import { extractIdFromSlug, generatePatientSlug, generateUrlWithSlug } from '../../lib/slugUtils'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card'
import { Button } from '../../components/ui/button'
import { Badge } from '../../components/ui/badge'
import { 
  ArrowLeft, 
  Calendar, 
  User, 
  Clock, 
  FileText, 
  Phone, 
  MapPin,
  CheckCircle,
  XCircle,
  AlertCircle,
  Edit,
  Building2
} from 'lucide-react'
import { format } from 'date-fns'
import { fr } from 'date-fns/locale'
import { AnimatedContainer, AnimatedStagger } from '../../components/ui/animated-page'

const STATUT_COLORS = {
  planifie: 'bg-blue-500/20 text-blue-500',
  confirme: 'bg-green-500/20 text-green-500',
  en_cours: 'bg-yellow-500/20 text-yellow-500',
  termine: 'bg-gray-500/20 text-gray-500',
  annule: 'bg-red-500/20 text-red-500',
  absent: 'bg-orange-500/20 text-orange-500',
}

const STATUT_LABELS = {
  planifie: 'Planifié',
  confirme: 'Confirmé',
  en_cours: 'En cours',
  termine: 'Terminé',
  annule: 'Annulé',
  absent: 'Absent',
}

const STATUT_ICONS = {
  planifie: Clock,
  confirme: CheckCircle,
  en_cours: AlertCircle,
  termine: CheckCircle,
  annule: XCircle,
  absent: XCircle,
}

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

export const RendezVousDetail = () => {
  const { id: idWithSlug } = useParams()
  const navigate = useNavigate()
  const id = extractIdFromSlug(idWithSlug)
  const [rendezVous, setRendezVous] = useState(null)
  const [patient, setPatient] = useState(null)
  const [hopitaux, setHopitaux] = useState([])
  const [patientStats, setPatientStats] = useState({
    totalRendezVous: 0,
    totalConsultations: 0,
    dernierRendezVous: null,
    derniereConsultation: null
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (id) {
      fetchRendezVousData()
    }
  }, [id])

  const fetchRendezVousData = async () => {
    try {
      setLoading(true)
      
      // Récupérer les données du rendez-vous
      const rendezVousResponse = await rendezVousService.getById(id)
      const rendezVousData = rendezVousResponse.data
      setRendezVous(rendezVousData)
      
      // Récupérer la liste des hôpitaux pour les noms
      try {
        const hopitauxResponse = await hopitauxService.getAll()
        const hopitauxData = Array.isArray(hopitauxResponse.data) 
          ? hopitauxResponse.data 
          : (hopitauxResponse.data?.results || [])
        setHopitaux(hopitauxData)
      } catch (error) {
        console.warn('Erreur lors du chargement des hôpitaux:', error)
        setHopitaux([])
      }
      
      // Récupérer les données du patient
      if (rendezVousData.patient) {
        const patientResponse = await patientsService.getById(rendezVousData.patient)
        setPatient(patientResponse.data)
        
        // Récupérer les statistiques du patient
        await fetchPatientStats(rendezVousData.patient)
      }
      
    } catch (error) {
      console.error('Erreur lors du chargement des données du rendez-vous:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchPatientStats = async (patientId) => {
    try {
      // Récupérer tous les rendez-vous du patient
      const rendezVousResponse = await rendezVousService.getAll({ patient: patientId })
      const rendezVousData = Array.isArray(rendezVousResponse.data) 
        ? rendezVousResponse.data 
        : (rendezVousResponse.data?.results || [])
      
      // Récupérer toutes les consultations du patient
      const consultationsResponse = await consultationsService.getAll({ patient: patientId })
      const consultationsData = Array.isArray(consultationsResponse.data) 
        ? consultationsResponse.data 
        : (consultationsResponse.data?.results || [])
      
      // Calculer les statistiques
      const totalRendezVous = rendezVousData.length
      const totalConsultations = consultationsData.length
      
      // Dernier rendez-vous (excluant le rendez-vous actuel)
      const autresRendezVous = rendezVousData.filter(rdv => rdv.id !== parseInt(id))
      const dernierRendezVous = autresRendezVous
        .sort((a, b) => new Date(b.datetime) - new Date(a.datetime))[0] || null
      
      // Dernière consultation
      const derniereConsultation = consultationsData
        .sort((a, b) => new Date(b.date) - new Date(a.date))[0] || null
      
      setPatientStats({
        totalRendezVous,
        totalConsultations,
        dernierRendezVous,
        derniereConsultation
      })
      
    } catch (error) {
      console.error('Erreur lors du chargement des statistiques du patient:', error)
    }
  }

  const calculateAge = (dob) => {
    if (!dob) return '-'
    const today = new Date()
    const birthDate = new Date(dob)
    let age = today.getFullYear() - birthDate.getFullYear()
    const monthDiff = today.getMonth() - birthDate.getMonth()
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
      age--
    }
    return age
  }

  const formatDate = (dateString) => {
    try {
      if (!dateString) return 'Date inconnue'
      const date = new Date(dateString)
      if (isNaN(date.getTime())) return 'Date invalide'
      return format(date, 'dd MMM yyyy à HH:mm', { locale: fr })
    } catch (error) {
      console.warn('Erreur de formatage de date:', dateString, error)
      return 'Date invalide'
    }
  }

  const formatDateOnly = (dateString) => {
    try {
      if (!dateString) return 'Date inconnue'
      const date = new Date(dateString)
      if (isNaN(date.getTime())) return 'Date invalide'
      return format(date, 'dd MMM yyyy', { locale: fr })
    } catch (error) {
      console.warn('Erreur de formatage de date:', dateString, error)
      return 'Date invalide'
    }
  }

  const getStatusColor = (statut) => {
    switch (statut) {
      case 'confirme':
      case 'termine':
        return 'success'
      case 'planifie':
        return 'info'
      case 'en_cours':
        return 'warning'
      case 'annule':
      case 'absent':
        return 'danger'
      default:
        return 'primary'
    }
  }

  const isUpcoming = (datetime) => {
    return new Date(datetime) > new Date()
  }

  const getHopitalName = (hopitalId) => {
    if (!hopitalId || !Array.isArray(hopitaux)) return 'Hôpital non spécifié'
    const hopital = hopitaux.find(h => h.id === hopitalId)
    return hopital ? hopital.nom : `Hôpital #${hopitalId}`
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Chargement des données du rendez-vous...</p>
        </div>
      </div>
    )
  }

  if (!rendezVous) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <XCircle className="h-12 w-12 text-destructive mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">Rendez-vous non trouvé</h2>
          <p className="text-muted-foreground mb-4">Le rendez-vous demandé n'existe pas ou a été supprimé.</p>
          <Button onClick={() => navigate('/rendez-vous')}>
            <ArrowLeft className="h-4 w-4 mr-2" />
            Retour à la liste
          </Button>
        </div>
      </div>
    )
  }

  const StatusIcon = STATUT_ICONS[rendezVous.statut] || Clock

  return (
    <div className="space-y-6">
      <AnimatedContainer>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button 
              variant="outline" 
              size="icon"
              onClick={() => navigate('/rendez-vous')}
            >
              <ArrowLeft className="h-4 w-4" />
            </Button>
            <div>
              <h1 className="text-3xl font-bold">
                Rendez-vous #{rendezVous.id}
              </h1>
              <p className="text-muted-foreground">
                {formatDate(rendezVous.datetime)}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Badge className={STATUT_COLORS[rendezVous.statut]} variant="secondary">
              <StatusIcon className="h-3 w-3 mr-1" />
              {STATUT_LABELS[rendezVous.statut]}
            </Badge>
            <Button variant="outline" size="sm">
              <Edit className="h-4 w-4 mr-2" />
              Modifier
            </Button>
          </div>
        </div>
      </AnimatedContainer>

      {/* Informations générales */}
      <AnimatedStagger className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6" staggerDelay={0.1}>
        <StatCard
          title="Statut"
          value={STATUT_LABELS[rendezVous.statut]}
          description={isUpcoming(rendezVous.datetime) ? "À venir" : "Passé"}
          icon={StatusIcon}
          color={getStatusColor(rendezVous.statut)}
        />
        <StatCard
          title="Patient"
          value={patient ? `${patient.prenom} ${patient.nom}` : 'Chargement...'}
          description={patient ? `${calculateAge(patient.dob)} ans` : ''}
          icon={User}
          color="primary"
        />
        <StatCard
          title="RDV Patient"
          value={patientStats.totalRendezVous}
          description="Total rendez-vous"
          icon={Calendar}
          color="info"
        />
        <StatCard
          title="Consultations"
          value={patientStats.totalConsultations}
          description="Total consultations"
          icon={FileText}
          color="warning"
        />
      </AnimatedStagger>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Détails du rendez-vous */}
        <AnimatedContainer delay={0.2}>
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="h-5 w-5" />
                Détails du rendez-vous
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Date et heure</p>
                <p className="text-lg font-semibold">{formatDate(rendezVous.datetime)}</p>
                {isUpcoming(rendezVous.datetime) ? (
                  <Badge className="bg-blue-500/20 text-blue-500 mt-1">À venir</Badge>
                ) : (
                  <Badge className="bg-gray-500/20 text-gray-500 mt-1">Passé</Badge>
                )}
              </div>
              
              <div>
                <p className="text-sm font-medium text-muted-foreground">Statut actuel</p>
                <Badge className={STATUT_COLORS[rendezVous.statut]} variant="secondary">
                  <StatusIcon className="h-3 w-3 mr-1" />
                  {STATUT_LABELS[rendezVous.statut]}
                </Badge>
              </div>
              
              <div>
                <p className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                  <Building2 className="h-3 w-3" />
                  Hôpital
                </p>
                <p className="font-medium">{getHopitalName(rendezVous.hopital)}</p>
              </div>
              
              <div>
                <p className="text-sm font-medium text-muted-foreground">Créé le</p>
                <p>{formatDate(rendezVous.created_at)}</p>
              </div>
              
              {rendezVous.updated_at && rendezVous.updated_at !== rendezVous.created_at && (
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Dernière modification</p>
                  <p>{formatDate(rendezVous.updated_at)}</p>
                </div>
              )}
              
              {rendezVous.notes && (
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Notes</p>
                  <p className="text-sm bg-muted p-3 rounded">{rendezVous.notes}</p>
                </div>
              )}
              
              {!rendezVous.notes && (
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Notes</p>
                  <p className="text-sm text-muted-foreground italic">Aucune note ajoutée</p>
                </div>
              )}
            </CardContent>
          </Card>
        </AnimatedContainer>

        {/* Informations du patient */}
        <AnimatedContainer delay={0.3}>
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="h-5 w-5" />
                Informations du patient
              </CardTitle>
              {patient && (
                <CardDescription>
                  <Button 
                    variant="link" 
                    className="p-0 h-auto text-primary"
                    onClick={() => {
                      const slug = generatePatientSlug(patient.nom, patient.prenom)
                      const urlPath = generateUrlWithSlug(patient.id, slug)
                      navigate(`/patients/${urlPath}`)
                    }}
                  >
                    Voir le profil complet →
                  </Button>
                </CardDescription>
              )}
            </CardHeader>
            <CardContent className="space-y-4">
              {patient ? (
                <>
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Nom complet</p>
                    <p className="text-lg font-semibold">{patient.prenom} {patient.nom}</p>
                  </div>
                  
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Âge et sexe</p>
                    <p>{calculateAge(patient.dob)} ans • {patient.sexe === 'F' ? 'Féminin' : 'Masculin'}</p>
                  </div>
                  
                  {patient.telephone && (
                    <div>
                      <p className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                        <Phone className="h-3 w-3" />
                        Téléphone
                      </p>
                      <p>{patient.telephone}</p>
                    </div>
                  )}
                  
                  {patient.adresse && (
                    <div>
                      <p className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                        <MapPin className="h-3 w-3" />
                        Adresse
                      </p>
                      <p>{patient.adresse}</p>
                    </div>
                  )}
                  
                  {patient.allergies && (
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">Allergies importantes</p>
                      <p className="text-sm bg-orange-50 border border-orange-200 p-2 rounded text-orange-800">
                        {patient.allergies}
                      </p>
                    </div>
                  )}
                </>
              ) : (
                <div className="text-center py-4">
                  <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary mx-auto mb-2"></div>
                  <p className="text-sm text-muted-foreground">Chargement des informations du patient...</p>
                </div>
              )}
            </CardContent>
          </Card>
        </AnimatedContainer>
      </div>

      {/* Historique du patient */}
      {patient && (
        <AnimatedContainer delay={0.4}>
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Clock className="h-5 w-5" />
                Historique récent du patient
              </CardTitle>
              <CardDescription>
                Dernières activités de {patient.prenom} {patient.nom}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Dernier rendez-vous */}
                <div>
                  <h4 className="font-medium mb-3">Dernier rendez-vous</h4>
                  {patientStats.dernierRendezVous ? (
                    <div className="bg-muted p-3 rounded">
                      <p className="text-sm font-medium">
                        {formatDate(patientStats.dernierRendezVous.datetime)}
                      </p>
                      <Badge className={STATUT_COLORS[patientStats.dernierRendezVous.statut]} size="sm">
                        {STATUT_LABELS[patientStats.dernierRendezVous.statut]}
                      </Badge>
                      {patientStats.dernierRendezVous.notes && (
                        <p className="text-xs text-muted-foreground mt-1">
                          {patientStats.dernierRendezVous.notes.substring(0, 80)}
                          {patientStats.dernierRendezVous.notes.length > 80 ? '...' : ''}
                        </p>
                      )}
                    </div>
                  ) : (
                    <p className="text-sm text-muted-foreground italic">
                      Aucun autre rendez-vous enregistré
                    </p>
                  )}
                </div>

                {/* Dernière consultation */}
                <div>
                  <h4 className="font-medium mb-3">Dernière consultation</h4>
                  {patientStats.derniereConsultation ? (
                    <div className="bg-muted p-3 rounded">
                      <p className="text-sm font-medium">
                        {formatDate(patientStats.derniereConsultation.date)}
                      </p>
                      {patientStats.derniereConsultation.methode_proposee_nom && (
                        <Badge variant="outline" className="mt-1">
                          {patientStats.derniereConsultation.methode_proposee_nom}
                        </Badge>
                      )}
                      {patientStats.derniereConsultation.notes && (
                        <p className="text-xs text-muted-foreground mt-1">
                          {patientStats.derniereConsultation.notes.substring(0, 80)}
                          {patientStats.derniereConsultation.notes.length > 80 ? '...' : ''}
                        </p>
                      )}
                    </div>
                  ) : (
                    <p className="text-sm text-muted-foreground italic">
                      Aucune consultation enregistrée
                    </p>
                  )}
                </div>
              </div>
              
              <div className="mt-4 pt-4 border-t">
                <Button 
                  variant="outline" 
                  onClick={() => {
                    const slug = generatePatientSlug(patient.nom, patient.prenom)
                    const urlPath = generateUrlWithSlug(patient.id, slug)
                    navigate(`/patients/${urlPath}`)
                  }}
                  className="w-full"
                >
                  Voir le profil complet du patient
                </Button>
              </div>
            </CardContent>
          </Card>
        </AnimatedContainer>
      )}
    </div>
  )
}