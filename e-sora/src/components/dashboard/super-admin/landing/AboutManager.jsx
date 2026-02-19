import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card'
import { Button } from '../../ui/button'
import { Input } from '../../ui/input'
import { Label } from '../../ui/label'
import { Textarea } from '../../ui/textarea'
import { Save, RefreshCw, Info, Stethoscope } from 'lucide-react'
import { landingPageService } from '../../../services/apiService'

export const AboutManager = ({ landingData, onUpdate }) => {
  const [formData, setFormData] = useState({
    about_title: landingData?.about_title || '',
    about_description_1: landingData?.about_description_1 || '',
    about_description_2: landingData?.about_description_2 || '',
    about_stat_1_value: landingData?.about_stat_1_value || '',
    about_stat_1_label: landingData?.about_stat_1_label || '',
    about_stat_2_value: landingData?.about_stat_2_value || '',
    about_stat_2_label: landingData?.about_stat_2_label || ''
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
      alert('Section À propos mise à jour avec succès !')
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
          <Info className="h-5 w-5 text-green-600" />
          Gestion de la Section À propos
        </CardTitle>
        <CardDescription>
          Modifier le contenu de la section à propos avec descriptions et statistiques
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-4">
          <div>
            <Label htmlFor="about_title">Titre de la Section</Label>
            <Input
              id="about_title"
              value={formData.about_title}
              onChange={(e) => handleChange('about_title', e.target.value)}
              placeholder="À propos de nous"
            />
          </div>

          <div>
            <Label htmlFor="about_description_1">Description 1</Label>
            <Textarea
              id="about_description_1"
              value={formData.about_description_1}
              onChange={(e) => handleChange('about_description_1', e.target.value)}
              placeholder="Premier paragraphe de description"
              rows={4}
            />
          </div>

          <div>
            <Label htmlFor="about_description_2">Description 2</Label>
            <Textarea
              id="about_description_2"
              value={formData.about_description_2}
              onChange={(e) => handleChange('about_description_2', e.target.value)}
              placeholder="Deuxième paragraphe de description"
              rows={4}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <h4 className="font-medium">Statistique 1</h4>
              <div>
                <Label htmlFor="about_stat_1_value">Valeur</Label>
                <Input
                  id="about_stat_1_value"
                  value={formData.about_stat_1_value}
                  onChange={(e) => handleChange('about_stat_1_value', e.target.value)}
                  placeholder="1000+"
                />
              </div>
              <div>
                <Label htmlFor="about_stat_1_label">Label</Label>
                <Input
                  id="about_stat_1_label"
                  value={formData.about_stat_1_label}
                  onChange={(e) => handleChange('about_stat_1_label', e.target.value)}
                  placeholder="Patientes satisfaites"
                />
              </div>
            </div>

            <div className="space-y-2">
              <h4 className="font-medium">Statistique 2</h4>
              <div>
                <Label htmlFor="about_stat_2_value">Valeur</Label>
                <Input
                  id="about_stat_2_value"
                  value={formData.about_stat_2_value}
                  onChange={(e) => handleChange('about_stat_2_value', e.target.value)}
                  placeholder="50+"
                />
              </div>
              <div>
                <Label htmlFor="about_stat_2_label">Label</Label>
                <Input
                  id="about_stat_2_label"
                  value={formData.about_stat_2_label}
                  onChange={(e) => handleChange('about_stat_2_label', e.target.value)}
                  placeholder="Spécialistes"
                />
              </div>
            </div>
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
          <div className="bg-muted p-6 rounded-lg">
            <div className="grid md:grid-cols-2 gap-8 items-center">
              <div>
                <h2 className="text-2xl font-bold mb-4">
                  {formData.about_title || 'Titre de la section'}
                </h2>
                <p className="text-muted-foreground mb-4">
                  {formData.about_description_1 || 'Première description...'}
                </p>
                <p className="text-muted-foreground mb-6">
                  {formData.about_description_2 || 'Deuxième description...'}
                </p>
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center p-4 bg-background rounded-lg border border-green-500/20">
                    <div className="text-2xl font-bold text-green-600 mb-1">
                      {formData.about_stat_1_value || '0'}
                    </div>
                    <div className="text-sm text-muted-foreground">
                      {formData.about_stat_1_label || 'Label 1'}
                    </div>
                  </div>
                  <div className="text-center p-4 bg-background rounded-lg border border-green-500/20">
                    <div className="text-2xl font-bold text-green-600 mb-1">
                      {formData.about_stat_2_value || '0'}
                    </div>
                    <div className="text-sm text-muted-foreground">
                      {formData.about_stat_2_label || 'Label 2'}
                    </div>
                  </div>
                </div>
              </div>
              <div className="bg-gradient-to-br from-green-500/20 to-green-500/5 rounded-lg flex items-center justify-center h-48">
                <Stethoscope className="h-16 w-16 text-green-500/50" />
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}