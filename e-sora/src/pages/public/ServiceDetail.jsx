import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { Header } from '../../components/landing/Header'
import { Footer } from '../../components/landing/Footer'
import { landingServicesService, landingPageService } from '../../services/apiService'
import { AnimatedContainer } from '../../components/ui/animated-page'
import { Button } from '../../components/ui/button'
import { ArrowLeft } from 'lucide-react'
import * as LucideIcons from 'lucide-react'

export const ServiceDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [service, setService] = useState(null)
  const [footerData, setFooterData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const [serviceRes, footerRes] = await Promise.all([
          landingServicesService.getById(id),
          landingPageService.getPublic()
        ])
        setService(serviceRes.data)
        setFooterData(footerRes.data)
        setError(null)
      } catch (err) {
        console.error('Erreur lors du chargement du service:', err)
        setError('Service introuvable')
      } finally {
        setLoading(false)
      }
    }

    if (id) {
      fetchData()
    }
  }, [id])

  const getIcon = (iconName) => {
    const IconComponent = LucideIcons[iconName] || LucideIcons.Heart
    return IconComponent
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Chargement...</p>
        </div>
      </div>
    )
  }

  if (error || !service) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <p className="text-destructive mb-4">{error || 'Service introuvable'}</p>
          <Button onClick={() => navigate('/')}>Retour à l'accueil</Button>
        </div>
      </div>
    )
  }

  const IconComponent = getIcon(service.icone)

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {footerData && (
        <AnimatedContainer>
          <Header logoText={footerData.logo_text} />
        </AnimatedContainer>
      )}

      <main className="flex-1">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16">
          <AnimatedContainer>
            <div className="max-w-4xl mx-auto">
              {/* Bouton retour */}
              <Button
                variant="ghost"
                onClick={() => navigate(-1)}
                className="mb-6"
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                Retour
              </Button>

              {/* En-tête du service */}
              <div className="mb-8">
                <div className="flex items-center gap-4 mb-6">
                  <div className="bg-primary/10 w-16 h-16 rounded-lg flex items-center justify-center">
                    <IconComponent className="h-8 w-8 text-primary" />
                  </div>
                  <div>
                    <h1 className="text-4xl md:text-5xl font-bold mb-2">{service.titre}</h1>
                    <p className="text-lg text-muted-foreground">{service.description}</p>
                  </div>
                </div>
              </div>

              {/* Contenu détaillé */}
              {service.contenu_detail ? (
                <AnimatedContainer delay={0.1}>
                  <div className="bg-card rounded-lg border border-border p-6 md:p-8 mb-8">
                    <h2 className="text-2xl md:text-3xl font-bold mb-6">Comment fonctionne ce service ?</h2>
                    <div className="prose prose-lg max-w-none">
                      <div 
                        className="text-muted-foreground leading-relaxed whitespace-pre-line space-y-4"
                        style={{ 
                          whiteSpace: 'pre-line',
                          lineHeight: '1.8'
                        }}
                      >
                        {service.contenu_detail.split('\n').map((paragraph, index) => (
                          paragraph.trim() && (
                            <p key={index} className="mb-4">
                              {paragraph.trim()}
                            </p>
                          )
                        ))}
                      </div>
                    </div>
                  </div>
                </AnimatedContainer>
              ) : (
                <AnimatedContainer delay={0.1}>
                  <div className="bg-card rounded-lg border border-border p-6 md:p-8 mb-8">
                    <h2 className="text-2xl md:text-3xl font-bold mb-6">Comment fonctionne ce service ?</h2>
                    <p className="text-muted-foreground text-center py-8">
                      Le contenu détaillé de ce service sera bientôt disponible.
                    </p>
                  </div>
                </AnimatedContainer>
              )}

              {/* Actions */}
              <AnimatedContainer delay={0.2}>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Link to="/login">
                    <Button size="lg" className="w-full sm:w-auto">
                      Prendre rendez-vous
                    </Button>
                  </Link>
                  <Button
                    variant="outline"
                    size="lg"
                    onClick={() => navigate('/')}
                    className="w-full sm:w-auto"
                  >
                    Retour à l'accueil
                  </Button>
                </div>
              </AnimatedContainer>
            </div>
          </AnimatedContainer>
        </div>
      </main>

      {footerData && (
        <Footer
          logoText={footerData.logo_text}
          aboutText={footerData.footer_about_text}
          address={footerData.footer_address}
          phone={footerData.footer_phone}
          email={footerData.footer_email}
          facebook={footerData.footer_facebook}
          twitter={footerData.footer_twitter}
          instagram={footerData.footer_instagram}
          linkedin={footerData.footer_linkedin}
        />
      )}
    </div>
  )
}

