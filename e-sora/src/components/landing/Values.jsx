import * as LucideIcons from 'lucide-react'
import { AnimatedContainer, AnimatedStagger } from '../ui/animated-page'

export const Values = ({ title, subtitle, values = [] }) => {
  const getIcon = (iconName) => {
    const IconComponent = LucideIcons[iconName] || LucideIcons.Shield
    return IconComponent
  }

  return (
    <section className="py-16 md:py-24 bg-background">
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
            {values.map((value) => {
              const IconComponent = getIcon(value.icone)
              return (
                <div key={value.id} className="text-center group">
                  <div className="bg-green-500/20 group-hover:bg-green-500/30 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 transition-colors">
                    <IconComponent className="h-8 w-8 text-green-600 group-hover:text-green-700 transition-colors" />
                  </div>
                  <h3 className="text-lg font-semibold mb-2 text-foreground">{value.titre}</h3>
                  <p className="text-muted-foreground text-sm">{value.description}</p>
                </div>
              )
            })}
          </AnimatedStagger>
        </div>
      </div>
    </section>
  )
}

