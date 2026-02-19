import { PatientHeader } from './PatientHeader'
import { Footer } from '../landing/Footer'
import { landingPageService } from '../../services/apiService'
import { useState, useEffect } from 'react'
import { AnimatedPage } from '../ui/animated-page'

export const PatientLayout = ({ children }) => {
  const [footerData, setFooterData] = useState(null)

  useEffect(() => {
    const fetchFooterData = async () => {
      try {
        const response = await landingPageService.getPublic()
        setFooterData(response.data)
      } catch (error) {
        console.error('Erreur lors du chargement des données du footer:', error)
      }
    }
    fetchFooterData()
  }, [])

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <PatientHeader logoText={footerData?.logo_text || 'Hôpital Abass Ndao'} />
      <main className="flex-1">
        <AnimatedPage>{children}</AnimatedPage>
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

