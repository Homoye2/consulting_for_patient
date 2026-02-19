import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card'
import { Button } from '../../ui/button'
import { Input } from '../../ui/input'
import { Badge } from '../../ui/badge'
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '../../ui/table'
import { 
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '../../ui/dialog'
import { 
  Users, 
  UserPlus, 
  Search, 
  Filter, 
  MoreHorizontal,
  Edit,
  Trash2,
  Shield,
  ShieldCheck,
  ShieldX,
  Eye
} from 'lucide-react'
import { usersService } from '../../../services/apiService'
import { AnimatedContainer } from '../../ui/animated-page'
import { format } from 'date-fns'
import { fr } from 'date-fns/locale'

const UserRoleBadge = ({ role }) => {
  const getRoleConfig = (role) => {
    switch (role) {
      case 'super_admin':
        return { label: 'Super Admin', variant: 'destructive' }
      case 'admin_hopital':
        return { label: 'Admin Hôpital', variant: 'default' }
      case 'specialiste':
        return { label: 'Spécialiste', variant: 'secondary' }
      case 'pharmacien':
        return { label: 'Pharmacien', variant: 'outline' }
      case 'agent_enregistrement':
        return { label: 'Agent', variant: 'secondary' }
      default:
        return { label: role, variant: 'outline' }
    }
  }

  const config = getRoleConfig(role)
  return <Badge variant={config.variant}>{config.label}</Badge>
}

const UserStatusBadge = ({ isActive }) => {
  return (
    <Badge variant={isActive ? 'default' : 'secondary'}>
      {isActive ? 'Actif' : 'Inactif'}
    </Badge>
  )
}

export const UserManagement = () => {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedRole, setSelectedRole] = useState('')
  const [selectedUser, setSelectedUser] = useState(null)
  const [showUserDialog, setShowUserDialog] = useState(false)

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    try {
      setLoading(true)
      const response = await usersService.getAll()
      const usersData = Array.isArray(response.data) ? response.data : (response.data?.results || [])
      setUsers(usersData)
    } catch (error) {
      console.error('Erreur lors du chargement des utilisateurs:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleActivateUser = async (userId) => {
    try {
      await usersService.activate(userId)
      await fetchUsers()
    } catch (error) {
      console.error('Erreur lors de l\'activation:', error)
    }
  }

  const handleDeactivateUser = async (userId) => {
    try {
      await usersService.deactivate(userId)
      await fetchUsers()
    } catch (error) {
      console.error('Erreur lors de la désactivation:', error)
    }
  }

  const handleDeleteUser = async (userId) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cet utilisateur ?')) return
    
    try {
      await usersService.delete(userId)
      await fetchUsers()
    } catch (error) {
      console.error('Erreur lors de la suppression:', error)
    }
  }

  const filteredUsers = users.filter(user => {
    const matchesSearch = user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.first_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.last_name?.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesRole = !selectedRole || user.role === selectedRole
    return matchesSearch && matchesRole
  })

  const userStats = {
    total: users.length,
    active: users.filter(u => u.is_active).length,
    inactive: users.filter(u => !u.is_active).length,
    byRole: users.reduce((acc, user) => {
      acc[user.role] = (acc[user.role] || 0) + 1
      return acc
    }, {})
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Chargement des utilisateurs...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4 sm:space-y-6">
      {/* Statistiques utilisateurs */}
      <AnimatedContainer>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-xs sm:text-sm font-medium truncate pr-2">Total Utilisateurs</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground flex-shrink-0" />
            </CardHeader>
            <CardContent className="pt-0">
              <div className="text-xl sm:text-2xl font-bold">{userStats.total}</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-xs sm:text-sm font-medium truncate pr-2">Utilisateurs Actifs</CardTitle>
              <ShieldCheck className="h-4 w-4 text-green-600 flex-shrink-0" />
            </CardHeader>
            <CardContent className="pt-0">
              <div className="text-xl sm:text-2xl font-bold text-green-600">{userStats.active}</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-xs sm:text-sm font-medium truncate pr-2">Utilisateurs Inactifs</CardTitle>
              <ShieldX className="h-4 w-4 text-red-600 flex-shrink-0" />
            </CardHeader>
            <CardContent className="pt-0">
              <div className="text-xl sm:text-2xl font-bold text-red-600">{userStats.inactive}</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-xs sm:text-sm font-medium truncate pr-2">Super Admins</CardTitle>
              <Shield className="h-4 w-4 text-purple-600 flex-shrink-0" />
            </CardHeader>
            <CardContent className="pt-0">
              <div className="text-xl sm:text-2xl font-bold text-purple-600">
                {userStats.byRole.super_admin || 0}
              </div>
            </CardContent>
          </Card>
        </div>
      </AnimatedContainer>

      {/* Gestion des utilisateurs */}
      <AnimatedContainer>
        <Card>
          <CardHeader className="pb-3 sm:pb-6">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div>
                <CardTitle className="text-lg sm:text-xl">Gestion des Utilisateurs</CardTitle>
                <CardDescription className="text-sm">
                  Gérer tous les utilisateurs du système
                </CardDescription>
              </div>
              <Button className="w-full sm:w-auto">
                <UserPlus className="h-4 w-4 mr-2" />
                Nouvel Utilisateur
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {/* Filtres */}
            <div className="flex flex-col sm:flex-row items-stretch sm:items-center space-y-3 sm:space-y-0 sm:space-x-4 mb-4 sm:mb-6">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Rechercher par email, nom..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              <select
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
                className="px-3 py-2 border border-border rounded-md bg-background text-sm w-full sm:w-auto"
              >
                <option value="">Tous les rôles</option>
                <option value="super_admin">Super Admin</option>
                <option value="admin_hopital">Admin Hôpital</option>
                <option value="specialiste">Spécialiste</option>
                <option value="pharmacien">Pharmacien</option>
                <option value="agent_enregistrement">Agent</option>
              </select>
            </div>

            {/* Tableau des utilisateurs - Desktop */}
            <div className="hidden md:block rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Utilisateur</TableHead>
                    <TableHead>Rôle</TableHead>
                    <TableHead>Statut</TableHead>
                    <TableHead>Dernière connexion</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredUsers.map((user) => (
                    <TableRow key={user.id}>
                      <TableCell>
                        <div>
                          <div className="font-medium">
                            {user.first_name} {user.last_name}
                          </div>
                          <div className="text-sm text-muted-foreground">
                            {user.email}
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <UserRoleBadge role={user.role} />
                      </TableCell>
                      <TableCell>
                        <UserStatusBadge isActive={user.is_active} />
                      </TableCell>
                      <TableCell>
                        {user.last_login ? (
                          (() => {
                            try {
                              const date = new Date(user.last_login)
                              if (isNaN(date.getTime())) return 'Date invalide'
                              return format(date, 'dd MMM yyyy', { locale: fr })
                            } catch (error) {
                              console.warn('Erreur de formatage de date:', user.last_login, error)
                              return 'Date invalide'
                            }
                          })()
                        ) : (
                          'Jamais'
                        )}
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center space-x-2">
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => {
                              setSelectedUser(user)
                              setShowUserDialog(true)
                            }}
                          >
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => user.is_active ? 
                              handleDeactivateUser(user.id) : 
                              handleActivateUser(user.id)
                            }
                          >
                            {user.is_active ? <ShieldX className="h-4 w-4" /> : <ShieldCheck className="h-4 w-4" />}
                          </Button>
                          <Button
                            size="sm"
                            variant="destructive"
                            onClick={() => handleDeleteUser(user.id)}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>

            {/* Cards des utilisateurs - Mobile */}
            <div className="md:hidden space-y-3">
              {filteredUsers.map((user) => (
                <Card key={user.id} className="p-4">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex-1 min-w-0">
                      <h3 className="font-medium truncate">
                        {user.first_name} {user.last_name}
                      </h3>
                      <p className="text-sm text-muted-foreground truncate">
                        {user.email}
                      </p>
                    </div>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => {
                        setSelectedUser(user)
                        setShowUserDialog(true)
                      }}
                    >
                      <Eye className="h-4 w-4" />
                    </Button>
                  </div>
                  
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-2">
                      <UserRoleBadge role={user.role} />
                      <UserStatusBadge isActive={user.is_active} />
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <p className="text-xs text-muted-foreground">
                      Dernière connexion: {user.last_login ? (
                        (() => {
                          try {
                            const date = new Date(user.last_login)
                            if (isNaN(date.getTime())) return 'Date invalide'
                            return format(date, 'dd MMM yyyy', { locale: fr })
                          } catch (error) {
                            console.warn('Erreur de formatage de date:', user.last_login, error)
                            return 'Date invalide'
                          }
                        })()
                      ) : 'Jamais'}
                    </p>
                    
                    <div className="flex items-center space-x-1">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => user.is_active ? 
                          handleDeactivateUser(user.id) : 
                          handleActivateUser(user.id)
                        }
                      >
                        {user.is_active ? <ShieldX className="h-3 w-3" /> : <ShieldCheck className="h-3 w-3" />}
                      </Button>
                      <Button
                        size="sm"
                        variant="destructive"
                        onClick={() => handleDeleteUser(user.id)}
                      >
                        <Trash2 className="h-3 w-3" />
                      </Button>
                    </div>
                  </div>
                </Card>
              ))}
            </div>

            {filteredUsers.length === 0 && (
              <div className="text-center py-8">
                <Users className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground">Aucun utilisateur trouvé</p>
              </div>
            )}
          </CardContent>
        </Card>
      </AnimatedContainer>

      {/* Dialog détails utilisateur */}
      <Dialog open={showUserDialog} onOpenChange={setShowUserDialog}>
        <DialogContent className="max-w-md sm:max-w-lg">
          <DialogHeader>
            <DialogTitle className="text-lg sm:text-xl">Détails de l'utilisateur</DialogTitle>
            <DialogDescription className="text-sm">
              Informations complètes sur l'utilisateur sélectionné
            </DialogDescription>
          </DialogHeader>
          {selectedUser && (
            <div className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">Nom complet</label>
                  <p className="text-sm text-muted-foreground">
                    {selectedUser.first_name} {selectedUser.last_name}
                  </p>
                </div>
                <div>
                  <label className="text-sm font-medium">Email</label>
                  <p className="text-sm text-muted-foreground break-all">{selectedUser.email}</p>
                </div>
                <div>
                  <label className="text-sm font-medium">Rôle</label>
                  <div className="mt-1">
                    <UserRoleBadge role={selectedUser.role} />
                  </div>
                </div>
                <div>
                  <label className="text-sm font-medium">Statut</label>
                  <div className="mt-1">
                    <UserStatusBadge isActive={selectedUser.is_active} />
                  </div>
                </div>
                <div className="sm:col-span-2">
                  <label className="text-sm font-medium">Date de création</label>
                  <p className="text-sm text-muted-foreground">
                    {(() => {
                      try {
                        if (!selectedUser.date_joined) return 'Date inconnue'
                        const date = new Date(selectedUser.date_joined)
                        if (isNaN(date.getTime())) return 'Date invalide'
                        return format(date, 'dd MMM yyyy à HH:mm', { locale: fr })
                      } catch (error) {
                        console.warn('Erreur de formatage de date:', selectedUser.date_joined, error)
                        return 'Date invalide'
                      }
                    })()}
                  </p>
                </div>
                <div className="sm:col-span-2">
                  <label className="text-sm font-medium">Dernière connexion</label>
                  <p className="text-sm text-muted-foreground">
                    {selectedUser.last_login ? 
                      (() => {
                        try {
                          const date = new Date(selectedUser.last_login)
                          if (isNaN(date.getTime())) return 'Date invalide'
                          return format(date, 'dd MMM yyyy à HH:mm', { locale: fr })
                        } catch (error) {
                          console.warn('Erreur de formatage de date:', selectedUser.last_login, error)
                          return 'Date invalide'
                        }
                      })() : 
                      'Jamais'
                    }
                  </p>
                </div>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  )
}