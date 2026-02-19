import { useState, useEffect } from 'react'
import { Header } from '../../components/landing/Header'
import { Hero } from '../../components/landing/Hero'
import { About } from '../../components/landing/About'
import { Services } from '../../components/landing/Services'
import { Values } from '../../components/landing/Values'
import { Testimonials } from '../../components/landing/Testimonials'

import { Footer } from '../../components/landing/Footer'
import { landingPageService } from '../../services/apiService'
import { AnimatedContainer } from '../../components/ui/animated-page'

export const LandingPage = () => {
  const [content, setContent] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchContent = async () => {
      try {
        setLoading(true)
        const response = await landingPageService.getPublic()
        console.log("response leading :", response.data)
        setContent(response.data)
        setError(null)
      } catch (err) {
        console.error('Erreur lors du chargement du contenu:', err)
        setError('Impossible de charger le contenu de la page')
      } finally {
        setLoading(false)
      }
    }

    fetchContent()
  }, [])

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

  if (error || !content) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <p className="text-destructive mb-4">{error || 'Erreur de chargement'}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-primary text-primary-foreground rounded-md"
          >
            Réessayer
          </button>
        </div>
      </div>
    )
  }

  // Vérifier si les sections ont des données pour les afficher ou les cacher
  const hasHeroData = content.hero_title || content.hero_description
  const hasAboutData = content.about_title // Afficher si au moins le titre existe
  const hasServicesData = content.services_title // Afficher la section même si pas de services
  const hasValuesData = content.values_title // Afficher la section même si pas de valeurs
  const hasFooterData = true // Toujours afficher le footer

  return (
    <div className="min-h-screen bg-background">
      <AnimatedContainer>
        <Header />
      </AnimatedContainer>
      {hasHeroData && (
        <Hero
          title={content.hero_title}
          description={content.hero_description}
          buttonPrimary={content.hero_button_primary}
          buttonSecondary={content.hero_button_secondary}
        />
      )}
      {hasAboutData && (
        <About
          title={content.about_title}
          description1={content.about_description_1}
          description2={content.about_description_2}
          stat1Value={content.about_stat_1_value}
          stat1Label={content.about_stat_1_label}
          stat2Value={content.about_stat_2_value}
          stat2Label={content.about_stat_2_label}
        />
      )}
      
     
      
      {hasServicesData && (
        <Services
          title={content.services_title}
          subtitle={content.services_subtitle}
          services={content.services || []}
        />
      )}
      
      {hasValuesData && (
        <Values
          title={content.values_title}
          subtitle={content.values_subtitle}
          values={content.values || []}
        />
      )}
      
      <Testimonials />
      
     
      {hasFooterData && (
        <Footer
          logoText={content.logo_text || "E-Sora Santé"}
          aboutText={content.footer_about_text || "Votre partenaire de confiance pour la santé et le bien-être de la communauté."}
          address={content.footer_address || "Dakar, Sénégal"}
          phone={content.footer_phone || "+221 33 XXX XX XX"}
          email={content.footer_email || "contact@e-sora.sn"}
          facebook={content.footer_facebook}
          twitter={content.footer_twitter}
          instagram={content.footer_instagram}
          linkedin={content.footer_linkedin}
        />
      )}
    </div>
  )
}

