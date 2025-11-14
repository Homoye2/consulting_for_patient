import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card'
import { Button } from '../../components/ui/button'
import { Input } from '../../components/ui/input'
import { Label } from '../../components/ui/label'
import { Textarea } from '../../components/ui/textarea'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '../../components/ui/dialog'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../../components/ui/table'
import { Plus, Calendar, Clock, CheckCircle2, XCircle } from 'lucide-react'
import { rendezVousService, usersService } from '../../services/apiService'
import { format } from 'date-fns'

export const PatientRendezVous = () => {
  const [rendezVous, setRendezVous] = useState([])
  const [loading, setLoading] = useState(true)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [professionnels, setProfessionnels] = useState([])
  const [formData, setFormData] = useState({
    datetime: '',
    notes: '',
    user: '',
  })

  useEffect(() => {
    fetchData()
    fetchProfessionnels()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      // Les patients voient automatiquement leurs propres rendez-vous grâce au backend
      const response = await rendezVousService.getAll()
      const data = Array.isArray(response.data) ? response.data : (response.data?.results || [])
      setRendezVous(data)
    } catch (error) {
      console.error('Erreur lors du chargement des rendez-vous:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchProfessionnels = async () => {
    try {
      const response = await usersService.getAll({ role: 'medecin' })
      const data = Array.isArray(response.data) ? response.data : (response.data?.results || [])
      setProfessionnels(data)
    } catch (error) {
      console.error('Erreur lors du chargement des professionnels:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      // Récupérer l'ID du patient depuis le user
      const user = JSON.parse(localStorage.getItem('user'))
      const patientId = user?.patient_id
      
      if (!patientId) {
        alert('Erreur: Profil patient non trouvé')
        return
      }

      await rendezVousService.create({
        patient: patientId,
        user: formData.user,
        datetime: formData.datetime,
        notes: formData.notes,
        statut: 'en_attente',
      })
      alert('Rendez-vous demandé avec succès !')
      setDialogOpen(false)
      setFormData({ datetime: '', notes: '', user: '' })
      fetchData()
    } catch (error) {
      console.error('Erreur lors de la création du rendez-vous:', error)
      alert('Erreur lors de la création du rendez-vous')
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
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
        <div>
          <h1 className="text-3xl md:text-4xl font-bold mb-2">Mes rendez-vous</h1>
          <p className="text-muted-foreground">
            Gérez vos rendez-vous et prenez de nouveaux rendez-vous
          </p>
        </div>
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Prendre un rendez-vous
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[500px]">
            <DialogHeader>
              <DialogTitle>Nouveau rendez-vous</DialogTitle>
              <DialogDescription>
                Remplissez le formulaire pour demander un rendez-vous
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleSubmit}>
              <div className="space-y-4 py-4">
                <div>
                  <Label htmlFor="user">Professionnel de santé</Label>
                  <select
                    id="user"
                    value={formData.user}
                    onChange={(e) => setFormData({ ...formData, user: e.target.value })}
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    required
                  >
                    <option value="">Sélectionner un professionnel</option>
                    {professionnels.map((prof) => (
                      <option key={prof.id} value={prof.id}>
                        {prof.nom} - {prof.role}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <Label htmlFor="datetime">Date et heure</Label>
                  <Input
                    id="datetime"
                    type="datetime-local"
                    value={formData.datetime}
                    onChange={(e) => setFormData({ ...formData, datetime: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="notes">Notes (optionnel)</Label>
                  <Textarea
                    id="notes"
                    value={formData.notes}
                    onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                    rows={3}
                    placeholder="Informations supplémentaires..."
                  />
                </div>
              </div>
              <DialogFooter>
                <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>
                  Annuler
                </Button>
                <Button type="submit">Demander le rendez-vous</Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Liste des rendez-vous</CardTitle>
          <CardDescription>Tous vos rendez-vous passés et à venir</CardDescription>
        </CardHeader>
        <CardContent>
          {rendezVous.length > 0 ? (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Date et heure</TableHead>
                    <TableHead>Professionnel</TableHead>
                    <TableHead>Statut</TableHead>
                    <TableHead>Notes</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {rendezVous.map((rdv) => {
                    const badge = getStatutBadge(rdv.statut)
                    const BadgeIcon = badge.icon
                    return (
                      <TableRow key={rdv.id}>
                        <TableCell>
                          {format(new Date(rdv.datetime), "dd MMMM yyyy 'à' HH:mm")}
                        </TableCell>
                        <TableCell>{rdv.professionnel_nom}</TableCell>
                        <TableCell>
                          <div className={`flex items-center gap-1 px-2 py-1 rounded-full text-xs w-fit ${badge.className}`}>
                            <BadgeIcon className="h-3 w-3" />
                            <span>{badge.label}</span>
                          </div>
                        </TableCell>
                        <TableCell className="max-w-xs truncate">{rdv.notes || '-'}</TableCell>
                      </TableRow>
                    )
                  })}
                </TableBody>
              </Table>
            </div>
          ) : (
            <div className="text-center py-8">
              <Calendar className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">Aucun rendez-vous pour le moment</p>
              <Button className="mt-4" onClick={() => setDialogOpen(true)}>
                <Plus className="h-4 w-4 mr-2" />
                Prendre un rendez-vous
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

