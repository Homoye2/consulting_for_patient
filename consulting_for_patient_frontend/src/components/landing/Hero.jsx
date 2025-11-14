import { Link } from 'react-router-dom'
import { Button } from '../ui/button'
import hospitalLogo from '../../assets/hopital.jpg'
export const Hero = ({ title, description, buttonPrimary, buttonSecondary }) => {
  return (
    <section className="relative py-20 md:py-32 lg:py-40 overflow-hidden" style={{ backgroundImage: `url(${hospitalLogo})`, backgroundSize: 'cover', backgroundPosition: 'center' }}>
      <div className="absolute inset-0 bg-black/85 from-primary/10 via-background to-primary/5"></div>
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 bg-gradient-to-r from-primary to-primary/70 bg-clip-text text-transparent">
            {title}
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            {description}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/login">
              <Button size="lg" className="w-full sm:w-auto">
                {buttonPrimary}
              </Button>
            </Link>
            <Button size="lg" variant="outline" className="w-full sm:w-auto">
              {buttonSecondary}
            </Button>
          </div>
        </div>
      </div>
    </section>
  )
}

