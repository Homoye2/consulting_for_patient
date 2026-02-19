import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { hopitauxService, specialistesService, patientsService, consultationsService, rendezVousService } from '../../services/apiService'
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
  Building2, 
  MapPin, 
  Phone, 
  Mail, 
  Users, 
  UserCheck, 
  Calendar, 
  FileText,
  Activity,
  Clock,
  CheckCircle,
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

export const HopitalDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [hopital, setHopital] = useState(null)
  const [specialistes, setSpecialistes] = useState([])
  const [patients, setPatients] = useState([])
  const [consultations, setConsultations] = useState([])
  const [rendezVous, setRendezVous] = useState([])
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({
    totalSpecialistes: 0,
    totalPatients: 0,
    totalConsultations: 0,
    totalRendezVous: 0,
    rdvConfirmes: 0,
    rdvEnAttente: 0,
    rdvAnnules: 0
  })

  useEffect(() => {
    fetchHopitalData()
  }, [id])

  const fetchHopitalData = async () => {
    try {
      setLoading(true)
      
      // Récupérer les informations de l'hôpital
      const hopitalResponse = await hopitauxService.getById(id)
      setHopital(hopitalResponse.data)
      
      // Récupérer les données liées à l'hôpital en parallèle
      const [
        specialistesResponse,
        consultationsResponse,
        rendezVousResponse
      ] = await Promise.all([
        specialistesService.getAll({ hopital: id }).catch(() => ({ data: [] })),
        consultationsService.getAll({ hopital: id }).catch(() => ({ data: [] })),
        rendezVousService.getAll({ hopital: id }).catch(() => ({ data: [] }))
      ])

      const specialistesData = Array.isArray(specialistesResponse.data) ? specialistesResponse.data : (specialistesResponse.data?.results || [])
      const consultationsData = Array.isArray(consultationsResponse.data) ? consultationsResponse.data : (consultationsResponse.data?.results || [])
      const rendezVousData = Array.isArray(rendezVousResponse.data) ? rendezVousResponse.data : (rendezVousResponse.data?.results || [])

      // Récupérer les patients uniques qui ont eu des consultations ou rendez-vous dans cet hôpital
      const patientIds = new Set()
      consultationsData.forEach(consultation => {
        if (consultation.patient) patientIds.add(consultation.patient)
      })
      rendezVousData.forEach(rdv => {
        if (rdv.patient) patientIds.add(rdv.patient)
      })

      // Récupérer les détails des patients
      let patientsData = []
      if (patientIds.size > 0) {
        try {
          const patientsResponse = await patientsService.getAll()
          const allPatients = Array.isArray(patientsResponse.data) ? patientsResponse.data : (patientsResponse.data?.results || [])
          patientsData = allPatients.filter(patient => patientIds.has(patient.id))
        } catch (error) {
          console.error('Erreur lors du chargement des patients:', error)
        }
      }
      
      setSpecialistes(specialistesData)
      setPatients(patientsData)
      setConsultations(consultationsData)

      setRendezVous(rendezVousData)

      // Calculer les statistiques
      const rdvConfirmes = rendezVousData.filter(rdv => rdv.statut === 'confirme').length
      const rdvEnAttente = rendezVousData.filter(rdv => rdv.statut === 'en_attente').length
      const rdvAnnules = rendezVousData.filter(rdv => rdv.statut === 'annule').length

      setStats({
        totalSpecialistes: specialistesData.length,
        totalPatients: patientsData.length,
        totalConsultations: consultationsData.length,
        totalRendezVous: rendezVousData.length,
        rdvConfirmes,
        rdvEnAttente,
        rdvAnnules
      })

    } catch (error) {
      console.error('Erreur lors du chargement des données de l\'hôpital:', error)
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
      case 'confirme': return 'text-green-600 bg-green-100'
      case 'en_attente': return 'text-yellow-600 bg-yellow-100'
      case 'annule': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    )
  }

  if (!hopital) {
    return (
      <div className="text-center py-8">
        <p className="text-muted-foreground">Hôpital non trouvé</p>
        <Button onClick={() => navigate('/hopitaux')} className="mt-4">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Retour aux hôpitaux
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
              onClick={() => navigate('/hopitaux')}
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Retour
            </Button>
            <div>
              <h1 className="text-3xl font-bold flex items-center gap-2">
                <Building2 className="h-8 w-8 text-primary" />
                {hopital.nom}
              </h1>
              <p className="text-muted-foreground mt-1">
                Détails et activités de l'établissement
              </p>
            </div>
          </div>
          <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
            hopital.actif 
              ? 'bg-green-100 text-green-800' 
              : 'bg-red-100 text-red-800'
          }`}>
            {hopital.actif ? 'Actif' : 'Inactif'}
          </span>
        </div>
      </AnimatedContainer>

      {/* Informations de base */}
      <AnimatedContainer delay={0.1}>
        <Card>
          <CardHeader>
            <CardTitle>Informations de l'établissement</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {hopital.adresse && (
                <div className="flex items-center gap-2">
                  <MapPin className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">{hopital.adresse}</span>
                </div>
              )}
              {hopital.telephone && (
                <div className="flex items-center gap-2">
                  <Phone className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">{hopital.telephone}</span>
                </div>
              )}
              {hopital.email && (
                <div className="flex items-center gap-2">
                  <Mail className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">{hopital.email}</span>
                </div>
              )}
              <div className="flex items-center gap-2">
                <Activity className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">ID: {hopital.id}</span>
              </div>
            </div>
            {hopital.description && (
              <div className="mt-4">
                <p className="text-sm text-muted-foreground">{hopital.description}</p>
              </div>
            )}
          </CardContent>
        </Card>
      </AnimatedContainer>

      {/* Statistiques */}
      <AnimatedStagger className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4" staggerDelay={0.1}>
        <StatCard
          title="Spécialistes"
          value={stats.totalSpecialistes}
          description="Médecins actifs"
          icon={UserCheck}
          color="primary"
        />
        <StatCard
          title="Patients"
          value={stats.totalPatients}
          description="Patients suivis"
          icon={Users}
          color="info"
        />
        <StatCard
          title="Consultations"
          value={stats.totalConsultations}
          description="Total effectuées"
          icon={FileText}
          color="success"
        />
        <StatCard
          title="Rendez-vous"
          value={stats.totalRendezVous}
          description={`${stats.rdvEnAttente} en attente`}
          icon={Calendar}
          color="warning"
        />
      </AnimatedStagger>

      {/* Détails par onglets */}
      <AnimatedContainer delay={0.3}>
        <Tabs defaultValue="specialistes" className="w-full">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="specialistes">Spécialistes ({stats.totalSpecialistes})</TabsTrigger>
            <TabsTrigger value="patients">Patients ({stats.totalPatients})</TabsTrigger>
            <TabsTrigger value="consultations">Consultations ({stats.totalConsultations})</TabsTrigger>
            <TabsTrigger value="rendez-vous">Rendez-vous ({stats.totalRendezVous})</TabsTrigger>
          </TabsList>

          <TabsContent value="specialistes" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Spécialistes de l'hôpital</CardTitle>
              </CardHeader>
              <CardContent>
                {specialistes.length > 0 ? (
                  <div className="rounded-md border">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Nom</TableHead>
                          <TableHead>Spécialité</TableHead>
                          <TableHead>Contact</TableHead>
                          <TableHead>Statut</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {specialistes.map((specialiste) => (
                          <TableRow key={specialiste.id}>
                            <TableCell className="font-medium">
                              {specialiste.user?.nom || specialiste.user_nom || 'N/A'}
                            </TableCell>
                            <TableCell>{specialiste.specialite_nom || specialiste.specialite || 'N/A'}</TableCell>
                            <TableCell>{specialiste?.user_email || specialiste.telephone || 'N/A'}</TableCell>
                            <TableCell>
                              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                                specialiste.actif 
                                  ? 'bg-green-100 text-green-800' 
                                  : 'bg-red-100 text-red-800'
                              }`}>
                                {specialiste.actif ? 'Actif' : 'Inactif'}
                              </span>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <UserCheck className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                    <p className="text-muted-foreground">Aucun spécialiste enregistré</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="patients" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Patients de l'hôpital</CardTitle>
              </CardHeader>
              <CardContent>
                {patients.length > 0 ? (
                  <div className="rounded-md border">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Nom</TableHead>
                          <TableHead>Âge</TableHead>
                          <TableHead>Contact</TableHead>
                          <TableHead>Dernière visite</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {patients.map((patient) => (
                          <TableRow key={patient.id}>
                            <TableCell className="font-medium">
                              {patient.nom} {patient.prenom}
                            </TableCell>
                            <TableCell>{patient.age || 'N/A'}</TableCell>
                            <TableCell>{patient.telephone || 'N/A'}</TableCell>
                            <TableCell>{formatDate(patient.updated_at)}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <Users className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                    <p className="text-muted-foreground">Aucun patient enregistré</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="consultations" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Consultations récentes</CardTitle>
              </CardHeader>
              <CardContent>
                {consultations.length > 0 ? (
                  <div className="rounded-md border">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Date</TableHead>
                          <TableHead>Patient</TableHead>
                          <TableHead>Spécialiste</TableHead>
                          <TableHead>Type</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {consultations.map((consultation) => (
                          <TableRow key={consultation.id}>
                            <TableCell>{formatDate(consultation.date)}</TableCell>
                            <TableCell className="font-medium">
                              {consultation.patient_nom_complet} 
                            </TableCell>
                            <TableCell>
                              {consultation.professionnel_nom || 'N/A'}
                            </TableCell>
                            <TableCell>Consultation PF</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                    <p className="text-muted-foreground">Aucune consultation enregistrée</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="rendez-vous" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <StatCard
                title="Confirmés"
                value={stats.rdvConfirmes}
                icon={CheckCircle}
                color="success"
              />
              <StatCard
                title="En attente"
                value={stats.rdvEnAttente}
                icon={Clock}
                color="warning"
              />
              <StatCard
                title="Annulés"
                value={stats.rdvAnnules}
                icon={XCircle}
                color="danger"
              />
            </div>
            
            <Card>
              <CardHeader>
                <CardTitle>Rendez-vous récents</CardTitle>
              </CardHeader>
              <CardContent>
                {rendezVous.length > 0 ? (
                  <div className="rounded-md border">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Date & Heure</TableHead>
                          <TableHead>Patient</TableHead>
                          <TableHead>Spécialiste</TableHead>
                          <TableHead>Statut</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {rendezVous.map((rdv) => (
                          <TableRow key={rdv.id}>
                            <TableCell>{formatDate(rdv.datetime)}</TableCell>
                            <TableCell className="font-medium">
                              {rdv.patient_nom} {rdv.patient_prenom}
                            </TableCell>
                            <TableCell>
                              {rdv.specialiste_nom || rdv.specialiste?.nom || 'N/A'}
                            </TableCell>
                            <TableCell>
                              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatutColor(rdv.statut)}`}>
                                {rdv.statut === 'confirme' && <CheckCircle className="h-3 w-3 mr-1" />}
                                {rdv.statut === 'en_attente' && <Clock className="h-3 w-3 mr-1" />}
                                {rdv.statut === 'annule' && <XCircle className="h-3 w-3 mr-1" />}
                                {rdv.statut === 'confirme' ? 'Confirmé' : 
                                 rdv.statut === 'en_attente' ? 'En attente' : 
                                 rdv.statut === 'annule' ? 'Annulé' : rdv.statut}
                              </span>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <Calendar className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                    <p className="text-muted-foreground">Aucun rendez-vous enregistré</p>
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