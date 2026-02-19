import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card'
import { Button } from '../../ui/button'
import { Input } from '../../ui/input'
import { Label } from '../../ui/label'
import { Textarea } from '../../ui/textarea'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../ui/tabs'
import { 
  Globe, 
  Save, 
  RefreshCw, 
  Plus, 
  Trash2, 
  Edit, 
  Eye,
  ArrowUp,
  ArrowDown,
  Image,
  FileText,
  Star,
  Users
} from 'lucide-react'
import { AnimatedContainer } from '../../ui/animated-page'
import { landingPageService, landingServicesService, landingValuesService } from '../../../services/apiService'
import { useAuth } from '../../../contexts/AuthContext'

export const LandingPageManager = () => {
  const { user } = useAuth()
  const [content, setContent] = useState({
    // Hero Section
    hero_title: '',
    hero_description: '',
    hero_button_primary: '',
    hero_button_secondary: '',
    
    // About Section
    about_title: '',
    about_description_1: '',
    about_description_2: '',
    about_stat_1_label: '',
    about_stat_1_value: '',
    about_stat_2_label: '',
    about_stat_2_value: '',
    
    // Services Section
    services_title: '',
    services_subtitle: '',
    
    // Values Section
    values_title: '',
    values_subtitle: '',
    
    // Footer
    logo_text: '',
    footer_about_text: '',
    footer_address: '',
    footer_phone: '',
    footer_email: '',
    footer_facebook: '',
    footer_twitter: '',
    footer_instagram: '',
    footer_linkedin: ''
  })

  const [services, setServices] = useState([])
  const [values, setValues] = useState([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [editingService, setEditingService] = useState(null)
  const [editingValue, setEditingValue] = useState(null)
  const [newService, setNewService] = useState({ titre: '', description: '', icone: '', ordre: 1 })
  const [newValue, setNewValue] = useState({ titre: '', description: '', icone: '', ordre: 1 })
  const [permissionError, setPermissionError] = useState(null)

  useEffect(() => {
    fetchLandingPageData()
    checkPermissions()
  }, [])

  const checkPermissions = async () => {
    try {
      // Tester les permissions en essayant d'accéder à l'endpoint des utilisateurs
      const response = await fetch('/api/users/me/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json'
        }
      })
      
      if (response.status === 403) {
        setPermissionError('Permissions insuffisantes. Vous devez être connecté en tant que super_admin.')
      } else if (!response.ok) {
        setPermissionError(`Erreur d'authentification: ${response.status}`)
      } else {
        setPermissionError(null)
      }
    } catch (error) {
      console.error('Erreur lors de la vérification des permissions:', error)
      setPermissionError('Erreur de connexion au serveur')
    }
  }

  const fetchLandingPageData = async () => {
    try {
      setLoading(true)
      
      // Récupérer le contenu principal (toujours accessible)
      const contentResponse = await landingPageService.getPublic()
      setContent(contentResponse.data || {})
      
      // Essayer de récupérer les services et valeurs avec gestion d'erreur
      try {
        const servicesResponse = await landingServicesService.getPublic()
        const servicesData = Array.isArray(servicesResponse.data) 
          ? servicesResponse.data 
          : (servicesResponse.data?.results || [])
        setServices(Array.isArray(servicesData) ? servicesData : [])
      } catch (servicesError) {
        console.warn('Erreur lors du chargement des services:', servicesError)
        setServices([])
      }
      
      try {
        const valuesResponse = await landingValuesService.getAll()
        const valuesData = Array.isArray(valuesResponse.data) 
          ? valuesResponse.data 
          : (valuesResponse.data?.results || [])
        setValues(Array.isArray(valuesData) ? valuesData : [])
      } catch (valuesError) {
        console.warn('Erreur lors du chargement des valeurs:', valuesError)
        // Essayer l'endpoint public des valeurs si disponible
        try {
          const publicValuesResponse = await fetch('/api/values/public/')
          if (publicValuesResponse.ok) {
            const publicValuesData = await publicValuesResponse.json()
            setValues(Array.isArray(publicValuesData) ? publicValuesData : [])
          } else {
            setValues([])
          }
        } catch {
          setValues([])
        }
      }
      
    } catch (error) {
      console.error('Erreur lors du chargement:', error)
      alert('Erreur lors du chargement des données. Vérifiez vos permissions.')
      // Initialiser avec des valeurs par défaut en cas d'erreur
      setServices([])
      setValues([])
    } finally {
      setLoading(false)
    }
  }

  const handleContentChange = (key, value) => {
    setContent(prev => ({ ...prev, [key]: value }))
  }

  const handleSaveContent = async (section) => {
    setSaving(true)
    try {
      await landingPageService.update(content)
      alert(`Contenu ${section} sauvegardé avec succès !`)
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error)
      if (error.response?.status === 403) {
        alert('Vous n\'avez pas les permissions nécessaires pour modifier le contenu. Contactez l\'administrateur.')
      } else {
        alert('Erreur lors de la sauvegarde')
      }
    } finally {
      setSaving(false)
    }
  }

  const handleAddService = async () => {
    if (!newService.titre || !newService.description) {
      alert('Veuillez remplir tous les champs obligatoires')
      return
    }
    
    try {
      const serviceData = {
        ...newService,
        ordre: Array.isArray(services) ? services.length + 1 : 1
      }
      const response = await landingServicesService.create(serviceData)
      setServices([...services, response.data])
      setNewService({ titre: '', description: '', icone: '', ordre: 1 })
      alert('Service ajouté avec succès !')
    } catch (error) {
      console.error('Erreur lors de l\'ajout:', error)
      if (error.response?.status === 403) {
        alert('Vous n\'avez pas les permissions nécessaires pour ajouter un service. Contactez l\'administrateur.')
      } else {
        alert('Erreur lors de l\'ajout du service')
      }
    }
  }

  const handleAddValue = async () => {
    if (!newValue.titre || !newValue.description) {
      alert('Veuillez remplir tous les champs obligatoires')
      return
    }
    
    try {
      const valueData = {
        ...newValue,
        ordre: Array.isArray(values) ? values.length + 1 : 1
      }
      const response = await landingValuesService.create(valueData)
      setValues([...values, response.data])
      setNewValue({ titre: '', description: '', icone: '', ordre: 1 })
      alert('Valeur ajoutée avec succès !')
    } catch (error) {
      console.error('Erreur lors de l\'ajout:', error)
      if (error.response?.status === 403) {
        alert('Vous n\'avez pas les permissions nécessaires pour ajouter une valeur. Contactez l\'administrateur.')
      } else {
        alert('Erreur lors de l\'ajout de la valeur')
      }
    }
  }

  const handleDeleteService = async (serviceId) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce service ?')) return
    
    try {
      await landingServicesService.delete(serviceId)
      setServices(services.filter(s => s.id !== serviceId))
      alert('Service supprimé avec succès !')
    } catch (error) {
      console.error('Erreur lors de la suppression:', error)
      alert('Erreur lors de la suppression')
    }
  }

  const handleDeleteValue = async (valueId) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette valeur ?')) return
    
    try {
      await landingValuesService.delete(valueId)
      setValues(values.filter(v => v.id !== valueId))
      alert('Valeur supprimée avec succès !')
    } catch (error) {
      console.error('Erreur lors de la suppression:', error)
      alert('Erreur lors de la suppression')
    }
  }

  const moveItem = async (items, setItems, index, direction, type) => {
    if (!Array.isArray(items)) return
    
    const newItems = [...items]
    const targetIndex = direction === 'up' ? index - 1 : index + 1
    
    if (targetIndex >= 0 && targetIndex < newItems.length) {
      [newItems[index], newItems[targetIndex]] = [newItems[targetIndex], newItems[index]]
      // Mettre à jour les ordres
      newItems.forEach((item, idx) => {
        item.ordre = idx + 1
      })
      setItems(newItems)
      
      // Sauvegarder les nouveaux ordres via l'API
      try {
        const updatePromises = newItems.map(item => {
          if (type === 'service') {
            return landingServicesService.update(item.id, { ordre: item.ordre })
          } else {
            return landingValuesService.update(item.id, { ordre: item.ordre })
          }
        })
        await Promise.all(updatePromises)
      } catch (error) {
        console.error('Erreur lors de la mise à jour des ordres:', error)
        alert('Erreur lors de la réorganisation')
      }
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Chargement...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <AnimatedContainer>
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">Gestion Landing Page</h2>
            <p className="text-muted-foreground">
              Configuration du contenu de la page d'accueil
            </p>
            {user && (
              <p className="text-xs text-muted-foreground mt-1">
                Connecté en tant que: {user.email} | Rôle: {user.role} | ID: {user.id}
              </p>
            )}
            {permissionError && (
              <div className="mt-2 p-2 bg-yellow-100 border border-yellow-400 text-yellow-700 rounded text-sm">
                ⚠️ {permissionError}
              </div>
            )}
          </div>
          <Button onClick={fetchLandingPageData} variant="outline">
            <RefreshCw className="h-4 w-4 mr-2" />
            Actualiser
          </Button>
        </div>
      </AnimatedContainer>

      <Tabs defaultValue="hero" className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="hero">Hero & À propos</TabsTrigger>
          <TabsTrigger value="services">Services</TabsTrigger>
          <TabsTrigger value="values">Valeurs</TabsTrigger>
          <TabsTrigger value="footer">Footer</TabsTrigger>
          <TabsTrigger value="preview">Aperçu</TabsTrigger>
        </TabsList>

        <TabsContent value="hero" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Section Hero */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Image className="h-5 w-5" />
                  Section Hero
                </CardTitle>
                <CardDescription>
                  Contenu principal de la page d'accueil
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="hero_title">Titre principal</Label>
                  <Input
                    id="hero_title"
                    value={content.hero_title}
                    onChange={(e) => handleContentChange('hero_title', e.target.value)}
                    placeholder="Bienvenue à l'Hôpital..."
                  />
                </div>
                <div>
                  <Label htmlFor="hero_description">Description</Label>
                  <Textarea
                    id="hero_description"
                    value={content.hero_description}
                    onChange={(e) => handleContentChange('hero_description', e.target.value)}
                    placeholder="Votre partenaire de confiance..."
                    rows={3}
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="hero_button_primary">Bouton principal</Label>
                    <Input
                      id="hero_button_primary"
                      value={content.hero_button_primary}
                      onChange={(e) => handleContentChange('hero_button_primary', e.target.value)}
                      placeholder="Accéder à l'application"
                    />
                  </div>
                  <div>
                    <Label htmlFor="hero_button_secondary">Bouton secondaire</Label>
                    <Input
                      id="hero_button_secondary"
                      value={content.hero_button_secondary}
                      onChange={(e) => handleContentChange('hero_button_secondary', e.target.value)}
                      placeholder="En savoir plus"
                    />
                  </div>
                </div>
                <Button onClick={() => handleSaveContent('hero')} disabled={saving}>
                  {saving ? (
                    <>
                      <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                      Sauvegarde...
                    </>
                  ) : (
                    <>
                      <Save className="mr-2 h-4 w-4" />
                      Sauvegarder Hero
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>

            {/* Section À propos */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5" />
                  Section À propos
                </CardTitle>
                <CardDescription>
                  Informations sur l'établissement
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="about_title">Titre de la section</Label>
                  <Input
                    id="about_title"
                    value={content.about_title}
                    onChange={(e) => handleContentChange('about_title', e.target.value)}
                    placeholder="À propos de l'Hôpital..."
                  />
                </div>
                <div>
                  <Label htmlFor="about_description_1">Description 1</Label>
                  <Textarea
                    id="about_description_1"
                    value={content.about_description_1}
                    onChange={(e) => handleContentChange('about_description_1', e.target.value)}
                    placeholder="Première partie de la description..."
                    rows={2}
                  />
                </div>
                <div>
                  <Label htmlFor="about_description_2">Description 2</Label>
                  <Textarea
                    id="about_description_2"
                    value={content.about_description_2}
                    onChange={(e) => handleContentChange('about_description_2', e.target.value)}
                    placeholder="Deuxième partie de la description..."
                    rows={2}
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="about_stat_1_value">Statistique 1 - Valeur</Label>
                    <Input
                      id="about_stat_1_value"
                      value={content.about_stat_1_value}
                      onChange={(e) => handleContentChange('about_stat_1_value', e.target.value)}
                      placeholder="15+"
                    />
                  </div>
                  <div>
                    <Label htmlFor="about_stat_1_label">Statistique 1 - Label</Label>
                    <Input
                      id="about_stat_1_label"
                      value={content.about_stat_1_label}
                      onChange={(e) => handleContentChange('about_stat_1_label', e.target.value)}
                      placeholder="Années d'expérience"
                    />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="about_stat_2_value">Statistique 2 - Valeur</Label>
                    <Input
                      id="about_stat_2_value"
                      value={content.about_stat_2_value}
                      onChange={(e) => handleContentChange('about_stat_2_value', e.target.value)}
                      placeholder="50+"
                    />
                  </div>
                  <div>
                    <Label htmlFor="about_stat_2_label">Statistique 2 - Label</Label>
                    <Input
                      id="about_stat_2_label"
                      value={content.about_stat_2_label}
                      onChange={(e) => handleContentChange('about_stat_2_label', e.target.value)}
                      placeholder="Professionnels"
                    />
                  </div>
                </div>
                <Button onClick={() => handleSaveContent('à propos')} disabled={saving}>
                  {saving ? (
                    <>
                      <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                      Sauvegarde...
                    </>
                  ) : (
                    <>
                      <Save className="mr-2 h-4 w-4" />
                      Sauvegarder À propos
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="services" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Configuration de la section Services */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Star className="h-5 w-5" />
                  Configuration Services
                </CardTitle>
                <CardDescription>
                  Paramètres généraux de la section services
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="services_title">Titre de la section</Label>
                  <Input
                    id="services_title"
                    value={content.services_title}
                    onChange={(e) => handleContentChange('services_title', e.target.value)}
                    placeholder="Nos Services"
                  />
                </div>
                <div>
                  <Label htmlFor="services_subtitle">Sous-titre</Label>
                  <Textarea
                    id="services_subtitle"
                    value={content.services_subtitle}
                    onChange={(e) => handleContentChange('services_subtitle', e.target.value)}
                    placeholder="Nous offrons une gamme complète..."
                    rows={2}
                  />
                </div>
                <Button onClick={() => handleSaveContent('services')} disabled={saving}>
                  {saving ? (
                    <>
                      <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                      Sauvegarde...
                    </>
                  ) : (
                    <>
                      <Save className="mr-2 h-4 w-4" />
                      Sauvegarder Configuration
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>

            {/* Ajouter un nouveau service */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Plus className="h-5 w-5" />
                  Ajouter un Service
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="new_service_titre">Titre du service</Label>
                  <Input
                    id="new_service_titre"
                    value={newService.titre}
                    onChange={(e) => setNewService({...newService, titre: e.target.value})}
                    placeholder="Consultation générale"
                  />
                </div>
                <div>
                  <Label htmlFor="new_service_description">Description</Label>
                  <Textarea
                    id="new_service_description"
                    value={newService.description}
                    onChange={(e) => setNewService({...newService, description: e.target.value})}
                    placeholder="Description du service..."
                    rows={3}
                  />
                </div>
                <div>
                  <Label htmlFor="new_service_icone">Icône (nom Lucide)</Label>
                  <Input
                    id="new_service_icone"
                    value={newService.icone}
                    onChange={(e) => setNewService({...newService, icone: e.target.value})}
                    placeholder="Stethoscope"
                  />
                </div>
                <Button onClick={handleAddService} className="w-full">
                  <Plus className="mr-2 h-4 w-4" />
                  Ajouter le Service
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Liste des services existants */}
          <Card>
            <CardHeader>
              <CardTitle>Services Existants ({Array.isArray(services) ? services.length : 0})</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Array.isArray(services) && services.map((service, index) => (
                  <div key={service.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex-1">
                      <h4 className="font-medium">{service.titre}</h4>
                      <p className="text-sm text-muted-foreground">{service.description}</p>
                      <p className="text-xs text-muted-foreground mt-1">Icône: {service.icone} | Ordre: {service.ordre}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => moveItem(services, setServices, index, 'up', 'service')}
                        disabled={index === 0}
                      >
                        <ArrowUp className="h-4 w-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => moveItem(services, setServices, index, 'down', 'service')}
                        disabled={!Array.isArray(services) || index === services.length - 1}
                      >
                        <ArrowDown className="h-4 w-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => setEditingService(service)}
                      >
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="destructive"
                        onClick={() => handleDeleteService(service.id)}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
                {(!Array.isArray(services) || services.length === 0) && (
                  <p className="text-center text-muted-foreground py-8">
                    Aucun service configuré. Ajoutez votre premier service ci-dessus.
                  </p>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="values" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Configuration de la section Valeurs */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  Configuration Valeurs
                </CardTitle>
                <CardDescription>
                  Paramètres généraux de la section valeurs
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="values_title">Titre de la section</Label>
                  <Input
                    id="values_title"
                    value={content.values_title}
                    onChange={(e) => handleContentChange('values_title', e.target.value)}
                    placeholder="Pourquoi nous choisir ?"
                  />
                </div>
                <div>
                  <Label htmlFor="values_subtitle">Sous-titre</Label>
                  <Textarea
                    id="values_subtitle"
                    value={content.values_subtitle}
                    onChange={(e) => handleContentChange('values_subtitle', e.target.value)}
                    placeholder="Des valeurs qui font la différence..."
                    rows={2}
                  />
                </div>
                <Button onClick={() => handleSaveContent('valeurs')} disabled={saving}>
                  {saving ? (
                    <>
                      <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                      Sauvegarde...
                    </>
                  ) : (
                    <>
                      <Save className="mr-2 h-4 w-4" />
                      Sauvegarder Configuration
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>

            {/* Ajouter une nouvelle valeur */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Plus className="h-5 w-5" />
                  Ajouter une Valeur
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="new_value_titre">Titre de la valeur</Label>
                  <Input
                    id="new_value_titre"
                    value={newValue.titre}
                    onChange={(e) => setNewValue({...newValue, titre: e.target.value})}
                    placeholder="Excellence"
                  />
                </div>
                <div>
                  <Label htmlFor="new_value_description">Description</Label>
                  <Textarea
                    id="new_value_description"
                    value={newValue.description}
                    onChange={(e) => setNewValue({...newValue, description: e.target.value})}
                    placeholder="Description de la valeur..."
                    rows={3}
                  />
                </div>
                <div>
                  <Label htmlFor="new_value_icone">Icône (nom Lucide)</Label>
                  <Input
                    id="new_value_icone"
                    value={newValue.icone}
                    onChange={(e) => setNewValue({...newValue, icone: e.target.value})}
                    placeholder="Award"
                  />
                </div>
                <Button onClick={handleAddValue} className="w-full">
                  <Plus className="mr-2 h-4 w-4" />
                  Ajouter la Valeur
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Liste des valeurs existantes */}
          <Card>
            <CardHeader>
              <CardTitle>Valeurs Existantes ({Array.isArray(values) ? values.length : 0})</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Array.isArray(values) && values.map((value, index) => (
                  <div key={value.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex-1">
                      <h4 className="font-medium">{value.titre}</h4>
                      <p className="text-sm text-muted-foreground">{value.description}</p>
                      <p className="text-xs text-muted-foreground mt-1">Icône: {value.icone} | Ordre: {value.ordre}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => moveItem(values, setValues, index, 'up', 'value')}
                        disabled={index === 0}
                      >
                        <ArrowUp className="h-4 w-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => moveItem(values, setValues, index, 'down', 'value')}
                        disabled={!Array.isArray(values) || index === values.length - 1}
                      >
                        <ArrowDown className="h-4 w-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => setEditingValue(value)}
                      >
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="destructive"
                        onClick={() => handleDeleteValue(value.id)}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
                {(!Array.isArray(values) || values.length === 0) && (
                  <p className="text-center text-muted-foreground py-8">
                    Aucune valeur configurée. Ajoutez votre première valeur ci-dessus.
                  </p>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="footer" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Globe className="h-5 w-5" />
                Configuration Footer
              </CardTitle>
              <CardDescription>
                Informations de contact et réseaux sociaux
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="logo_text">Nom de l'organisation</Label>
                  <Input
                    id="logo_text"
                    value={content.logo_text}
                    onChange={(e) => handleContentChange('logo_text', e.target.value)}
                    placeholder="Hôpital Abass Ndao"
                  />
                </div>
                <div>
                  <Label htmlFor="footer_email">Email de contact</Label>
                  <Input
                    id="footer_email"
                    type="email"
                    value={content.footer_email}
                    onChange={(e) => handleContentChange('footer_email', e.target.value)}
                    placeholder="contact@hopital.sn"
                  />
                </div>
              </div>
              
              <div>
                <Label htmlFor="footer_about_text">Texte de présentation</Label>
                <Textarea
                  id="footer_about_text"
                  value={content.footer_about_text}
                  onChange={(e) => handleContentChange('footer_about_text', e.target.value)}
                  placeholder="Votre partenaire de confiance pour la santé..."
                  rows={3}
                />
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="footer_address">Adresse</Label>
                  <Input
                    id="footer_address"
                    value={content.footer_address}
                    onChange={(e) => handleContentChange('footer_address', e.target.value)}
                    placeholder="Abass Ndao, Dakar, Sénégal"
                  />
                </div>
                <div>
                  <Label htmlFor="footer_phone">Téléphone</Label>
                  <Input
                    id="footer_phone"
                    value={content.footer_phone}
                    onChange={(e) => handleContentChange('footer_phone', e.target.value)}
                    placeholder="+221 33 XXX XX XX"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                  <Label htmlFor="footer_facebook">Facebook</Label>
                  <Input
                    id="footer_facebook"
                    value={content.footer_facebook || ''}
                    onChange={(e) => handleContentChange('footer_facebook', e.target.value)}
                    placeholder="https://facebook.com/..."
                  />
                </div>
                <div>
                  <Label htmlFor="footer_twitter">Twitter</Label>
                  <Input
                    id="footer_twitter"
                    value={content.footer_twitter || ''}
                    onChange={(e) => handleContentChange('footer_twitter', e.target.value)}
                    placeholder="https://twitter.com/..."
                  />
                </div>
                <div>
                  <Label htmlFor="footer_instagram">Instagram</Label>
                  <Input
                    id="footer_instagram"
                    value={content.footer_instagram || ''}
                    onChange={(e) => handleContentChange('footer_instagram', e.target.value)}
                    placeholder="https://instagram.com/..."
                  />
                </div>
                <div>
                  <Label htmlFor="footer_linkedin">LinkedIn</Label>
                  <Input
                    id="footer_linkedin"
                    value={content.footer_linkedin || ''}
                    onChange={(e) => handleContentChange('footer_linkedin', e.target.value)}
                    placeholder="https://linkedin.com/..."
                  />
                </div>
              </div>

              <Button onClick={() => handleSaveContent('footer')} disabled={saving}>
                {saving ? (
                  <>
                    <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                    Sauvegarde...
                  </>
                ) : (
                  <>
                    <Save className="mr-2 h-4 w-4" />
                    Sauvegarder Footer
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="preview" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Eye className="h-5 w-5" />
                Aperçu de la Landing Page
              </CardTitle>
              <CardDescription>
                Prévisualisation du contenu configuré
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6 p-4 border rounded-lg bg-muted/20">
                {/* Aperçu Hero */}
                <div className="text-center space-y-2">
                  <h1 className="text-2xl font-bold">{content.hero_title || 'Titre Hero'}</h1>
                  <p className="text-muted-foreground">{content.hero_description || 'Description Hero'}</p>
                  <div className="flex gap-2 justify-center">
                    <span className="px-4 py-2 bg-primary text-primary-foreground rounded text-sm">
                      {content.hero_button_primary || 'Bouton Principal'}
                    </span>
                    <span className="px-4 py-2 border rounded text-sm">
                      {content.hero_button_secondary || 'Bouton Secondaire'}
                    </span>
                  </div>
                </div>

                {/* Aperçu About */}
                <div className="space-y-2">
                  <h2 className="text-xl font-semibold">{content.about_title || 'Titre À propos'}</h2>
                  <p className="text-sm text-muted-foreground">{content.about_description_1}</p>
                  <p className="text-sm text-muted-foreground">{content.about_description_2}</p>
                  <div className="flex gap-4 text-sm">
                    <div>
                      <span className="font-bold">{content.about_stat_1_value}</span>
                      <span className="text-muted-foreground ml-1">{content.about_stat_1_label}</span>
                    </div>
                    <div>
                      <span className="font-bold">{content.about_stat_2_value}</span>
                      <span className="text-muted-foreground ml-1">{content.about_stat_2_label}</span>
                    </div>
                  </div>
                </div>

                {/* Aperçu Services */}
                <div className="space-y-2">
                  <h2 className="text-xl font-semibold">{content.services_title || 'Nos Services'}</h2>
                  <p className="text-sm text-muted-foreground">{content.services_subtitle}</p>
                  <div className="grid grid-cols-2 gap-2">
                    {Array.isArray(services) && services.slice(0, 4).map(service => (
                      <div key={service.id} className="p-2 border rounded text-sm">
                        <div className="font-medium">{service.titre}</div>
                        <div className="text-xs text-muted-foreground">{service.description}</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Aperçu Values */}
                <div className="space-y-2">
                  <h2 className="text-xl font-semibold">{content.values_title || 'Nos Valeurs'}</h2>
                  <p className="text-sm text-muted-foreground">{content.values_subtitle}</p>
                  <div className="grid grid-cols-2 gap-2">
                    {Array.isArray(values) && values.slice(0, 4).map(value => (
                      <div key={value.id} className="p-2 border rounded text-sm">
                        <div className="font-medium">{value.titre}</div>
                        <div className="text-xs text-muted-foreground">{value.description}</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Aperçu Footer */}
                <div className="border-t pt-4 text-sm">
                  <div className="font-medium">{content.logo_text || 'Nom Organisation'}</div>
                  <div className="text-muted-foreground">{content.footer_about_text}</div>
                  <div className="text-xs text-muted-foreground mt-2">
                    {content.footer_address} | {content.footer_phone} | {content.footer_email}
                  </div>
                </div>
              </div>
              
              <div className="mt-4 text-center">
                <Button onClick={() => window.open('/', '_blank')} variant="outline">
                  <Eye className="mr-2 h-4 w-4" />
                  Voir la page complète
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}