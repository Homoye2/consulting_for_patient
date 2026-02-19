import { useState, useEffect } from 'react'
import { landingPageService, landingServicesService, landingValuesService } from '../services/apiService'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Label } from '../components/ui/label'
import { Textarea } from '../components/ui/textarea'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs'
import { Save, Plus, Trash2, Loader2 } from 'lucide-react'

export const LandingPageAdmin = () => {
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [content, setContent] = useState(null)
  const [services, setServices] = useState([])
  const [values, setValues] = useState([])
  const [activeTab, setActiveTab] = useState('general')

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [contentRes, servicesRes, valuesRes] = await Promise.all([
        landingPageService.get(),
        landingServicesService.getAll(),
        landingValuesService.getAll(),
      ])
      setContent(contentRes.data)
      // Extraire le tableau results si la réponse est paginée
      const servicesData = Array.isArray(servicesRes.data) ? servicesRes.data : (servicesRes.data?.results || [])
      const valuesData = Array.isArray(valuesRes.data) ? valuesRes.data : (valuesRes.data?.results || [])
      setServices(servicesData)
      setValues(valuesData)
    } catch (error) {
      console.error('Erreur lors du chargement:', error)
      alert('Erreur lors du chargement des données')
    } finally {
      setLoading(false)
    }
  }

  const handleContentChange = (field, value) => {
    setContent({ ...content, [field]: value })
  }

  const handleSaveContent = async () => {
    try {
      setSaving(true)
      // Créer un objet avec uniquement les champs modifiables (exclure services, values, id, dates)
      const updateData = {
        logo_text: content.logo_text,
        hero_title: content.hero_title,
        hero_description: content.hero_description,
        hero_button_primary: content.hero_button_primary,
        hero_button_secondary: content.hero_button_secondary,
        about_title: content.about_title,
        about_description_1: content.about_description_1,
        about_description_2: content.about_description_2,
        about_stat_1_value: content.about_stat_1_value,
        about_stat_1_label: content.about_stat_1_label,
        about_stat_2_value: content.about_stat_2_value,
        about_stat_2_label: content.about_stat_2_label,
        services_title: content.services_title,
        services_subtitle: content.services_subtitle,
        values_title: content.values_title,
        values_subtitle: content.values_subtitle,
        footer_about_text: content.footer_about_text,
        footer_address: content.footer_address,
        footer_phone: content.footer_phone,
        footer_email: content.footer_email,
        footer_facebook: content.footer_facebook,
        footer_twitter: content.footer_twitter,
        footer_instagram: content.footer_instagram,
        footer_linkedin: content.footer_linkedin,
      }
      await landingPageService.partialUpdate(updateData)
      alert('Contenu sauvegardé avec succès !')
      // Recharger les données pour avoir la version à jour
      await fetchData()
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error)
      alert('Erreur lors de la sauvegarde')
    } finally {
      setSaving(false)
    }
  }

  const handleServiceChange = (index, field, value) => {
    const updated = [...services]
    updated[index] = { ...updated[index], [field]: value }
    setServices(updated)
  }

  const handleAddService = () => {
    setServices([...services, { titre: '', description: '', icone: 'Heart', ordre: services.length + 1, landing_page: 1 }])
  }

  const handleSaveService = async (service, index) => {
    try {
      if (service.id) {
        await landingServicesService.update(service.id, service)
      } else {
        const response = await landingServicesService.create(service)
        const updated = [...services]
        updated[index] = response.data
        setServices(updated)
      }
      alert('Service sauvegardé avec succès !')
    } catch (error) {
      console.error('Erreur lors de la sauvegarde du service:', error)
      alert('Erreur lors de la sauvegarde')
    }
  }

  const handleDeleteService = async (id, index) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce service ?')) return
    try {
      if (id) {
        await landingServicesService.delete(id)
      }
      const updated = services.filter((_, i) => i !== index)
      setServices(updated)
      alert('Service supprimé avec succès !')
    } catch (error) {
      console.error('Erreur lors de la suppression:', error)
      alert('Erreur lors de la suppression')
    }
  }

  const handleValueChange = (index, field, value) => {
    const updated = [...values]
    updated[index] = { ...updated[index], [field]: value }
    setValues(updated)
  }

  const handleAddValue = () => {
    setValues([...values, { titre: '', description: '', icone: 'Shield', ordre: values.length + 1, landing_page: 1 }])
  }

  const handleSaveValue = async (value, index) => {
    try {
      if (value.id) {
        await landingValuesService.update(value.id, value)
      } else {
        const response = await landingValuesService.create(value)
        const updated = [...values]
        updated[index] = response.data
        setValues(updated)
      }
      alert('Valeur sauvegardée avec succès !')
    } catch (error) {
      console.error('Erreur lors de la sauvegarde de la valeur:', error)
      alert('Erreur lors de la sauvegarde')
    }
  }

  const handleDeleteValue = async (id, index) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette valeur ?')) return
    try {
      if (id) {
        await landingValuesService.delete(id)
      }
      const updated = values.filter((_, i) => i !== index)
      setValues(updated)
      alert('Valeur supprimée avec succès !')
    } catch (error) {
      console.error('Erreur lors de la suppression:', error)
      alert('Erreur lors de la suppression')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    )
  }

  if (!content) {
    return <div>Erreur de chargement</div>
  }

  return (
    <div className="space-y-6">
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="general">Général</TabsTrigger>
          <TabsTrigger value="hero">Hero</TabsTrigger>
          <TabsTrigger value="about">À propos</TabsTrigger>
          <TabsTrigger value="footer">Footer</TabsTrigger>
        </TabsList>

        {/* Onglet Général */}
        <TabsContent value="general" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Informations générales</CardTitle>
              <CardDescription>Texte du logo et informations de base</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="logo_text">Texte du logo</Label>
                <Input
                  id="logo_text"
                  value={content.logo_text || ''}
                  onChange={(e) => handleContentChange('logo_text', e.target.value)}
                />
              </div>
              <Button onClick={handleSaveContent} disabled={saving}>
                {saving ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Sauvegarde...
                  </>
                ) : (
                  <>
                    <Save className="mr-2 h-4 w-4" />
                    Sauvegarder
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Onglet Hero */}
        <TabsContent value="hero" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Section Hero</CardTitle>
              <CardDescription>Contenu de la section principale</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="hero_title">Titre principal</Label>
                <Input
                  id="hero_title"
                  value={content.hero_title || ''}
                  onChange={(e) => handleContentChange('hero_title', e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="hero_description">Description</Label>
                <Textarea
                  id="hero_description"
                  value={content.hero_description || ''}
                  onChange={(e) => handleContentChange('hero_description', e.target.value)}
                  rows={4}
                />
              </div>
              <div>
                <Label htmlFor="hero_button_primary">Texte bouton principal</Label>
                <Input
                  id="hero_button_primary"
                  value={content.hero_button_primary || ''}
                  onChange={(e) => handleContentChange('hero_button_primary', e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="hero_button_secondary">Texte bouton secondaire</Label>
                <Input
                  id="hero_button_secondary"
                  value={content.hero_button_secondary || ''}
                  onChange={(e) => handleContentChange('hero_button_secondary', e.target.value)}
                />
              </div>
              <Button onClick={handleSaveContent} disabled={saving}>
                {saving ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Sauvegarde...
                  </>
                ) : (
                  <>
                    <Save className="mr-2 h-4 w-4" />
                    Sauvegarder
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Onglet À propos */}
        <TabsContent value="about" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Section À propos</CardTitle>
              <CardDescription>Contenu de la section à propos</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="about_title">Titre</Label>
                <Input
                  id="about_title"
                  value={content.about_title || ''}
                  onChange={(e) => handleContentChange('about_title', e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="about_description_1">Description 1</Label>
                <Textarea
                  id="about_description_1"
                  value={content.about_description_1 || ''}
                  onChange={(e) => handleContentChange('about_description_1', e.target.value)}
                  rows={4}
                />
              </div>
              <div>
                <Label htmlFor="about_description_2">Description 2</Label>
                <Textarea
                  id="about_description_2"
                  value={content.about_description_2 || ''}
                  onChange={(e) => handleContentChange('about_description_2', e.target.value)}
                  rows={4}
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="about_stat_1_value">Statistique 1 - Valeur</Label>
                  <Input
                    id="about_stat_1_value"
                    value={content.about_stat_1_value || ''}
                    onChange={(e) => handleContentChange('about_stat_1_value', e.target.value)}
                  />
                </div>
                <div>
                  <Label htmlFor="about_stat_1_label">Statistique 1 - Label</Label>
                  <Input
                    id="about_stat_1_label"
                    value={content.about_stat_1_label || ''}
                    onChange={(e) => handleContentChange('about_stat_1_label', e.target.value)}
                  />
                </div>
                <div>
                  <Label htmlFor="about_stat_2_value">Statistique 2 - Valeur</Label>
                  <Input
                    id="about_stat_2_value"
                    value={content.about_stat_2_value || ''}
                    onChange={(e) => handleContentChange('about_stat_2_value', e.target.value)}
                  />
                </div>
                <div>
                  <Label htmlFor="about_stat_2_label">Statistique 2 - Label</Label>
                  <Input
                    id="about_stat_2_label"
                    value={content.about_stat_2_label || ''}
                    onChange={(e) => handleContentChange('about_stat_2_label', e.target.value)}
                  />
                </div>
              </div>
              <Button onClick={handleSaveContent} disabled={saving}>
                {saving ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Sauvegarde...
                  </>
                ) : (
                  <>
                    <Save className="mr-2 h-4 w-4" />
                    Sauvegarder
                  </>
                )}
              </Button>
            </CardContent>
          </Card>

          {/* Services */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Services</CardTitle>
                  <CardDescription>Gérer les services affichés</CardDescription>
                </div>
                <Button onClick={handleAddService} size="sm">
                  <Plus className="h-4 w-4 mr-2" />
                  Ajouter
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4 pb-4 border-b">
                <div>
                  <Label htmlFor="services_title">Titre de la section</Label>
                  <Input
                    id="services_title"
                    value={content.services_title || ''}
                    onChange={(e) => handleContentChange('services_title', e.target.value)}
                  />
                </div>
                <div>
                  <Label htmlFor="services_subtitle">Sous-titre</Label>
                  <Input
                    id="services_subtitle"
                    value={content.services_subtitle || ''}
                    onChange={(e) => handleContentChange('services_subtitle', e.target.value)}
                  />
                </div>
              </div>
              {services.map((service, index) => (
                <div key={index} className="p-4 border rounded-lg space-y-3">
                  <div>
                    <Label>Titre</Label>
                    <Input
                      value={service.titre || ''}
                      onChange={(e) => handleServiceChange(index, 'titre', e.target.value)}
                    />
                  </div>
                  <div>
                    <Label>Description</Label>
                    <Textarea
                      value={service.description || ''}
                      onChange={(e) => handleServiceChange(index, 'description', e.target.value)}
                      rows={3}
                    />
                  </div>
                  <div>
                    <Label>Icône (nom Lucide)</Label>
                    <Input
                      value={service.icone || ''}
                      onChange={(e) => handleServiceChange(index, 'icone', e.target.value)}
                      placeholder="Heart, Stethoscope, etc."
                    />
                  </div>
                  <div className="flex gap-2">
                    <Button
                      onClick={() => handleSaveService(service, index)}
                      size="sm"
                    >
                      <Save className="h-4 w-4 mr-2" />
                      Sauvegarder
                    </Button>
                    <Button
                      onClick={() => handleDeleteService(service.id, index)}
                      variant="destructive"
                      size="sm"
                    >
                      <Trash2 className="h-4 w-4 mr-2" />
                      Supprimer
                    </Button>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Valeurs */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Valeurs</CardTitle>
                  <CardDescription>Gérer les valeurs affichées</CardDescription>
                </div>
                <Button onClick={handleAddValue} size="sm">
                  <Plus className="h-4 w-4 mr-2" />
                  Ajouter
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4 pb-4 border-b">
                <div>
                  <Label htmlFor="values_title">Titre de la section</Label>
                  <Input
                    id="values_title"
                    value={content.values_title || ''}
                    onChange={(e) => handleContentChange('values_title', e.target.value)}
                  />
                </div>
                <div>
                  <Label htmlFor="values_subtitle">Sous-titre</Label>
                  <Input
                    id="values_subtitle"
                    value={content.values_subtitle || ''}
                    onChange={(e) => handleContentChange('values_subtitle', e.target.value)}
                  />
                </div>
              </div>
              {values.map((value, index) => (
                <div key={index} className="p-4 border rounded-lg space-y-3">
                  <div>
                    <Label>Titre</Label>
                    <Input
                      value={value.titre || ''}
                      onChange={(e) => handleValueChange(index, 'titre', e.target.value)}
                    />
                  </div>
                  <div>
                    <Label>Description</Label>
                    <Textarea
                      value={value.description || ''}
                      onChange={(e) => handleValueChange(index, 'description', e.target.value)}
                      rows={3}
                    />
                  </div>
                  <div>
                    <Label>Icône (nom Lucide)</Label>
                    <Input
                      value={value.icone || ''}
                      onChange={(e) => handleValueChange(index, 'icone', e.target.value)}
                      placeholder="Shield, Award, etc."
                    />
                  </div>
                  <div className="flex gap-2">
                    <Button
                      onClick={() => handleSaveValue(value, index)}
                      size="sm"
                    >
                      <Save className="h-4 w-4 mr-2" />
                      Sauvegarder
                    </Button>
                    <Button
                      onClick={() => handleDeleteValue(value.id, index)}
                      variant="destructive"
                      size="sm"
                    >
                      <Trash2 className="h-4 w-4 mr-2" />
                      Supprimer
                    </Button>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Onglet Footer */}
        <TabsContent value="footer" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Footer</CardTitle>
              <CardDescription>Informations du pied de page</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="footer_about_text">Texte à propos</Label>
                <Textarea
                  id="footer_about_text"
                  value={content.footer_about_text || ''}
                  onChange={(e) => handleContentChange('footer_about_text', e.target.value)}
                  rows={3}
                />
              </div>
              <div>
                <Label htmlFor="footer_address">Adresse</Label>
                <Input
                  id="footer_address"
                  value={content.footer_address || ''}
                  onChange={(e) => handleContentChange('footer_address', e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="footer_phone">Téléphone</Label>
                <Input
                  id="footer_phone"
                  value={content.footer_phone || ''}
                  onChange={(e) => handleContentChange('footer_phone', e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="footer_email">Email</Label>
                <Input
                  id="footer_email"
                  type="email"
                  value={content.footer_email || ''}
                  onChange={(e) => handleContentChange('footer_email', e.target.value)}
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="footer_facebook">Facebook (URL)</Label>
                  <Input
                    id="footer_facebook"
                    type="url"
                    value={content.footer_facebook || ''}
                    onChange={(e) => handleContentChange('footer_facebook', e.target.value)}
                  />
                </div>
                <div>
                  <Label htmlFor="footer_twitter">Twitter (URL)</Label>
                  <Input
                    id="footer_twitter"
                    type="url"
                    value={content.footer_twitter || ''}
                    onChange={(e) => handleContentChange('footer_twitter', e.target.value)}
                  />
                </div>
                <div>
                  <Label htmlFor="footer_instagram">Instagram (URL)</Label>
                  <Input
                    id="footer_instagram"
                    type="url"
                    value={content.footer_instagram || ''}
                    onChange={(e) => handleContentChange('footer_instagram', e.target.value)}
                  />
                </div>
                <div>
                  <Label htmlFor="footer_linkedin">LinkedIn (URL)</Label>
                  <Input
                    id="footer_linkedin"
                    type="url"
                    value={content.footer_linkedin || ''}
                    onChange={(e) => handleContentChange('footer_linkedin', e.target.value)}
                  />
                </div>
              </div>
              <Button onClick={handleSaveContent} disabled={saving}>
                {saving ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Sauvegarde...
                  </>
                ) : (
                  <>
                    <Save className="mr-2 h-4 w-4" />
                    Sauvegarder
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

