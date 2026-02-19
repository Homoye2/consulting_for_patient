import { Stethoscope } from 'lucide-react'
import { AnimatedContainer, AnimatedStagger } from '../ui/animated-page'

export const About = ({
  title,
  description1,
  description2,
  stat1Value,
  stat1Label,
  stat2Value,
  stat2Label,
}) => {
  return (
    <section className="py-16 md:py-24 bg-background">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <AnimatedContainer className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4 text-foreground">{title}</h2>
            <div className="w-24 h-1 bg-green-500 mx-auto"></div>
          </AnimatedContainer>
          <AnimatedStagger className="grid md:grid-cols-2 gap-8 lg:gap-12 items-center" staggerDelay={0.2}>
            <div>
              <p className="text-muted-foreground mb-4 text-lg leading-relaxed text-justify">
                {description1}
              </p>
              <p className="text-muted-foreground mb-4 text-lg leading-relaxed text-justify">
                {description2}
              </p>
              <div className="grid grid-cols-2 gap-6 mt-8">
                <div className="text-center p-4 bg-card rounded-lg border border-green-500/20 hover:border-green-500/40 transition-colors">
                  <div className="text-3xl font-bold text-green-600 mb-2">{stat1Value}</div>
                  <div className="text-sm text-muted-foreground">{stat1Label}</div>
                </div>
                <div className="text-center p-4 bg-card rounded-lg border border-green-500/20 hover:border-green-500/40 transition-colors">
                  <div className="text-3xl font-bold text-green-600 mb-2">{stat2Value}</div>
                  <div className="text-sm text-muted-foreground">{stat2Label}</div>
                </div>
              </div>
            </div>
            <div className="relative">
              <div className="aspect-video bg-gradient-to-br from-green-500/20 to-green-500/5 rounded-lg flex items-center justify-center">
                <Stethoscope className="h-32 w-32 text-green-500/50" />
              </div>
            </div>
          </AnimatedStagger>
        </div>
      </div>
    </section>
  )
}

