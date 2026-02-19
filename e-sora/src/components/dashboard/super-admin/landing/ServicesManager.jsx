import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card'
import { Button } from '../../ui/button'
import { Input } from '../../ui/input'
import { Label } from '../../ui/label'
import { Textarea } from '../../ui/textarea'
import { 
  Save, 
  RefreshCw, 
  Grid3X3, 
  Plus, 
  Edit, 
  Trash2,
  Heart
} from 'lucide-react'
import { 
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '../../ui/dialog'
import { landingPageService, landingServicesService } from '../../../services/apiService'
import * as LucideIcons from 'lucide-react'

export const ServicesManager = ({ landingData, services, onUpdate }) => {
  const [sectionData, setSectionData] = useState({
    services_title: landingData?.services_title || '',
    services_subtitle: landingData?.services_subtitle || ''
  })
  const [editingService, setEditingService] = useState(null)
  const [showServiceDialog, setShowServiceDialog] = useState(false)
  const [saving, setSaving] = useState(false)

  const handleSectionSave = async () => {
    try {
      setSaving(true)
      await landingPageService.partialUpdate(sectionData)
      await onUpdate()
      alert('Titre de section mis à jour avec succès !')
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error)
      alert('Erreur lors de la sauvegarde')
    } finally {
      setSaving(false)
    }
  }

  const handleServiceSave = async (serviceData) => {
    try {
      setSaving(true)
      if (editingService?.id) {
        await landingServicesService.update(editingService.id, serviceData)
      } else {
        await landingServicesService.create({
          ...serviceData,
          ordre: services.length + 1,
          landing_page: 1
        })
      }
      await onUpdate()
      setShowServiceDialog(false)
      setEditingService(null)
      alert('Service sauvegardé avec succès !')
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error)
      alert('Erreur lors de la sauvegarde')
    } finally {
      setSaving(false)
    }
  }

  const handleServiceDelete = async (serviceId) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce service ?')) return
    
    try {
      await landingServicesService.delete(serviceId)
      await onUpdate()
      alert('Service supprimé avec succès !')
    } catch (error) {
      console.error('Erreur lors de la suppression:', error)
      alert('Erreur lors de la suppression')
    }
  }

  const getIcon = (iconName) => {
    const IconComponent = LucideIcons[iconName] || LucideIcons.Heart
    return IconComponent
  }

  return (
    <div className="space-y-6">
      {/* Configuration de la section */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Grid3X3 className="h-5 w-5 text-green-600" />
            Configuration de la Section Services
          </CardTitle>
          <CardDescription>
            Modifier le titre et sous-titre de la section services
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Label htmlFor="services_title">Titre de la Section</Label>
            <Input
              id="services_title"
              value={sectionData.services_title}
              onChange={(e) => setSectionData(prev => ({ ...prev, services_title: e.target.value }))}
              placeholder="Nos Services"
            />
          </div>

          <div>
            <Label htmlFor="services_subtitle">Sous-titre</Label>
            <Input
              id="services_subtitle"
              value={sectionData.services_subtitle}
              onChange={(e) => setSectionData(prev => ({ ...prev, services_subtitle: e.target.value }))}
              placeholder="Description des services offerts"
            />
          </div>

          <Button onClick={handleSectionSave} disabled={saving}>
            {saving ? (
              <>
                <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                Sauvegarde...
              </>
            ) : (
              <>
                <Save className="mr-2 h-4 w-4" />
                Sauvegarder la Section
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Gestion des services */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Services ({services.length})</CardTitle>
              <CardDescription>
                Gérer la liste des services affichés
              </CardDescription>
            </div>
            <Dialog open={showServiceDialog} onOpenChange={setShowServiceDialog}>
              <DialogTrigger asChild>
                <Button 
                  onClick={() => {
                    setEditingService({ titre: '', description: '', icone: 'Heart' })
                    setShowServiceDialog(true)
                  }}
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Ajouter un Service
                </Button>
              </DialogTrigger>
              <ServiceDialog
                service={editingService}
                onSave={handleServiceSave}
                onCancel={() => {
                  setShowServiceDialog(false)
                  setEditingService(null)
                }}
                saving={saving}
              />
            </Dialog>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {services.map((service) => {
              const IconComponent = getIcon(service.icone)
              return (
                <div key={service.id} className="p-4 border rounded-lg space-y-3">
                  <div className="flex items-center gap-3">
                    <div className="bg-green-500/20 w-10 h-10 rounded-lg flex items-center justify-center">
                      <IconComponent className="h-5 w-5 text-green-600" />
                    </div>
                    <div className="flex-1">
                      <h4 className="font-medium">{service.titre}</h4>
                      <p className="text-sm text-muted-foreground line-clamp-2">
                        {service.description}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => {
                        setEditingService(service)
                        setShowServiceDialog(true)
                      }}
                    >
                      <Edit className="h-3 w-3 mr-1" />
                      Modifier
                    </Button>
                    <Button
                      size="sm"
                      variant="destructive"
                      onClick={() => handleServiceDelete(service.id)}
                    >
                      <Trash2 className="h-3 w-3 mr-1" />
                      Supprimer
                    </Button>
                  </div>
                </div>
              )
            })}
          </div>

          {services.length === 0 && (
            <div className="text-center py-8 text-muted-foreground">
              <Grid3X3 className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>Aucun service configuré</p>
              <p className="text-sm">Cliquez sur "Ajouter un Service" pour commencer</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

const ServiceDialog = ({ service, onSave, onCancel, saving }) => {
  const [formData, setFormData] = useState({
    titre: service?.titre || '',
    description: service?.description || '',
    icone: service?.icone || 'Heart'
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!formData.titre || !formData.description) {
      alert('Veuillez remplir tous les champs obligatoires')
      return
    }
    onSave(formData)
  }

  const iconOptions = [
    'Heart', 'Stethoscope', 'Shield', 'Users', 'Calendar', 'FileText',
    'Phone', 'Mail', 'MapPin', 'Clock', 'Award', 'Star'
  ]

  return (
    <DialogContent className="max-w-md">
      <DialogHeader>
        <DialogTitle>
          {service?.id ? 'Modifier le Service' : 'Ajouter un Service'}
        </DialogTitle>
        <DialogDescription>
          Remplissez les informations du service
        </DialogDescription>
      </DialogHeader>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <Label htmlFor="titre">Titre *</Label>
          <Input
            id="titre"
            value={formData.titre}
            onChange={(e) => setFormData(prev => ({ ...prev, titre: e.target.value }))}
            placeholder="Nom du service"
            required
          />
        </div>

        <div>
          <Label htmlFor="description">Description *</Label>
          <Textarea
            id="description"
            value={formData.description}
            onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
            placeholder="Description détaillée du service"
            rows={3}
            required
          />
        </div>

        <div>
          <Label htmlFor="icone">Icône</Label>
          <select
            id="icone"
            value={formData.icone}
            onChange={(e) => setFormData(prev => ({ ...prev, icone: e.target.value }))}
            className="w-full px-3 py-2 border border-border rounded-md bg-background"
          >
            {iconOptions.map(icon => (
              <option key={icon} value={icon}>{icon}</option>
            ))}
          </select>
        </div>

        <div className="flex gap-3 pt-4">
          <Button type="submit" disabled={saving}>
            {saving ? (
              <>
                <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                Sauvegarde...
              </>
            ) : (
              <>
                <Save className="mr-2 h-4 w-4" />
                Sauvegarder
              </>
            )}
          </Button>
          <Button type="button" variant="outline" onClick={onCancel}>
            Annuler
          </Button>
        </div>
      </form>
    </DialogContent>
  )
}