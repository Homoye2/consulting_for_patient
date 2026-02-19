import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../../components/ui/table'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '../../components/ui/dialog'
import { Button } from '../../components/ui/button'
import { FileText, Eye } from 'lucide-react'
import { consultationsService } from '../../services/apiService'
import { format } from 'date-fns'

export const PatientConsultations = () => {
  const [consultations, setConsultations] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedConsultation, setSelectedConsultation] = useState(null)
  const [dialogOpen, setDialogOpen] = useState(false)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      // Les patients voient automatiquement leurs propres consultations grâce au backend
      const response = await consultationsService.getAll()
      const data = Array.isArray(response.data) ? response.data : (response.data?.results || [])
      setConsultations(data)
    } catch (error) {
      console.error('Erreur lors du chargement des consultations:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleViewDetails = (consultation) => {
    setSelectedConsultation(consultation)
    setDialogOpen(true)
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
      <div className="mb-6">
        <h1 className="text-3xl md:text-4xl font-bold mb-2">Mes consultations</h1>
        <p className="text-muted-foreground">
          Consultez l'historique de toutes vos consultations
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Historique des consultations</CardTitle>
          <CardDescription>Toutes vos consultations de planification familiale</CardDescription>
        </CardHeader>
        <CardContent>
          {consultations.length > 0 ? (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Date</TableHead>
                    <TableHead>Professionnel</TableHead>
                    <TableHead>Méthode prescrite</TableHead>
                    <TableHead>Méthode posée</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {consultations.map((consultation) => (
                    <TableRow key={consultation.id}>
                      <TableCell>
                        {format(new Date(consultation.date), "dd MMMM yyyy")}
                      </TableCell>
                      <TableCell>{consultation.professionnel_nom}</TableCell>
                      <TableCell>{consultation.methode_prescite_nom || '-'}</TableCell>
                      <TableCell>
                        {consultation.methode_posee ? (
                          <span className="text-green-600">Oui</span>
                        ) : (
                          <span className="text-muted-foreground">Non</span>
                        )}
                      </TableCell>
                      <TableCell>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleViewDetails(consultation)}
                        >
                          <Eye className="h-4 w-4 mr-2" />
                          Voir détails
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          ) : (
            <div className="text-center py-8">
              <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">Aucune consultation pour le moment</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Dialog Détails */}
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="sm:max-w-[600px] max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Détails de la consultation</DialogTitle>
            <DialogDescription>
              {selectedConsultation && format(new Date(selectedConsultation.date), "dd MMMM yyyy")}
            </DialogDescription>
          </DialogHeader>
          {selectedConsultation && (
            <div className="space-y-4">
              <div>
                <h4 className="font-semibold mb-2">Professionnel</h4>
                <p className="text-muted-foreground">{selectedConsultation.professionnel_nom}</p>
              </div>
              {selectedConsultation.anamnese && (
                <div>
                  <h4 className="font-semibold mb-2">Anamnèse</h4>
                  <p className="text-muted-foreground">{selectedConsultation.anamnese}</p>
                </div>
              )}
              {selectedConsultation.examen && (
                <div>
                  <h4 className="font-semibold mb-2">Examen clinique</h4>
                  <p className="text-muted-foreground">{selectedConsultation.examen}</p>
                </div>
              )}
              {selectedConsultation.methode_prescite_nom && (
                <div>
                  <h4 className="font-semibold mb-2">Méthode prescrite</h4>
                  <p className="text-muted-foreground">{selectedConsultation.methode_prescite_nom}</p>
                </div>
              )}
              <div>
                <h4 className="font-semibold mb-2">Méthode posée</h4>
                <p className="text-muted-foreground">
                  {selectedConsultation.methode_posee ? 'Oui' : 'Non'}
                </p>
              </div>
              {selectedConsultation.effets_secondaires && (
                <div>
                  <h4 className="font-semibold mb-2">Effets secondaires</h4>
                  <p className="text-muted-foreground">{selectedConsultation.effets_secondaires}</p>
                </div>
              )}
              {selectedConsultation.notes && (
                <div>
                  <h4 className="font-semibold mb-2">Notes</h4>
                  <p className="text-muted-foreground">{selectedConsultation.notes}</p>
                </div>
              )}
              {selectedConsultation.observation && (
                <div>
                  <h4 className="font-semibold mb-2">Observation</h4>
                  <p className="text-muted-foreground">{selectedConsultation.observation}</p>
                </div>
              )}
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  )
}

