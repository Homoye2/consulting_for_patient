import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card'
import { Button } from '../../ui/button'
import { Input } from '../../ui/input'
import { Label } from '../../ui/label'
import { Save, RefreshCw, Header as HeaderIcon } from 'lucide-react'
import { landingPageService } from '../../../services/apiService'

export const HeaderManager = ({ landingData, onUpdate }) => {
  const [formData, setFormData] = useState({
    logo_text: landingData?.logo_text || ''
  })
  const [saving, setSaving] = useState(false)

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const handleSave = async () => {
    try {
      setSaving(true)
      await landingPageService.partialUpdate(formData)
      await onUpdate()
      alert('Header mis à jour avec succès !')
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error)
      alert('Erreur lors de la sauvegarde')
    } finally {
      setSaving(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <HeaderIcon className="h-5 w-5 text-green-600" />
          Gestion du Header
        </CardTitle>
        <CardDescription>
          Modifier les informations du header (logo et navigation)
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-4">
          <div>
            <Label htmlFor="logo_text">Texte du Logo</Label>
            <Input
              id="logo_text"
              value={formData.logo_text}
              onChange={(e) => handleChange('logo_text', e.target.value)}
              placeholder="Nom de votre plateforme"
            />
            <p className="text-xs text-muted-foreground mt-1">
              Ce texte apparaîtra à côté de l'icône cœur dans le header
            </p>
          </div>
        </div>

        <div className="flex gap-3">
          <Button onClick={handleSave} disabled={saving}>
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
        </div>

        {/* Prévisualisation */}
        <div className="border-t pt-4">
          <h4 className="font-medium mb-3">Prévisualisation</h4>
          <div className="bg-muted p-4 rounded-lg">
            <div className="flex items-center gap-2">
              <div className="rounded-lg bg-green-500/20 p-2">
                <HeaderIcon className="h-6 w-6 text-green-600" />
              </div>
              <span className="font-bold text-lg">
                {formData.logo_text || 'Nom de la plateforme'}
              </span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}