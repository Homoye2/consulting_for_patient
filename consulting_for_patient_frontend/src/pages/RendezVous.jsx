import { useState, useEffect } from 'react'
import { rendezVousService, patientsService } from '../services/apiService'
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
import { Plus, Search, Edit, Trash2, Check, X } from 'lucide-react'
import { format } from 'date-fns'

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

export const RendezVous = () => {
  const [rendezVous, setRendezVous] = useState([])
  const [patients, setPatients] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editingRendezVous, setEditingRendezVous] = useState(null)
  const [formData, setFormData] = useState({
    patient: '',
    datetime: new Date().toISOString().slice(0, 16),
    statut: 'planifie',
    notes: '',
  })

  useEffect(() => {
    fetchRendezVous()
    fetchPatients()
  }, [searchTerm])

  const fetchRendezVous = async () => {
    try {
      setLoading(true)
      const params = searchTerm ? { search: searchTerm } : {}
      const response = await rendezVousService.getAll(params)
      setRendezVous(response.data.results || response.data)
    } catch (error) {
      console.error('Erreur lors du chargement des rendez-vous:', error)
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

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const data = {
        ...formData,
        patient: parseInt(formData.patient),
        datetime: new Date(formData.datetime).toISOString(),
      }
      if (editingRendezVous) {
        await rendezVousService.update(editingRendezVous.id, data)
      } else {
        await rendezVousService.create(data)
      }
      setDialogOpen(false)
      resetForm()
      fetchRendezVous()
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error)
      alert('Erreur lors de la sauvegarde')
    }
  }

  const handleEdit = (rdv) => {
    setEditingRendezVous(rdv)
    setFormData({
      patient: rdv.patient?.id || rdv.patient || '',
      datetime: rdv.datetime ? rdv.datetime.slice(0, 16) : new Date().toISOString().slice(0, 16),
      statut: rdv.statut || 'planifie',
      notes: rdv.notes || '',
    })
    setDialogOpen(true)
  }

  const handleDelete = async (id) => {
    if (confirm('Êtes-vous sûr de vouloir supprimer ce rendez-vous ?')) {
      try {
        await rendezVousService.delete(id)
        fetchRendezVous()
      } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        alert('Erreur lors de la suppression')
      }
    }
  }

  const handleConfirmer = async (id) => {
    try {
      await rendezVousService.confirmer(id)
      fetchRendezVous()
    } catch (error) {
      console.error('Erreur lors de la confirmation:', error)
      alert('Erreur lors de la confirmation')
    }
  }

  const handleAnnuler = async (id) => {
    try {
      await rendezVousService.annuler(id)
      fetchRendezVous()
    } catch (error) {
      console.error('Erreur lors de l\'annulation:', error)
      alert('Erreur lors de l\'annulation')
    }
  }

  const resetForm = () => {
    setEditingRendezVous(null)
    setFormData({
      patient: '',
      datetime: new Date().toISOString().slice(0, 16),
      statut: 'planifie',
      notes: '',
    })
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold">Rendez-vous</h1>
          <p className="text-muted-foreground mt-2">
            Gestion des rendez-vous
          </p>
        </div>
        <Dialog open={dialogOpen} onOpenChange={(open) => {
          setDialogOpen(open)
          if (!open) resetForm()
        }}>
          <DialogTrigger asChild>
            <Button onClick={() => resetForm()}>
              <Plus className="h-4 w-4 mr-2" />
              Nouveau rendez-vous
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>
                {editingRendezVous ? 'Modifier le rendez-vous' : 'Nouveau rendez-vous'}
              </DialogTitle>
              <DialogDescription>
                Remplissez les informations du rendez-vous
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
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
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="datetime">Date et heure *</Label>
                  <Input
                    id="datetime"
                    type="datetime-local"
                    value={formData.datetime}
                    onChange={(e) => setFormData({ ...formData, datetime: e.target.value })}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="statut">Statut *</Label>
                  <select
                    id="statut"
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                    value={formData.statut}
                    onChange={(e) => setFormData({ ...formData, statut: e.target.value })}
                    required
                  >
                    {Object.entries(STATUT_LABELS).map(([value, label]) => (
                      <option key={value} value={value}>
                        {label}
                      </option>
                    ))}
                  </select>
                </div>
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
              placeholder="Rechercher un rendez-vous..."
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
                  <TableHead>Date et heure</TableHead>
                  <TableHead>Patient</TableHead>
                  <TableHead>Statut</TableHead>
                  <TableHead>Notes</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {rendezVous.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center text-muted-foreground">
                      Aucun rendez-vous trouvé
                    </TableCell>
                  </TableRow>
                ) : (
                  rendezVous.map((rdv) => (
                    <TableRow key={rdv.id}>
                      <TableCell>
                        {rdv.datetime
                          ? format(new Date(rdv.datetime), 'dd/MM/yyyy HH:mm')
                          : '-'}
                      </TableCell>
                      <TableCell>
                        {rdv.patient?.nom} {rdv.patient?.prenom}
                      </TableCell>
                      <TableCell>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${STATUT_COLORS[rdv.statut] || ''}`}>
                          {STATUT_LABELS[rdv.statut] || rdv.statut}
                        </span>
                      </TableCell>
                      <TableCell className="max-w-xs truncate">
                        {rdv.notes || '-'}
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex justify-end gap-2">
                          {rdv.statut === 'planifie' && (
                            <>
                              <Button
                                variant="ghost"
                                size="icon"
                                onClick={() => handleConfirmer(rdv.id)}
                                title="Confirmer"
                              >
                                <Check className="h-4 w-4 text-green-500" />
                              </Button>
                              <Button
                                variant="ghost"
                                size="icon"
                                onClick={() => handleAnnuler(rdv.id)}
                                title="Annuler"
                              >
                                <X className="h-4 w-4 text-red-500" />
                              </Button>
                            </>
                          )}
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleEdit(rdv)}
                          >
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleDelete(rdv.id)}
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

