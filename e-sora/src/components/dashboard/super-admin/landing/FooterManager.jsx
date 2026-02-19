import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card'
import { Button } from '../../ui/button'
import { Input } from '../../ui/input'
import { Label } from '../../ui/label'
import { Textarea } from '../../ui/textarea'
import { 
  Save, 
  RefreshCw, 
  Phone, 
  Mail, 
  MapPin, 
  Facebook, 
  Twitter, 
  Instagram, 
  Linkedin,
  Heart,
  Globe
} from 'lucide-react'

export const FooterManager = ({ landingData, onUpdate }) => {
  const [footerData, setFooterData] = useState({
    logoText: 'E-Sora Santé',
    aboutText: 'Votre plateforme de confiance pour la planification familiale et les soins de santé reproductive.',
    address: 'Dakar, Sénégal',
    phone: '+221 33 XXX XX XX',
    email: 'contact@e-sora.sn',
    facebook: 'https://facebook.com/esora',
    twitter: 'https://twitter.com/esora',
    instagram: 'https://instagram.com/esora',
    linkedin: 'https://linkedin.com/company/esora'
  })
  
  const [saving, setSaving] = useState(false)
  const [hasChanges, setHasChanges] = useState(false)

  useEffect(() => {
    // Charger les données du footer depuis landingData si disponibles
    if (landingData?.footer) {
      setFooterData(prev => ({ ...prev, ...landingData.footer }))
    }
  }, [landingData])

  const handleInputChange = (field, value) => {
    setFooterData(prev => ({ ...prev, [field]: value }))
    setHasChanges(true)
  }

  const handleSave = async () => {
    try {
      setSaving(true)
      
      // Note: Dans une vraie application, vous feriez un appel API ici
      // await landingPageService.updateFooter(footerData)
      
      console.log('Données du footer sauvegardées:', footerData)
      alert('Footer sauvegardé avec succès !')
      setHasChanges(false)
      
      if (onUpdate) {
        onUpdate()
      }
      
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error)
      alert('Erreur lors de la sauvegarde')
    } finally {
      setSaving(false)
    }
  }

  const handleReset = () => {
    if (confirm('Êtes-vous sûr de vouloir annuler les modifications ?')) {
      if (landingData?.footer) {
        setFooterData(prev => ({ ...prev, ...landingData.footer }))
      }
      setHasChanges(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Phone className="h-5 w-5 text-green-600" />
          Gestion du Footer
        </CardTitle>
        <CardDescription>
          Gérer les informations de contact et les liens du pied de page
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Informations générales */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <h3 className="text-lg font-semibold flex items-center gap-2">
              <Heart className="h-5 w-5 text-green-600" />
              Informations générales
            </h3>
            
            <div>
              <Label htmlFor="logoText">Nom de l'organisation</Label>
              <Input
                id="logoText"
                value={footerData.logoText}
                onChange={(e) => handleInputChange('logoText', e.target.value)}
                placeholder="E-Sora Santé"
              />
            </div>

            <div>
              <Label htmlFor="aboutText">Description</Label>
              <Textarea
                id="aboutText"
                value={footerData.aboutText}
                onChange={(e) => handleInputChange('aboutText', e.target.value)}
                placeholder="Description de votre organisation"
                rows={3}
              />
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-lg font-semibold flex items-center gap-2">
              <MapPin className="h-5 w-5 text-green-600" />
              Informations de contact
            </h3>
            
            <div>
              <Label htmlFor="address">Adresse</Label>
              <Input
                id="address"
                value={footerData.address}
                onChange={(e) => handleInputChange('address', e.target.value)}
                placeholder="Dakar, Sénégal"
              />
            </div>

            <div>
              <Label htmlFor="phone">Téléphone</Label>
              <Input
                id="phone"
                value={footerData.phone}
                onChange={(e) => handleInputChange('phone', e.target.value)}
                placeholder="+221 33 XXX XX XX"
              />
            </div>

            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={footerData.email}
                onChange={(e) => handleInputChange('email', e.target.value)}
                placeholder="contact@e-sora.sn"
              />
            </div>
          </div>
        </div>

        {/* Réseaux sociaux */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold flex items-center gap-2">
            <Globe className="h-5 w-5 text-green-600" />
            Réseaux sociaux
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="facebook" className="flex items-center gap-2">
                <Facebook className="h-4 w-4 text-blue-600" />
                Facebook
              </Label>
              <Input
                id="facebook"
                value={footerData.facebook}
                onChange={(e) => handleInputChange('facebook', e.target.value)}
                placeholder="https://facebook.com/esora"
              />
            </div>

            <div>
              <Label htmlFor="twitter" className="flex items-center gap-2">
                <Twitter className="h-4 w-4 text-blue-400" />
                Twitter
              </Label>
              <Input
                id="twitter"
                value={footerData.twitter}
                onChange={(e) => handleInputChange('twitter', e.target.value)}
                placeholder="https://twitter.com/esora"
              />
            </div>

            <div>
              <Label htmlFor="instagram" className="flex items-center gap-2">
                <Instagram className="h-4 w-4 text-pink-600" />
                Instagram
              </Label>
              <Input
                id="instagram"
                value={footerData.instagram}
                onChange={(e) => handleInputChange('instagram', e.target.value)}
                placeholder="https://instagram.com/esora"
              />
            </div>

            <div>
              <Label htmlFor="linkedin" className="flex items-center gap-2">
                <Linkedin className="h-4 w-4 text-blue-700" />
                LinkedIn
              </Label>
              <Input
                id="linkedin"
                value={footerData.linkedin}
                onChange={(e) => handleInputChange('linkedin', e.target.value)}
                placeholder="https://linkedin.com/company/esora"
              />
            </div>
          </div>
        </div>

        {/* Aperçu */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">Aperçu</h3>
          <div className="bg-muted p-6 rounded-lg border">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
              {/* À propos */}
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <div className="rounded-lg bg-green-500/20 p-2">
                    <Heart className="h-4 w-4 text-green-600" />
                  </div>
                  <span className="font-bold">{footerData.logoText}</span>
                </div>
                <p className="text-muted-foreground text-xs">{footerData.aboutText}</p>
              </div>

              {/* Contact */}
              <div>
                <h4 className="font-semibold mb-3">Contact</h4>
                <div className="space-y-2 text-xs">
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <MapPin className="h-3 w-3" />
                    <span>{footerData.address}</span>
                  </div>
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <Phone className="h-3 w-3" />
                    <span>{footerData.phone}</span>
                  </div>
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <Mail className="h-3 w-3" />
                    <span>{footerData.email}</span>
                  </div>
                </div>
              </div>

              {/* Réseaux sociaux */}
              <div>
                <h4 className="font-semibold mb-3">Suivez-nous</h4>
                <div className="flex gap-3">
                  {footerData.facebook && (
                    <Facebook className="h-4 w-4 text-muted-foreground" />
                  )}
                  {footerData.twitter && (
                    <Twitter className="h-4 w-4 text-muted-foreground" />
                  )}
                  {footerData.instagram && (
                    <Instagram className="h-4 w-4 text-muted-foreground" />
                  )}
                  {footerData.linkedin && (
                    <Linkedin className="h-4 w-4 text-muted-foreground" />
                  )}
                </div>
              </div>
            </div>
            
            <div className="border-t border-border pt-4 mt-6 text-center text-xs text-muted-foreground">
              <p>&copy; {new Date().getFullYear()} {footerData.logoText}. Tous droits réservés.</p>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-3 pt-4 border-t">
          <Button 
            onClick={handleSave} 
            disabled={saving || !hasChanges}
            className="bg-green-600 hover:bg-green-700"
          >
            {saving ? (
              <>
                <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                Sauvegarde...
              </>
            ) : (
              <>
                <Save className="mr-2 h-4 w-4" />
                Sauvegarder les modifications
              </>
            )}
          </Button>
          
          {hasChanges && (
            <Button variant="outline" onClick={handleReset}>
              Annuler les modifications
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  )
}