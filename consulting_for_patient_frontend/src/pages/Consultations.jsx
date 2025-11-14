import { useState, useEffect } from 'react'
import { consultationsService, patientsService, methodesService } from '../services/apiService'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../components/ui/table'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '../components/ui/dialog'
import { Label } from '../components/ui/label'
import { Plus, Search, Edit, Trash2 } from 'lucide-react'
import { format } from 'date-fns'

export const Consultations = () => {
  const [consultations, setConsultations] = useState([])
  const [patients, setPatients] = useState([])
  const [methodes, setMethodes] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editingConsultation, setEditingConsultation] = useState(null)
  const [formData, setFormData] = useState({
    patient: '',
    date: new Date().toISOString().slice(0, 16),
    anamnese: '',
    examen: '',
    methode_proposee: '',
    methode_prescite: '',
    methode_posee: false,
    effets_secondaires: '',
    notes: '',
    observation: '',
  })

  useEffect(() => {
    fetchConsultations()
    fetchPatients()
    fetchMethodes()
  }, [searchTerm])

  const fetchConsultations = async () => {
    try {
      setLoading(true)
      const params = searchTerm ? { search: searchTerm } : {}
      const response = await consultationsService.getAll(params)
      setConsultations(response.data.results || response.data)
    } catch (error) {
      console.error('Erreur lors du chargement des consultations:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchPatients = async () => {
    try {
      const response = await patientsService.getAll()
      setPatients(response.data.results || response.data)
    } catch (error) {
      console.error('Erreur lors du chargement des patients:', error)
    }
  }

  const fetchMethodes = async () => {
    try {
      const response = await methodesService.getAll()
      setMethodes(response.data.results || response.data)
    } catch (error) {
      console.error('Erreur lors du chargement des méthodes:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const data = {
        ...formData,
        patient: parseInt(formData.patient),
        methode_proposee: formData.methode_proposee ? parseInt(formData.methode_proposee) : null,
        methode_prescite: formData.methode_prescite ? parseInt(formData.methode_prescite) : null,
        methode_posee: formData.methode_posee === 'true' || formData.methode_posee === true,
      }
      if (editingConsultation) {
        await consultationsService.update(editingConsultation.id, data)
      } else {
        await consultationsService.create(data)
      }
      setDialogOpen(false)
      resetForm()
      fetchConsultations()
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error)
      alert('Erreur lors de la sauvegarde')
    }
  }

  const handleEdit = (consultation) => {
    setEditingConsultation(consultation)
    setFormData({
      patient: consultation.patient?.id || consultation.patient || '',
      date: consultation.date ? consultation.date.slice(0, 16) : new Date().toISOString().slice(0, 16),
      anamnese: consultation.anamnese || '',
      examen: consultation.examen || '',
      methode_proposee: consultation.methode_proposee?.id || consultation.methode_proposee || '',
      methode_prescite: consultation.methode_prescite?.id || consultation.methode_prescite || '',
      methode_posee: consultation.methode_posee || false,
      effets_secondaires: consultation.effets_secondaires || '',
      notes: consultation.notes || '',
      observation: consultation.observation || '',
    })
    setDialogOpen(true)
  }

  const handleDelete = async (id) => {
    if (confirm('Êtes-vous sûr de vouloir supprimer cette consultation ?')) {
      try {
        await consultationsService.delete(id)
        fetchConsultations()
      } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        alert('Erreur lors de la suppression')
      }
    }
  }

  const resetForm = () => {
    setEditingConsultation(null)
    setFormData({
      patient: '',
      date: new Date().toISOString().slice(0, 16),
      anamnese: '',
      examen: '',
      methode_proposee: '',
      methode_prescite: '',
      methode_posee: false,
      effets_secondaires: '',
      notes: '',
      observation: '',
    })
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold">Consultations</h1>
          <p className="text-muted-foreground mt-2">
            Gestion des consultations de planification familiale
          </p>
        </div>
        <Dialog open={dialogOpen} onOpenChange={(open) => {
          setDialogOpen(open)
          if (!open) resetForm()
        }}>
          <DialogTrigger asChild>
            <Button onClick={() => resetForm()}>
              <Plus className="h-4 w-4 mr-2" />
              Nouvelle consultation
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>
                {editingConsultation ? 'Modifier la consultation' : 'Nouvelle consultation'}
              </DialogTitle>
              <DialogDescription>
                Remplissez les informations de la consultation
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="patient">Patient *</Label>
                  <select
                    id="patient"
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                    value={formData.patient}
                    onChange={(e) => setFormData({ ...formData, patient: e.target.value })}
                    required
                  >
                    <option value="">Sélectionner un patient</option>
                    {patients.map((p) => (
                      <option key={p.id} value={p.id}>
                        {p.nom} {p.prenom}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="date">Date et heure *</Label>
                  <Input
                    id="date"
                    type="datetime-local"
                    value={formData.date}
                    onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                    required
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="anamnese">Anamnèse</Label>
                <textarea
                  id="anamnese"
                  className="flex min-h-[100px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  value={formData.anamnese}
                  onChange={(e) => setFormData({ ...formData, anamnese: e.target.value })}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="examen">Examen clinique</Label>
                <textarea
                  id="examen"
                  className="flex min-h-[100px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  value={formData.examen}
                  onChange={(e) => setFormData({ ...formData, examen: e.target.value })}
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="methode_proposee">Méthode proposée</Label>
                  <select
                    id="methode_proposee"
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                    value={formData.methode_proposee}
                    onChange={(e) => setFormData({ ...formData, methode_proposee: e.target.value })}
                  >
                    <option value="">Aucune</option>
                    {methodes.map((m) => (
                      <option key={m.id} value={m.id}>
                        {m.nom}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="methode_prescite">Méthode prescrite</Label>
                  <select
                    id="methode_prescite"
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                    value={formData.methode_prescite}
                    onChange={(e) => setFormData({ ...formData, methode_prescite: e.target.value })}
                  >
                    <option value="">Aucune</option>
                    {methodes.map((m) => (
                      <option key={m.id} value={m.id}>
                        {m.nom}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="methode_posee" className="flex items-center gap-2">
                  <input
                    id="methode_posee"
                    type="checkbox"
                    checked={formData.methode_posee}
                    onChange={(e) => setFormData({ ...formData, methode_posee: e.target.checked })}
                    className="h-4 w-4"
                  />
                  Méthode posée
                </Label>
              </div>
              <div className="space-y-2">
                <Label htmlFor="effets_secondaires">Effets secondaires</Label>
                <textarea
                  id="effets_secondaires"
                  className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  value={formData.effets_secondaires}
                  onChange={(e) => setFormData({ ...formData, effets_secondaires: e.target.value })}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="notes">Notes</Label>
                <textarea
                  id="notes"
                  className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="observation">Observation</Label>
                <textarea
                  id="observation"
                  className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  value={formData.observation}
                  onChange={(e) => setFormData({ ...formData, observation: e.target.value })}
                />
              </div>
              <DialogFooter>
                <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>
                  Annuler
                </Button>
                <Button type="submit">Enregistrer</Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Search className="h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Rechercher une consultation..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="max-w-sm"
            />
          </div>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary"></div>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Date</TableHead>
                  <TableHead>Patient</TableHead>
                  <TableHead>Méthode prescrite</TableHead>
                  <TableHead>Méthode posée</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {consultations.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center text-muted-foreground">
                      Aucune consultation trouvée
                    </TableCell>
                  </TableRow>
                ) : (
                  consultations.map((consultation) => (
                    <TableRow key={consultation.id}>
                      <TableCell>
                        {consultation.date
                          ? format(new Date(consultation.date), 'dd/MM/yyyy HH:mm')
                          : '-'}
                      </TableCell>
                      <TableCell>
                        {consultation.patient?.nom} {consultation.patient?.prenom}
                      </TableCell>
                      <TableCell>
                        {consultation.methode_prescite?.nom || '-'}
                      </TableCell>
                      <TableCell>
                        {consultation.methode_posee ? 'Oui' : 'Non'}
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex justify-end gap-2">
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleEdit(consultation)}
                          >
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleDelete(consultation.id)}
                          >
                            <Trash2 className="h-4 w-4 text-destructive" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

