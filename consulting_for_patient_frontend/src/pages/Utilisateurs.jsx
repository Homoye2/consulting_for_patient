import { useState, useEffect } from 'react'
import { usersService } from '../services/apiService'
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
import { Plus, Search, Edit, Trash2, UserCheck, UserX } from 'lucide-react'
import { format } from 'date-fns'

const ROLE_LABELS = {
  administrateur: 'Administrateur',
  medecin: 'Médecin',
  sage_femme: 'Sage-femme',
  infirmier: 'Infirmier(ère)',
  pharmacien: 'Pharmacien',
  agent_enregistrement: 'Agent d\'enregistrement',
}

export const Utilisateurs = () => {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editingUser, setEditingUser] = useState(null)
  const [formData, setFormData] = useState({
    nom: '',
    email: '',
    password: '',
    password_confirm: '',
    role: 'medecin',
    actif: true,
  })

  useEffect(() => {
    fetchUsers()
  }, [searchTerm])

  const fetchUsers = async () => {
    try {
      setLoading(true)
      const params = searchTerm ? { search: searchTerm } : {}
      const response = await usersService.getAll(params)
      setUsers(response.data.results || response.data)
    } catch (error) {
      console.error('Erreur lors du chargement des utilisateurs:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (formData.password && formData.password !== formData.password_confirm) {
      alert('Les mots de passe ne correspondent pas')
      return
    }
    try {
      const data = { ...formData }
      if (!editingUser || !formData.password) {
        delete data.password
        delete data.password_confirm
      }
      if (editingUser) {
        await usersService.update(editingUser.id, data)
      } else {
        await usersService.create(data)
      }
      setDialogOpen(false)
      resetForm()
      fetchUsers()
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error)
      alert('Erreur lors de la sauvegarde')
    }
  }

  const handleEdit = (user) => {
    setEditingUser(user)
    setFormData({
      nom: user.nom || '',
      email: user.email || '',
      password: '',
      password_confirm: '',
      role: user.role || 'medecin',
      actif: user.actif !== false,
    })
    setDialogOpen(true)
  }

  const handleDelete = async (id) => {
    if (confirm('Êtes-vous sûr de vouloir supprimer cet utilisateur ?')) {
      try {
        await usersService.delete(id)
        fetchUsers()
      } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        alert('Erreur lors de la suppression')
      }
    }
  }

  const handleToggleActif = async (user) => {
    try {
      if (user.actif) {
        await usersService.deactivate(user.id)
      } else {
        await usersService.activate(user.id)
      }
      fetchUsers()
    } catch (error) {
      console.error('Erreur lors du changement de statut:', error)
      alert('Erreur lors du changement de statut')
    }
  }

  const resetForm = () => {
    setEditingUser(null)
    setFormData({
      nom: '',
      email: '',
      password: '',
      password_confirm: '',
      role: 'medecin',
      actif: true,
    })
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold">Utilisateurs</h1>
          <p className="text-muted-foreground mt-2">
            Gestion des utilisateurs du système
          </p>
        </div>
        <Dialog open={dialogOpen} onOpenChange={(open) => {
          setDialogOpen(open)
          if (!open) resetForm()
        }}>
          <DialogTrigger asChild>
            <Button onClick={() => resetForm()}>
              <Plus className="h-4 w-4 mr-2" />
              Nouvel utilisateur
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>
                {editingUser ? 'Modifier l\'utilisateur' : 'Nouvel utilisateur'}
              </DialogTitle>
              <DialogDescription>
                Remplissez les informations de l'utilisateur
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
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
                <Label htmlFor="email">Email *</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="password">
                    {editingUser ? 'Nouveau mot de passe' : 'Mot de passe *'}
                  </Label>
                  <Input
                    id="password"
                    type="password"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    required={!editingUser}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="password_confirm">
                    {editingUser ? 'Confirmer le nouveau mot de passe' : 'Confirmer le mot de passe *'}
                  </Label>
                  <Input
                    id="password_confirm"
                    type="password"
                    value={formData.password_confirm}
                    onChange={(e) => setFormData({ ...formData, password_confirm: e.target.value })}
                    required={!editingUser}
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="role">Rôle *</Label>
                  <select
                    id="role"
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                    value={formData.role}
                    onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                    required
                  >
                    {Object.entries(ROLE_LABELS).map(([value, label]) => (
                      <option key={value} value={value}>
                        {label}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="actif" className="flex items-center gap-2">
                    <input
                      id="actif"
                      type="checkbox"
                      checked={formData.actif}
                      onChange={(e) => setFormData({ ...formData, actif: e.target.checked })}
                      className="h-4 w-4"
                    />
                    Actif
                  </Label>
                </div>
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
              placeholder="Rechercher un utilisateur..."
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
                  <TableHead>Email</TableHead>
                  <TableHead>Rôle</TableHead>
                  <TableHead>Statut</TableHead>
                  <TableHead>Date d'inscription</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {users.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center text-muted-foreground">
                      Aucun utilisateur trouvé
                    </TableCell>
                  </TableRow>
                ) : (
                  users.map((user) => (
                    <TableRow key={user.id}>
                      <TableCell className="font-medium">{user.nom}</TableCell>
                      <TableCell>{user.email}</TableCell>
                      <TableCell>{ROLE_LABELS[user.role] || user.role}</TableCell>
                      <TableCell>
                        {user.actif ? (
                          <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-500/20 text-green-500">
                            Actif
                          </span>
                        ) : (
                          <span className="px-2 py-1 rounded-full text-xs font-medium bg-gray-500/20 text-gray-500">
                            Inactif
                          </span>
                        )}
                      </TableCell>
                      <TableCell>
                        {user.date_joined
                          ? format(new Date(user.date_joined), 'dd/MM/yyyy')
                          : '-'}
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex justify-end gap-2">
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleToggleActif(user)}
                            title={user.actif ? 'Désactiver' : 'Activer'}
                          >
                            {user.actif ? (
                              <UserX className="h-4 w-4" />
                            ) : (
                              <UserCheck className="h-4 w-4" />
                            )}
                          </Button>
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleEdit(user)}
                          >
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleDelete(user.id)}
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

