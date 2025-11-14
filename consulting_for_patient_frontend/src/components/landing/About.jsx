import { Stethoscope } from 'lucide-react'

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
    <section className="py-16 md:py-24 bg-card">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">{title}</h2>
            <div className="w-24 h-1 bg-primary mx-auto"></div>
          </div>
          <div className="grid md:grid-cols-2 gap-8 lg:gap-12 items-center">
            <div>
              <p className="text-muted-foreground mb-4 text-lg leading-relaxed">
                {description1}
              </p>
              <p className="text-muted-foreground mb-4 text-lg leading-relaxed">
                {description2}
              </p>
              <div className="grid grid-cols-2 gap-6 mt-8">
                <div className="text-center p-4 bg-background rounded-lg">
                  <div className="text-3xl font-bold text-primary mb-2">{stat1Value}</div>
                  <div className="text-sm text-muted-foreground">{stat1Label}</div>
                </div>
                <div className="text-center p-4 bg-background rounded-lg">
                  <div className="text-3xl font-bold text-primary mb-2">{stat2Value}</div>
                  <div className="text-sm text-muted-foreground">{stat2Label}</div>
                </div>
              </div>
            </div>
            <div className="relative">
              <div className="aspect-video bg-gradient-to-br from-primary/20 to-primary/5 rounded-lg flex items-center justify-center">
                <Stethoscope className="h-32 w-32 text-primary/50" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

