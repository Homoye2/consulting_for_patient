import { useState, useEffect } from 'react'
import { patientsService } from '../services/apiService'
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

export const Patients = () => {
  const [patients, setPatients] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editingPatient, setEditingPatient] = useState(null)
  const [formData, setFormData] = useState({
    nom: '',
    prenom: '',
    dob: '',
    sexe: 'F',
    telephone: '',
    adresse: '',
    antecedents: '',
    allergies: '',
  })

  useEffect(() => {
    fetchPatients()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchTerm])

  const fetchPatients = async () => {
    try {
      setLoading(true)
      const params = searchTerm ? { search: searchTerm } : {}
      const response = await patientsService.getAll(params)
      setPatients(response.data.results || response.data)
    } catch (error) {
      console.error('Erreur lors du chargement des patients:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editingPatient) {
        await patientsService.update(editingPatient.id, formData)
      } else {
        await patientsService.create(formData)
      }
      setDialogOpen(false)
      resetForm()
      fetchPatients()
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error)
      alert('Erreur lors de la sauvegarde')
    }
  }

  const handleEdit = (patient) => {
    setEditingPatient(patient)
    setFormData({
      nom: patient.nom || '',
      prenom: patient.prenom || '',
      dob: patient.dob || '',
      sexe: patient.sexe || 'F',
      telephone: patient.telephone || '',
      adresse: patient.adresse || '',
      antecedents: patient.antecedents || '',
      allergies: patient.allergies || '',
    })
    setDialogOpen(true)
  }

  const handleDelete = async (id) => {
    if (confirm('Êtes-vous sûr de vouloir supprimer ce patient ?')) {
      try {
        await patientsService.delete(id)
        fetchPatients()
      } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        alert('Erreur lors de la suppression')
      }
    }
  }

  const resetForm = () => {
    setEditingPatient(null)
    setFormData({
      nom: '',
      prenom: '',
      dob: '',
      sexe: 'F',
      telephone: '',
      adresse: '',
      antecedents: '',
      allergies: '',
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

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold">Patients</h1>
          <p className="text-muted-foreground mt-2">
            Gestion des patients
          </p>
        </div>
        <Dialog open={dialogOpen} onOpenChange={(open) => {
          setDialogOpen(open)
          if (!open) resetForm()
        }}>
          <DialogTrigger asChild>
            <Button onClick={() => resetForm()}>
              <Plus className="h-4 w-4 mr-2" />
              Nouveau patient
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>
                {editingPatient ? 'Modifier le patient' : 'Nouveau patient'}
              </DialogTitle>
              <DialogDescription>
                Remplissez les informations du patient
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="nom">Nom *</Label>
                  <Input
                    id="nom"
                    value={formData.nom}
                    onChange={(e) => setFormData({ ...formData, nom: e.target.value })}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="prenom">Prénom *</Label>
                  <Input
                    id="prenom"
                    value={formData.prenom}
                    onChange={(e) => setFormData({ ...formData, prenom: e.target.value })}
                    required
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="dob">Date de naissance *</Label>
                  <Input
                    id="dob"
                    type="date"
                    value={formData.dob}
                    onChange={(e) => setFormData({ ...formData, dob: e.target.value })}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="sexe">Sexe *</Label>
                  <select
                    id="sexe"
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                    value={formData.sexe}
                    onChange={(e) => setFormData({ ...formData, sexe: e.target.value })}
                    required
                  >
                    <option value="F">Féminin</option>
                    <option value="M">Masculin</option>
                  </select>
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="telephone">Téléphone</Label>
                <Input
                  id="telephone"
                  value={formData.telephone}
                  onChange={(e) => setFormData({ ...formData, telephone: e.target.value })}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="adresse">Adresse</Label>
                <Input
                  id="adresse"
                  value={formData.adresse}
                  onChange={(e) => setFormData({ ...formData, adresse: e.target.value })}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="antecedents">Antécédents</Label>
                <textarea
                  id="antecedents"
                  className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  value={formData.antecedents}
                  onChange={(e) => setFormData({ ...formData, antecedents: e.target.value })}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="allergies">Allergies</Label>
                <textarea
                  id="allergies"
                  className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  value={formData.allergies}
                  onChange={(e) => setFormData({ ...formData, allergies: e.target.value })}
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
              placeholder="Rechercher un patient..."
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
                  <TableHead>Nom</TableHead>
                  <TableHead>Prénom</TableHead>
                  <TableHead>Date de naissance</TableHead>
                  <TableHead>Âge</TableHead>
                  <TableHead>Sexe</TableHead>
                  <TableHead>Téléphone</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {patients.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={7} className="text-center text-muted-foreground">
                      Aucun patient trouvé
                    </TableCell>
                  </TableRow>
                ) : (
                  patients.map((patient) => (
                    <TableRow key={patient.id}>
                      <TableCell className="font-medium">{patient.nom}</TableCell>
                      <TableCell>{patient.prenom}</TableCell>
                      <TableCell>
                        {patient.dob
                          ? format(new Date(patient.dob), 'dd/MM/yyyy')
                          : '-'}
                      </TableCell>
                      <TableCell>{calculateAge(patient.dob)} ans</TableCell>
                      <TableCell>{patient.sexe === 'F' ? 'Féminin' : 'Masculin'}</TableCell>
                      <TableCell>{patient.telephone || '-'}</TableCell>
                      <TableCell className="text-right">
                        <div className="flex justify-end gap-2">
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleEdit(patient)}
                          >
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleDelete(patient.id)}
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

