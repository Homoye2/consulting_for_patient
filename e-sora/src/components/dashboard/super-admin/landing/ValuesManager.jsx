import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card'
import { Button } from '../../ui/button'
import { Input } from '../../ui/input'
import { Label } from '../../ui/label'
import { Textarea } from '../../ui/textarea'
import { 
  Save, 
  RefreshCw, 
  Award, 
  Plus, 
  Edit, 
  Trash2,
  Shield
} from 'lucide-react'
import { 
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '../../ui/dialog'
import { landingPageService, landingValuesService } from '../../../services/apiService'
import * as LucideIcons from 'lucide-react'

export const ValuesManager = ({ landingData, values, onUpdate }) => {
  const [sectionData, setSectionData] = useState({
    values_title: landingData?.values_title || '',
    values_subtitle: landingData?.values_subtitle || ''
  })
  const [editingValue, setEditingValue] = useState(null)
  const [showValueDialog, setShowValueDialog] = useState(false)
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

  const handleValueSave = async (valueData) => {
    try {
      setSaving(true)
      if (editingValue?.id) {
        await landingValuesService.update(editingValue.id, valueData)
      } else {
        await landingValuesService.create({
          ...valueData,
          ordre: values.length + 1,
          landing_page: 1
        })
      }
      await onUpdate()
      setShowValueDialog(false)
      setEditingValue(null)
      alert('Valeur sauvegardée avec succès !')
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error)
      alert('Erreur lors de la sauvegarde')
    } finally {
      setSaving(false)
    }
  }

  const handleValueDelete = async (valueId) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette valeur ?')) return
    
    try {
      await landingValuesService.delete(valueId)
      await onUpdate()
      alert('Valeur supprimée avec succès !')
    } catch (error) {
      console.error('Erreur lors de la suppression:', error)
      alert('Erreur lors de la suppression')
    }
  }

  const getIcon = (iconName) => {
    const IconComponent = LucideIcons[iconName] || LucideIcons.Shield
    return IconComponent
  }

  return (
    <div className="space-y-6">
      {/* Configuration de la section */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Award className="h-5 w-5 text-green-600" />
            Configuration de la Section Valeurs
          </CardTitle>
          <CardDescription>
            Modifier le titre et sous-titre de la section valeurs
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Label htmlFor="values_title">Titre de la Section</Label>
            <Input
              id="values_title"
              value={sectionData.values_title}
              onChange={(e) => setSectionData(prev => ({ ...prev, values_title: e.target.value }))}
              placeholder="Nos Valeurs"
            />
          </div>

          <div>
            <Label htmlFor="values_subtitle">Sous-titre</Label>
            <Input
              id="values_subtitle"
              value={sectionData.values_subtitle}
              onChange={(e) => setSectionData(prev => ({ ...prev, values_subtitle: e.target.value }))}
              placeholder="Les valeurs qui nous guident"
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

      {/* Gestion des valeurs */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Valeurs ({values.length})</CardTitle>
              <CardDescription>
                Gérer la liste des valeurs affichées
              </CardDescription>
            </div>
            <Dialog open={showValueDialog} onOpenChange={setShowValueDialog}>
              <DialogTrigger asChild>
                <Button 
                  onClick={() => {
                    setEditingValue({ titre: '', description: '', icone: 'Shield' })
                    setShowValueDialog(true)
                  }}
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Ajouter une Valeur
                </Button>
              </DialogTrigger>
              <ValueDialog
                value={editingValue}
                onSave={handleValueSave}
                onCancel={() => {
                  setShowValueDialog(false)
                  setEditingValue(null)
                }}
                saving={saving}
              />
            </Dialog>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {values.map((value) => {
              const IconComponent = getIcon(value.icone)
              return (
                <div key={value.id} className="p-4 border rounded-lg space-y-3 text-center">
                  <div className="bg-green-500/20 w-12 h-12 rounded-full flex items-center justify-center mx-auto">
                    <IconComponent className="h-6 w-6 text-green-600" />
                  </div>
                  <div>
                    <h4 className="font-medium">{value.titre}</h4>
                    <p className="text-sm text-muted-foreground line-clamp-2">
                      {value.description}
                    </p>
                  </div>
                  
                  <div className="flex gap-2 justify-center">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => {
                        setEditingValue(value)
                        setShowValueDialog(true)
                      }}
                    >
                      <Edit className="h-3 w-3 mr-1" />
                      Modifier
                    </Button>
                    <Button
                      size="sm"
                      variant="destructive"
                      onClick={() => handleValueDelete(value.id)}
                    >
                      <Trash2 className="h-3 w-3 mr-1" />
                      Supprimer
                    </Button>
                  </div>
                </div>
              )
            })}
          </div>

          {values.length === 0 && (
            <div className="text-center py-8 text-muted-foreground">
              <Award className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>Aucune valeur configurée</p>
              <p className="text-sm">Cliquez sur "Ajouter une Valeur" pour commencer</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

const ValueDialog = ({ value, onSave, onCancel, saving }) => {
  const [formData, setFormData] = useState({
    titre: value?.titre || '',
    description: value?.description || '',
    icone: value?.icone || 'Shield'
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
    'Shield', 'Award', 'Star', 'Heart', 'Users', 'CheckCircle',
    'Target', 'Zap', 'Compass', 'Crown', 'Gem', 'Trophy'
  ]

  return (
    <DialogContent className="max-w-md">
      <DialogHeader>
        <DialogTitle>
          {value?.id ? 'Modifier la Valeur' : 'Ajouter une Valeur'}
        </DialogTitle>
        <DialogDescription>
          Remplissez les informations de la valeur
        </DialogDescription>
      </DialogHeader>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <Label htmlFor="titre">Titre *</Label>
          <Input
            id="titre"
            value={formData.titre}
            onChange={(e) => setFormData(prev => ({ ...prev, titre: e.target.value }))}
            placeholder="Nom de la valeur"
            required
          />
        </div>

        <div>
          <Label htmlFor="description">Description *</Label>
          <Textarea
            id="description"
            value={formData.description}
            onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
            placeholder="Description de la valeur"
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