import { Link } from 'react-router-dom'
import { Button } from '../ui/button'
import hospitalLogo from '../../assets/hopital.jpg'
import { AnimatedContainer } from '../ui/animated-page'


export const Hero = ({ title, description, buttonPrimary, buttonSecondary }) => {
  return (
    <section className="relative py-20 md:py-32 lg:py-40 overflow-hidden" style={{ backgroundImage: `url(${hospitalLogo})`, backgroundSize: 'cover', backgroundPosition: 'center' }}>
      <div className="absolute inset-0 bg-black/85"></div>
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <AnimatedContainer className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 text-white">
            {title}
          </h1>
          <p className="text-lg md:text-xl text-white/90 mb-8 max-w-2xl mx-auto">
            {description}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/login">
              <Button 
                size="lg" 
                className="w-full sm:w-auto bg-green-500/20 hover:bg-green-600 text-green-100 hover:text-white border border-green-500/30 hover:border-green-600 transition-all duration-300"
              >
                {buttonPrimary}
              </Button>
            </Link>
            <Button 
              size="lg" 
              variant="outline" 
              className="w-full sm:w-auto border-white/30 text-foreground hover:bg-white/10 hover:border-white/50 transition-all duration-300"
            >
              {buttonSecondary}
            </Button>
          </div>
        </AnimatedContainer>
      </div>
    </section>
  )
}

