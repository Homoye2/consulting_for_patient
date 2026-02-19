import { Link } from 'react-router-dom'
import { Button } from '../ui/button'
import { ArrowRight } from 'lucide-react'
import { AnimatedContainer } from '../ui/animated-page'

export const CTA = ({ title, description, buttonText, buttonLink }) => {
  return (
    <section className="py-16 md:py-24 bg-background border-t border-border">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <AnimatedContainer className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-6">
            {title}
          </h2>
          <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
            {description}
          </p>
          <Link to={buttonLink}>
            <Button 
              size="lg" 
              className="group bg-green-500/20 hover:bg-green-600 text-green-700 hover:text-white border border-green-500/30 hover:border-green-600 transition-all duration-300"
            >
              {buttonText}
              <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
            </Button>
          </Link>
        </AnimatedContainer>
      </div>
    </section>
  )
}