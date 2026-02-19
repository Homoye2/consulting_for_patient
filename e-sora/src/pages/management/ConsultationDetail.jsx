import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { 
  consultationsService, 
  patientsService,
  rendezVousService,
  hopitauxService
} from '../../services/apiService'
import { extractIdFromSlug, generatePatientSlug, generateUrlWithSlug } from '../../lib/slugUtils'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card'
import { Button } from '../../components/ui/button'
import { Badge } from '../../components/ui/badge'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '../../components/ui/dialog'
import { 
  ArrowLeft, 
  FileText, 
  User, 
  Calendar, 
  Heart, 
  Phone, 
  MapPin,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Edit,
  Stethoscope,
  Pill,
  ClipboardList,
  Building2,
  Download,
  Printer,
  Share2,
  Copy,
  Mail
} from 'lucide-react'
import { format } from 'date-fns'
import { fr } from 'date-fns/locale'
import { AnimatedContainer, AnimatedStagger } from '../../components/ui/animated-page'
import { useToast } from '../../components/ui/toast'

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

export const ConsultationDetail = () => {
  const { id: idWithSlug } = useParams()
  const navigate = useNavigate()
  const id = extractIdFromSlug(idWithSlug)
  const { showToast, ToastContainer } = useToast()
  const [consultation, setConsultation] = useState(null)
  const [patient, setPatient] = useState(null)
  const [hopitaux, setHopitaux] = useState([])
  const [showConsultationActions, setShowConsultationActions] = useState(false)
  const [patientStats, setPatientStats] = useState({
    totalRendezVous: 0,
    totalConsultations: 0,
    dernierRendezVous: null,
    derniereConsultation: null
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (id) {
      fetchConsultationData()
    }
  }, [id])

  const fetchConsultationData = async () => {
    try {
      setLoading(true)
      
      // Récupérer les données de la consultation
      const consultationResponse = await consultationsService.getById(id)
      const consultationData = consultationResponse.data
      setConsultation(consultationData)
      
      // Récupérer les données du patient
      if (consultationData.patient) {
        const patientResponse = await patientsService.getById(consultationData.patient)
        setPatient(patientResponse.data)
        
        // Récupérer les statistiques du patient
        await fetchPatientStats(consultationData.patient)
      }
      
    } catch (error) {
      console.error('Erreur lors du chargement des données de la consultation:', error)
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
      
      // Dernier rendez-vous
      const dernierRendezVous = rendezVousData
        .sort((a, b) => new Date(b.datetime) - new Date(a.datetime))[0] || null
      
      // Dernière consultation (excluant la consultation actuelle)
      const autresConsultations = consultationsData.filter(cons => cons.id !== parseInt(id))
      const derniereConsultation = autresConsultations
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

  // Fonctions pour les actions de consultation PF
  const handleGenerateReport = () => {
    // Générer un rapport PDF de la consultation
    const reportData = {
      consultation,
      patient,
      date: new Date().toISOString()
    }
    
    // Simuler la génération d'un rapport
    const reportContent = generateConsultationReport(reportData)
    downloadReport(reportContent, `consultation-pf-${consultation.id}-${patient?.nom}-${patient?.prenom}.txt`)
    showToast('Rapport téléchargé avec succès', 'success')
    setShowConsultationActions(false)
  }

  const handlePrintConsultation = () => {
    // Ouvrir la fenêtre d'impression
    window.print()
    showToast('Impression lancée', 'success')
    setShowConsultationActions(false)
  }

  const handleShareConsultation = async () => {
    // Partager les détails de la consultation
    const shareData = {
      title: `Consultation PF #${consultation.id}`,
      text: `Consultation de planification familiale pour ${patient?.prenom} ${patient?.nom} du ${formatDateOnly(consultation.date)}`,
      url: window.location.href
    }

    if (navigator.share) {
      try {
        await navigator.share(shareData)
        showToast('Consultation partagée', 'success')
      } catch (error) {
        if (error.name !== 'AbortError') {
          showToast('Erreur lors du partage', 'error')
        }
      }
    } else {
      // Fallback: copier l'URL dans le presse-papiers
      try {
        await navigator.clipboard.writeText(window.location.href)
        showToast('Lien copié dans le presse-papiers', 'success')
      } catch (error) {
        showToast('Erreur lors de la copie', 'error')
      }
    }
    setShowConsultationActions(false)
  }

  const handleCopyConsultationInfo = async () => {
    // Copier les informations de la consultation
    const consultationInfo = `
Consultation PF #${consultation.id}
Patient: ${patient?.prenom} ${patient?.nom}
Date: ${formatDate(consultation.date)}
Spécialiste: ${consultation.specialiste_nom || 'Non renseigné'}
Hôpital: ${consultation.hopital_nom || 'Non renseigné'}
Méthode posée: ${consultation.methode_posee ? 'Oui' : 'Non'}
${consultation.anamnese ? `Anamnèse: ${consultation.anamnese}` : ''}
${consultation.examen ? `Examen: ${consultation.examen}` : ''}
${consultation.notes ? `Notes: ${consultation.notes}` : ''}
    `.trim()

    try {
      await navigator.clipboard.writeText(consultationInfo)
      showToast('Informations copiées avec succès', 'success')
    } catch (error) {
      showToast('Erreur lors de la copie', 'error')
    }
    setShowConsultationActions(false)
  }

  const handleSendByEmail = () => {
    // Préparer l'email avec les détails de la consultation
    const subject = `Consultation PF #${consultation.id} - ${patient?.prenom} ${patient?.nom}`
    const body = `
Bonjour,

Voici les détails de la consultation de planification familiale :

Patient: ${patient?.prenom} ${patient?.nom}
Date de consultation: ${formatDate(consultation.date)}
Spécialiste: ${consultation.specialiste_nom || 'Non renseigné'}
Hôpital: ${consultation.hopital_nom || 'Non renseigné'}
Méthode posée: ${consultation.methode_posee ? 'Oui' : 'Non'}

${consultation.anamnese ? `Anamnèse: ${consultation.anamnese}` : ''}
${consultation.examen ? `Examen clinique: ${consultation.examen}` : ''}
${consultation.notes ? `Notes: ${consultation.notes}` : ''}
${consultation.observation ? `Observations: ${consultation.observation}` : ''}

Cordialement,
Système de Planification Familiale
    `.trim()

    try {
      const mailtoLink = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`
      window.location.href = mailtoLink
      showToast('Client email ouvert', 'success')
    } catch (error) {
      showToast('Erreur lors de l\'ouverture de l\'email', 'error')
    }
    setShowConsultationActions(false)
  }

  // Fonction utilitaire pour générer le rapport
  const generateConsultationReport = (data) => {
    return `
RAPPORT DE CONSULTATION DE PLANIFICATION FAMILIALE
================================================

Consultation #${data.consultation.id}
Date de génération: ${formatDate(data.date)}

INFORMATIONS PATIENT
-------------------
Nom: ${data.patient?.prenom} ${data.patient?.nom}
Âge: ${calculateAge(data.patient?.dob)} ans
Sexe: ${data.patient?.sexe === 'F' ? 'Féminin' : 'Masculin'}
Téléphone: ${data.patient?.telephone || 'Non renseigné'}
Adresse: ${data.patient?.adresse || 'Non renseignée'}

INFORMATIONS MÉDICALES
---------------------
Spécialiste: ${data.consultation.specialiste_nom || 'Non renseigné'}
Hôpital: ${data.consultation.hopital_nom || 'Non renseigné'}

DÉTAILS DE LA CONSULTATION
-------------------------
Date de consultation: ${formatDate(data.consultation.date)}
Anamnèse: ${data.consultation.anamnese || 'Non renseignée'}
Examen clinique: ${data.consultation.examen || 'Non renseigné'}
Méthode posée: ${data.consultation.methode_posee ? 'Oui' : 'Non'}

EFFETS SECONDAIRES ET OBSERVATIONS
---------------------------------
Effets secondaires: ${data.consultation.effets_secondaires || 'Aucun'}
Notes: ${data.consultation.notes || 'Aucune'}
Observations: ${data.consultation.observation || 'Aucune'}

ANTÉCÉDENTS MÉDICAUX
-------------------
Antécédents: ${data.patient?.antecedents || 'Aucun'}
Allergies: ${data.patient?.allergies || 'Aucune'}

---
Rapport généré automatiquement par le système de planification familiale
    `.trim()
  }

  // Fonction utilitaire pour télécharger le rapport
  const downloadReport = (content, filename) => {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(link.href)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Chargement des données de la consultation...</p>
        </div>
      </div>
    )
  }

  if (!consultation) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <XCircle className="h-12 w-12 text-destructive mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">Consultation non trouvée</h2>
          <p className="text-muted-foreground mb-4">La consultation demandée n'existe pas ou a été supprimée.</p>
          <Button onClick={() => navigate('/consultations')}>
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
              onClick={() => navigate('/consultations')}
            >
              <ArrowLeft className="h-4 w-4" />
            </Button>
            <div>
              <h1 className="text-3xl font-bold">
                Consultation #{consultation.id}
              </h1>
              <p className="text-muted-foreground">
                {formatDate(consultation.date)}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Dialog open={showConsultationActions} onOpenChange={setShowConsultationActions}>
              <DialogTrigger asChild>
                <Button variant="outline" className="consultation-pf-button">
                  <FileText className="h-3 w-3 mr-1" />
                  Consultation PF
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-md">
                <DialogHeader>
                  <DialogTitle className="flex items-center gap-2">
                    <FileText className="h-5 w-5 text-green-600" />
                    Actions Consultation PF
                  </DialogTitle>
                  <DialogDescription>
                    Choisissez une action pour cette consultation de planification familiale
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-3 py-4">
                  <Button 
                    onClick={handleGenerateReport}
                    className="w-full justify-start"
                    variant="outline"
                  >
                    <Download className="h-4 w-4 mr-2" />
                    Télécharger le rapport
                  </Button>
                  
                  <Button 
                    onClick={handlePrintConsultation}
                    className="w-full justify-start"
                    variant="outline"
                  >
                    <Printer className="h-4 w-4 mr-2" />
                    Imprimer la consultation
                  </Button>
                  
                  <Button 
                    onClick={handleShareConsultation}
                    className="w-full justify-start"
                    variant="outline"
                  >
                    <Share2 className="h-4 w-4 mr-2" />
                    Partager la consultation
                  </Button>
                  
                  <Button 
                    onClick={handleCopyConsultationInfo}
                    className="w-full justify-start"
                    variant="outline"
                  >
                    <Copy className="h-4 w-4 mr-2" />
                    Copier les informations
                  </Button>
                  
                  <Button 
                    onClick={handleSendByEmail}
                    className="w-full justify-start"
                    variant="outline"
                  >
                    <Mail className="h-4 w-4 mr-2" />
                    Envoyer par email
                  </Button>
                </div>
              </DialogContent>
            </Dialog>
            
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
          title="Patient"
          value={patient ? `${patient.prenom} ${patient.nom}` : 'Chargement...'}
          description={patient ? `${calculateAge(patient.dob)} ans` : ''}
          icon={User}
          color="primary"
        />
        <StatCard
          title="Méthode posée"
          value={consultation.methode_posee ? "Oui" : "Non"}
          description={consultation.methode_posee ? "Méthode appliquée" : "Pas de pose"}
          icon={consultation.methode_posee ? CheckCircle : XCircle}
          color={consultation.methode_posee ? "success" : "warning"}
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
        {/* Détails de la consultation */}
        <div className="space-y-6">
          <AnimatedContainer delay={0.2}>
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <ClipboardList className="h-5 w-5" />
                  Anamnèse et Examen
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Date de consultation</p>
                  <p className="text-lg font-semibold">{formatDate(consultation.date)}</p>
                </div>
                
                {consultation.anamnese ? (
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Anamnèse</p>
                    <p className="text-sm bg-muted p-3 rounded">{consultation.anamnese}</p>
                  </div>
                ) : (
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Anamnèse</p>
                    <p className="text-sm text-muted-foreground italic">Aucune anamnèse renseignée</p>
                  </div>
                )}
                
                {consultation.examen ? (
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Examen clinique</p>
                    <p className="text-sm bg-muted p-3 rounded">{consultation.examen}</p>
                  </div>
                ) : (
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Examen clinique</p>
                    <p className="text-sm text-muted-foreground italic">Aucun examen renseigné</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </AnimatedContainer>

          <AnimatedContainer delay={0.3}>
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Stethoscope className="h-5 w-5" />
                  Informations Médicales
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Spécialiste</p>
                  <p className="text-lg font-semibold">
                    {consultation.specialiste_nom || 'Non renseigné'}
                  </p>
                  {consultation.specialiste_specialite && (
                    <Badge variant="outline" className="mt-1">
                      {consultation.specialiste_specialite}
                    </Badge>
                  )}
                </div>
                
                <div>
                  <p className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                    <Building2 className="h-3 w-3" />
                    Hôpital
                  </p>
                  <p className="text-lg font-semibold">
                    {consultation.hopital_nom || 'Non renseigné'}
                  </p>
                  {consultation.hopital_adresse && (
                    <p className="text-sm text-muted-foreground mt-1">
                      {consultation.hopital_adresse}
                    </p>
                  )}
                  {consultation.hopital_telephone && (
                    <p className="text-sm text-muted-foreground flex items-center gap-1 mt-1">
                      <Phone className="h-3 w-3" />
                      {consultation.hopital_telephone}
                    </p>
                  )}
                </div>
                
                <div className="pt-2 border-t">
                  <p className="text-sm font-medium text-muted-foreground">Méthode posée</p>
                  {consultation.methode_posee ? (
                    <Badge className="bg-green-500/20 text-green-500">
                      <CheckCircle className="h-3 w-3 mr-1" />
                      Oui, méthode posée
                    </Badge>
                  ) : (
                    <Badge className="bg-gray-500/20 text-gray-500">
                      <XCircle className="h-3 w-3 mr-1" />
                      Non posée
                    </Badge>
                  )}
                </div>
                
                {consultation.effets_secondaires && (
                  <div>
                    <p className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                      <AlertTriangle className="h-3 w-3 text-orange-500" />
                      Effets secondaires
                    </p>
                    <p className="text-sm bg-orange-50 border border-orange-200 p-3 rounded text-orange-800">
                      {consultation.effets_secondaires}
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </AnimatedContainer>
        </div>

        {/* Informations du patient et notes */}
        <div className="space-y-6">
          <AnimatedContainer delay={0.4}>
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
                    
                    {patient.antecedents && (
                      <div>
                        <p className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                          <Heart className="h-3 w-3" />
                          Antécédents
                        </p>
                        <p className="text-sm bg-muted p-2 rounded">{patient.antecedents}</p>
                      </div>
                    )}
                    
                    {patient.allergies && (
                      <div>
                        <p className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                          <AlertTriangle className="h-3 w-3 text-orange-500" />
                          Allergies importantes
                        </p>
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

          <AnimatedContainer delay={0.5}>
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Stethoscope className="h-5 w-5" />
                  Notes et Observations
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {consultation.notes ? (
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Notes de consultation</p>
                    <p className="text-sm bg-muted p-3 rounded">{consultation.notes}</p>
                  </div>
                ) : (
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Notes de consultation</p>
                    <p className="text-sm text-muted-foreground italic">Aucune note ajoutée</p>
                  </div>
                )}
                
                {consultation.observation ? (
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Observations</p>
                    <p className="text-sm bg-muted p-3 rounded">{consultation.observation}</p>
                  </div>
                ) : (
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Observations</p>
                    <p className="text-sm text-muted-foreground italic">Aucune observation ajoutée</p>
                  </div>
                )}
                
                <div className="pt-2 border-t">
                  <p className="text-sm font-medium text-muted-foreground">Informations système</p>
                  <div className="text-xs text-muted-foreground space-y-1 mt-2">
                    <p>Créée le: {formatDate(consultation.created_at)}</p>
                    {consultation.updated_at && consultation.updated_at !== consultation.created_at && (
                      <p>Modifiée le: {formatDate(consultation.updated_at)}</p>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          </AnimatedContainer>
        </div>
      </div>

      {/* Historique du patient */}
      {patient && (
        <AnimatedContainer delay={0.6}>
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="h-5 w-5" />
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
                      <Badge variant="outline" size="sm">
                        {patientStats.dernierRendezVous.statut}
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
                      Aucun rendez-vous enregistré
                    </p>
                  )}
                </div>

                {/* Dernière consultation */}
                <div>
                  <h4 className="font-medium mb-3">Consultation précédente</h4>
                  {patientStats.derniereConsultation ? (
                    <div className="bg-muted p-3 rounded">
                      <p className="text-sm font-medium">
                        {formatDate(patientStats.derniereConsultation.date)}
                      </p>
                      {patientStats.derniereConsultation.specialiste_nom && (
                        <p className="text-xs text-muted-foreground mt-1">
                          Dr. {patientStats.derniereConsultation.specialiste_nom}
                        </p>
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
                      Aucune autre consultation enregistrée
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
      
      <ToastContainer />
    </div>
  )
}