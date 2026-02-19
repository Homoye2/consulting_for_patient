import { Link } from 'react-router-dom'
import * as LucideIcons from 'lucide-react'
import { AnimatedContainer, AnimatedStagger } from '../ui/animated-page'

export const Services = ({ title, subtitle, services = [] }) => {
  const getIcon = (iconName) => {
    const IconComponent = LucideIcons[iconName] || LucideIcons.Heart
    return IconComponent
  }

  return (
    <section className="py-16 md:py-24 bg-card">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <AnimatedContainer className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4 text-foreground">{title}</h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              {subtitle}
            </p>
            <div className="w-24 h-1 bg-green-500 mx-auto mt-4"></div>
          </AnimatedContainer>
          <AnimatedStagger className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 md:gap-8" staggerDelay={0.1}>
            {services.map((service) => {
              const IconComponent = getIcon(service.icone)
              return (
                <Link
                  key={service.id}
                  to={`/service/${service.id}`}
                  className="p-6 bg-background rounded-lg border h-[250px] border-border hover:border-green-500/50 transition-all hover:shadow-lg cursor-pointer flex flex-col group"
                >
                  <div className='flex flex-row space-x-2'>
                      <div className="bg-green-500/20 group-hover:bg-green-500/30 w-12 h-12 rounded-lg flex items-center justify-center mb-4 transition-colors">
                        <IconComponent className="h-6 w-6 text-green-600 group-hover:text-green-700 transition-colors" />
                      </div>
                      <h3 className="text-xl font-semibold mb-2 text-foreground">{service.titre}</h3>
                  </div>
                  <p className="text-muted-foreground flex-1 line-clamp-3">{service.description}</p>
                  <div className="mt-4 text-green-600 group-hover:text-green-700 text-sm font-medium transition-colors">
                    En savoir plus →
                  </div>
                </Link>
              )
            })}
          </AnimatedStagger>
        </div>
      </div>
    </section>
  )
}

