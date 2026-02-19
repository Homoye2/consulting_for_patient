import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { consultationsService, patientsService } from '../../services/apiService'
import { generateConsultationSlug, generateUrlWithSlug } from '../../lib/slugUtils'
import { Button } from '../../components/ui/button'
import { Input } from '../../components/ui/input'
import { Card, CardContent, CardHeader } from '../../components/ui/card'
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
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '../../components/ui/dialog'
import { Label } from '../../components/ui/label'
import { Plus, Search, Edit, Trash2, Eye } from 'lucide-react'
import { format } from 'date-fns'
import { Pagination } from '../../components/ui/pagination'

export const Consultations = () => {
  const navigate = useNavigate()
  const [consultations, setConsultations] = useState([])
  const [patients, setPatients] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editingConsultation, setEditingConsultation] = useState(null)
  
  // Pagination
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [totalItems, setTotalItems] = useState(0)
  const itemsPerPage = 15
  const [formData, setFormData] = useState({
    patient: '',
    date: new Date().toISOString().slice(0, 16),
    anamnese: '',
    examen: '',
    effets_secondaires: '',
    notes: '',
    observation: '',
  })

  useEffect(() => {
    fetchConsultations()
    fetchPatients()
  }, [searchTerm, currentPage])

  const fetchConsultations = async () => {
    try {
      setLoading(true)
      const params = {
        page: currentPage,
        page_size: itemsPerPage,
        ...(searchTerm && { search: searchTerm })
      }
      const response = await consultationsService.getAll(params)
      
      if (response.data.results) {
        // API avec pagination
        setConsultations(response.data.results)
        console.log("consultation :",response.data.results)
        setTotalItems(response.data.count || 0)
        setTotalPages(Math.ceil((response.data.count || 0) / itemsPerPage))
      } else {
        // API sans pagination - simuler la pagination côté client
        const allConsultations = Array.isArray(response.data) ? response.data : []
        const filteredConsultations = searchTerm 
          ? allConsultations.filter(c => 
              `${c.patient?.nom} ${c.patient?.prenom}`.toLowerCase().includes(searchTerm.toLowerCase())
            )
          : allConsultations
        
        setTotalItems(filteredConsultations.length)
        setTotalPages(Math.ceil(filteredConsultations.length / itemsPerPage))
        
        const startIndex = (currentPage - 1) * itemsPerPage
        const endIndex = startIndex + itemsPerPage
        setConsultations(filteredConsultations.slice(startIndex, endIndex))
      }
    } catch (error) {
      console.error('Erreur lors du chargement des consultations:', error)
      setConsultations([])
      setTotalItems(0)
      setTotalPages(1)
    } finally {
      setLoading(false)
    }
  }

  const handlePageChange = (page) => {
    setCurrentPage(page)
  }

  const handleSearchChange = (value) => {
    setSearchTerm(value)
    setCurrentPage(1) // Reset à la première page lors d'une recherche
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
              onChange={(e) => handleSearchChange(e.target.value)}
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
                  <TableHead>Specialiste</TableHead>
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
                        {consultation.patient_nom_complet}
                      </TableCell>
                      <TableCell>
                        {consultation.professionnel_nom}
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex justify-end gap-2">
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => {
                              const slug = generateConsultationSlug(
                                consultation.patient?.nom || '', 
                                consultation.patient?.prenom || '', 
                                consultation.date
                              )
                              const urlPath = generateUrlWithSlug(consultation.id, slug)
                              navigate(`/consultations/${urlPath}`)
                            }}
                            title="Voir les détails"
                          >
                            <Eye className="h-4 w-4" />
                          </Button>
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
          
          {!loading && totalPages > 1 && (
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              totalItems={totalItems}
              itemsPerPage={itemsPerPage}
              onPageChange={handlePageChange}
            />
          )}
        </CardContent>
      </Card>
    </div>
  )
}

