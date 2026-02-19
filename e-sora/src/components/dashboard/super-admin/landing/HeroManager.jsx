import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card'
import { Button } from '../../ui/button'
import { Input } from '../../ui/input'
import { Label } from '../../ui/label'
import { Textarea } from '../../ui/textarea'
import { Save, RefreshCw, Image } from 'lucide-react'
import { landingPageService } from '../../../services/apiService'

export const HeroManager = ({ landingData, onUpdate }) => {
  const [formData, setFormData] = useState({
    hero_title: landingData?.hero_title || '',
    hero_description: landingData?.hero_description || '',
    hero_button_primary: landingData?.hero_button_primary || '',
    hero_button_secondary: landingData?.hero_button_secondary || ''
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
      alert('Section Hero mise à jour avec succès !')
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
          <Image className="h-5 w-5 text-green-600" />
          Gestion de la Section Hero
        </CardTitle>
        <CardDescription>
          Modifier le contenu de la section principale avec image de fond
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="grid grid-cols-1 gap-4">
          <div>
            <Label htmlFor="hero_title">Titre Principal</Label>
            <Input
              id="hero_title"
              value={formData.hero_title}
              onChange={(e) => handleChange('hero_title', e.target.value)}
              placeholder="Titre accrocheur de votre plateforme"
            />
          </div>

          <div>
            <Label htmlFor="hero_description">Description</Label>
            <Textarea
              id="hero_description"
              value={formData.hero_description}
              onChange={(e) => handleChange('hero_description', e.target.value)}
              placeholder="Description détaillée de vos services"
              rows={4}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="hero_button_primary">Bouton Principal</Label>
              <Input
                id="hero_button_primary"
                value={formData.hero_button_primary}
                onChange={(e) => handleChange('hero_button_primary', e.target.value)}
                placeholder="Commencer"
              />
            </div>

            <div>
              <Label htmlFor="hero_button_secondary">Bouton Secondaire</Label>
              <Input
                id="hero_button_secondary"
                value={formData.hero_button_secondary}
                onChange={(e) => handleChange('hero_button_secondary', e.target.value)}
                placeholder="En savoir plus"
              />
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
          <div className="bg-gradient-to-r from-gray-800 to-gray-900 text-white p-8 rounded-lg text-center">
            <h1 className="text-3xl font-bold mb-4">
              {formData.hero_title || 'Titre principal'}
            </h1>
            <p className="text-lg mb-6 opacity-90">
              {formData.hero_description || 'Description de votre plateforme'}
            </p>
            <div className="flex gap-4 justify-center">
              <div className="bg-green-500/20 hover:bg-green-600 text-green-100 px-6 py-2 rounded-lg border border-green-500/30">
                {formData.hero_button_primary || 'Bouton Principal'}
              </div>
              <div className="border border-white/30 text-white px-6 py-2 rounded-lg">
                {formData.hero_button_secondary || 'Bouton Secondaire'}
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}