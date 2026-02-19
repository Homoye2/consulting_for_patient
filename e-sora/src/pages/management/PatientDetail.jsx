import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { 
  patientsService, 
  rendezVousService, 
  consultationsService,
  hopitauxService
} from '../../services/apiService'
import { extractIdFromSlug } from '../../lib/slugUtils'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card'
import { Button } from '../../components/ui/button'
import { Badge } from '../../components/ui/badge'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../../components/ui/table'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs'
import { 
  ArrowLeft, 
  User, 
  Calendar, 
  FileText, 
  Phone, 
  MapPin, 
  AlertTriangle,
  Heart,
  Clock,
  CheckCircle,
  XCircle,
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

export const PatientDetail = () => {
  const { id: idWithSlug } = useParams()
  const navigate = useNavigate()
  const id = extractIdFromSlug(idWithSlug)
  const [patient, setPatient] = useState(null)
  const [rendezVous, setRendezVous] = useState([])
  const [consultations, setConsultations] = useState([])
  const [hopitaux, setHopitaux] = useState([])
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({
    totalRendezVous: 0,
    rendezVousConfirmes: 0,
    rendezVousAnnules: 0,
    totalConsultations: 0,
    derniereConsultation: null,
    prochainRendezVous: null
  })

  useEffect(() => {
    if (id) {
      fetchPatientData()
    }
  }, [id])

  const fetchPatientData = async () => {
    try {
      setLoading(true)
      
      // Récupérer les données du patient
      const patientResponse = await patientsService.getById(id)
      setPatient(patientResponse.data)
      
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
      
      // Récupérer les rendez-vous du patient
      const rendezVousResponse = await rendezVousService.getAll({ patient: id })
      const rendezVousData = Array.isArray(rendezVousResponse.data) 
        ? rendezVousResponse.data 
        : (rendezVousResponse.data?.results || [])
      setRendezVous(rendezVousData)
      
      // Récupérer les consultations du patient
      const consultationsResponse = await consultationsService.getAll({ patient: id })
      const consultationsData = Array.isArray(consultationsResponse.data) 
        ? consultationsResponse.data 
        : (consultationsResponse.data?.results || [])
      setConsultations(consultationsData)
      
      // Calculer les statistiques
      calculateStats(rendezVousData, consultationsData)
      
    } catch (error) {
      console.error('Erreur lors du chargement des données du patient:', error)
    } finally {
      setLoading(false)
    }
  }

  const calculateStats = (rendezVousData, consultationsData) => {
    const now = new Date()
    
    // Statistiques des rendez-vous
    const totalRendezVous = rendezVousData.length
    const rendezVousConfirmes = rendezVousData.filter(rdv => rdv.statut === 'confirme').length
    const rendezVousAnnules = rendezVousData.filter(rdv => rdv.statut === 'annule').length
    
    // Prochain rendez-vous
    const futureRendezVous = rendezVousData
      .filter(rdv => new Date(rdv.datetime) > now && rdv.statut !== 'annule')
      .sort((a, b) => new Date(a.datetime) - new Date(b.datetime))
    const prochainRendezVous = futureRendezVous[0] || null
    
    // Statistiques des consultations
    const totalConsultations = consultationsData.length
    
    // Dernière consultation
    const derniereConsultation = consultationsData
      .sort((a, b) => new Date(b.date) - new Date(a.date))[0] || null
    
    setStats({
      totalRendezVous,
      rendezVousConfirmes,
      rendezVousAnnules,
      totalConsultations,
      derniereConsultation,
      prochainRendezVous
    })
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
          <p className="text-muted-foreground">Chargement des données du patient...</p>
        </div>
      </div>
    )
  }

  if (!patient) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <XCircle className="h-12 w-12 text-destructive mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">Patient non trouvé</h2>
          <p className="text-muted-foreground mb-4">Le patient demandé n'existe pas ou a été supprimé.</p>
          <Button onClick={() => navigate('/patients')}>
            <ArrowLeft className="h-4 w-4 mr-2" />
            Retour à la liste
          </Button>
        </div>
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
              size="icon"
              onClick={() => navigate('/patients')}
            >
              <ArrowLeft className="h-4 w-4" />
            </Button>
            <div>
              <h1 className="text-3xl font-bold">
                {patient.prenom} {patient.nom}
              </h1>
              <p className="text-muted-foreground">
                Détails du patient • ID: {patient.id}
              </p>
            </div>
          </div>
        </div>
      </AnimatedContainer>

      {/* Informations générales */}
      <AnimatedStagger className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6" staggerDelay={0.1}>
        <StatCard
          title="Rendez-vous Total"
          value={stats.totalRendezVous}
          description="Tous les rendez-vous"
          icon={Calendar}
          color="primary"
        />
        <StatCard
          title="RDV Confirmés"
          value={stats.rendezVousConfirmes}
          description="Rendez-vous confirmés"
          icon={CheckCircle}
          color="success"
        />
        <StatCard
          title="Consultations"
          value={stats.totalConsultations}
          description="Consultations effectuées"
          icon={FileText}
          color="info"
        />
        <StatCard
          title="Âge"
          value={`${calculateAge(patient.dob)} ans`}
          description={patient.sexe === 'F' ? 'Féminin' : 'Masculin'}
          icon={User}
          color="warning"
        />
      </AnimatedStagger>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Informations personnelles */}
        <AnimatedContainer delay={0.2}>
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="h-5 w-5" />
                Informations personnelles
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Nom complet</p>
                <p className="text-lg font-semibold">{patient.prenom} {patient.nom}</p>
              </div>
              
              <div>
                <p className="text-sm font-medium text-muted-foreground">Date de naissance</p>
                <p>{patient.dob ? formatDateOnly(patient.dob) : 'Non renseignée'}</p>
              </div>
              
              <div>
                <p className="text-sm font-medium text-muted-foreground">Sexe</p>
                <p>{patient.sexe === 'F' ? 'Féminin' : 'Masculin'}</p>
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
            </CardContent>
          </Card>
        </AnimatedContainer>

        {/* Informations médicales */}
        <AnimatedContainer delay={0.3}>
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Heart className="h-5 w-5" />
                Informations médicales
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {patient.antecedents ? (
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Antécédents</p>
                  <p className="text-sm bg-muted p-2 rounded">{patient.antecedents}</p>
                </div>
              ) : (
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Antécédents</p>
                  <p className="text-sm text-muted-foreground italic">Aucun antécédent renseigné</p>
                </div>
              )}
              
              {patient.allergies ? (
                <div>
                  <p className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                    <AlertTriangle className="h-3 w-3 text-orange-500" />
                    Allergies
                  </p>
                  <p className="text-sm bg-orange-50 border border-orange-200 p-2 rounded text-orange-800">
                    {patient.allergies}
                  </p>
                </div>
              ) : (
                <div>
                  <p className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                    <AlertTriangle className="h-3 w-3" />
                    Allergies
                  </p>
                  <p className="text-sm text-muted-foreground italic">Aucune allergie connue</p>
                </div>
              )}
            </CardContent>
          </Card>
        </AnimatedContainer>

        {/* Résumé récent */}
        <AnimatedContainer delay={0.4}>
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Clock className="h-5 w-5" />
                Activité récente
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {stats.prochainRendezVous ? (
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Prochain rendez-vous</p>
                  <div className="bg-blue-50 border border-blue-200 p-2 rounded">
                    <p className="text-sm font-medium text-blue-800">
                      {formatDate(stats.prochainRendezVous.datetime)}
                    </p>
                    <Badge className={STATUT_COLORS[stats.prochainRendezVous.statut]}>
                      {STATUT_LABELS[stats.prochainRendezVous.statut]}
                    </Badge>
                  </div>
                </div>
              ) : (
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Prochain rendez-vous</p>
                  <p className="text-sm text-muted-foreground italic">Aucun rendez-vous planifié</p>
                </div>
              )}
              
              {stats.derniereConsultation ? (
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Dernière consultation</p>
                  <div className="bg-green-50 border border-green-200 p-2 rounded">
                    <p className="text-sm font-medium text-green-800">
                      {formatDate(stats.derniereConsultation.date)}
                    </p>
                    {stats.derniereConsultation.notes && (
                      <p className="text-xs text-green-700 mt-1">
                        {stats.derniereConsultation.notes.substring(0, 100)}
                        {stats.derniereConsultation.notes.length > 100 ? '...' : ''}
                      </p>
                    )}
                  </div>
                </div>
              ) : (
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Dernière consultation</p>
                  <p className="text-sm text-muted-foreground italic">Aucune consultation enregistrée</p>
                </div>
              )}
            </CardContent>
          </Card>
        </AnimatedContainer>
      </div>

      {/* Onglets pour les détails */}
      <AnimatedContainer delay={0.5}>
        <Tabs defaultValue="rendez-vous" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="rendez-vous">
              Rendez-vous ({rendezVous.length})
            </TabsTrigger>
            <TabsTrigger value="consultations">
              Consultations ({consultations.length})
            </TabsTrigger>
          </TabsList>

          <TabsContent value="rendez-vous" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Historique des rendez-vous</CardTitle>
                <CardDescription>
                  Tous les rendez-vous de ce patient
                </CardDescription>
              </CardHeader>
              <CardContent>
                {rendezVous.length === 0 ? (
                  <div className="text-center py-8">
                    <Calendar className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                    <h3 className="text-lg font-semibold mb-2">Aucun rendez-vous</h3>
                    <p className="text-muted-foreground">
                      Ce patient n'a pas encore de rendez-vous enregistré.
                    </p>
                  </div>
                ) : (
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Date et heure</TableHead>
                        <TableHead>Statut</TableHead>
                        <TableHead>Hôpital</TableHead>
                        <TableHead>Notes</TableHead>
                        <TableHead>Créé le</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {rendezVous
                        .sort((a, b) => new Date(b.datetime) - new Date(a.datetime))
                        .map((rdv) => (
                        <TableRow key={rdv.id}>
                          <TableCell className="font-medium">
                            {formatDate(rdv.datetime)}
                          </TableCell>
                          <TableCell>
                            <Badge className={STATUT_COLORS[rdv.statut]}>
                              {STATUT_LABELS[rdv.statut]}
                            </Badge>
                          </TableCell>
                          <TableCell>
                            <div className="flex items-center gap-1">
                              <Building2 className="h-3 w-3 text-muted-foreground" />
                              <span className="text-sm">{getHopitalName(rdv.hopital)}</span>
                            </div>
                          </TableCell>
                          <TableCell>
                            {rdv.notes ? (
                              <span className="text-sm">
                                {rdv.notes.length > 50 
                                  ? `${rdv.notes.substring(0, 50)}...` 
                                  : rdv.notes}
                              </span>
                            ) : (
                              <span className="text-muted-foreground italic">Aucune note</span>
                            )}
                          </TableCell>
                          <TableCell className="text-muted-foreground">
                            {formatDateOnly(rdv.created_at)}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="consultations" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Historique des consultations</CardTitle>
                <CardDescription>
                  Toutes les consultations de ce patient
                </CardDescription>
              </CardHeader>
              <CardContent>
                {consultations.length === 0 ? (
                  <div className="text-center py-8">
                    <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                    <h3 className="text-lg font-semibold mb-2">Aucune consultation</h3>
                    <p className="text-muted-foreground">
                      Ce patient n'a pas encore de consultation enregistrée.
                    </p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {consultations
                      .sort((a, b) => new Date(b.date) - new Date(a.date))
                      .map((consultation) => (
                      <Card key={consultation.id} className="border-l-4 border-l-primary">
                        <CardHeader className="pb-3">
                          <div className="flex items-center justify-between">
                            <CardTitle className="text-lg">
                              Consultation du {formatDate(consultation.date)}
                            </CardTitle>
                            <Badge variant="outline">
                              ID: {consultation.id}
                            </Badge>
                          </div>
                        </CardHeader>
                        <CardContent className="space-y-3">
                          {consultation.anamnese && (
                            <div>
                              <p className="text-sm font-medium text-muted-foreground">Anamnèse</p>
                              <p className="text-sm bg-muted p-2 rounded">{consultation.anamnese}</p>
                            </div>
                          )}
                          
                          {consultation.examen && (
                            <div>
                              <p className="text-sm font-medium text-muted-foreground">Examen</p>
                              <p className="text-sm bg-muted p-2 rounded">{consultation.examen}</p>
                            </div>
                          )}
                          
                          {consultation.methode_proposee_nom && (
                            <div>
                              <p className="text-sm font-medium text-muted-foreground">Méthode proposée</p>
                              <Badge variant="secondary">{consultation.methode_proposee_nom}</Badge>
                            </div>
                          )}
                          
                          {consultation.methode_prescite_nom && (
                            <div>
                              <p className="text-sm font-medium text-muted-foreground">Méthode prescrite</p>
                              <Badge variant="secondary">{consultation.methode_prescite_nom}</Badge>
                            </div>
                          )}
                          
                          {consultation.methode_posee && (
                            <div>
                              <Badge className="bg-green-500/20 text-green-500">
                                Méthode posée
                              </Badge>
                            </div>
                          )}
                          
                          {consultation.effets_secondaires && (
                            <div>
                              <p className="text-sm font-medium text-muted-foreground">Effets secondaires</p>
                              <p className="text-sm bg-orange-50 border border-orange-200 p-2 rounded text-orange-800">
                                {consultation.effets_secondaires}
                              </p>
                            </div>
                          )}
                          
                          {consultation.notes && (
                            <div>
                              <p className="text-sm font-medium text-muted-foreground">Notes</p>
                              <p className="text-sm bg-muted p-2 rounded">{consultation.notes}</p>
                            </div>
                          )}
                          
                          {consultation.observation && (
                            <div>
                              <p className="text-sm font-medium text-muted-foreground">Observation</p>
                              <p className="text-sm bg-muted p-2 rounded">{consultation.observation}</p>
                            </div>
                          )}
                        </CardContent>
                      </Card>
                    ))}
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