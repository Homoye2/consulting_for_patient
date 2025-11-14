import * as LucideIcons from 'lucide-react'

export const Services = ({ title, subtitle, services = [] }) => {
  const getIcon = (iconName) => {
    const IconComponent = LucideIcons[iconName] || LucideIcons.Heart
    return IconComponent
  }

  return (
    <section className="py-16 md:py-24 bg-background">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">{title}</h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              {subtitle}
            </p>
            <div className="w-24 h-1 bg-primary mx-auto mt-4"></div>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
            {services.map((service) => {
              const IconComponent = getIcon(service.icone)
              return (
                <div
                  key={service.id}
                  className="p-6 bg-card rounded-lg border border-border hover:border-primary/50 transition-all hover:shadow-lg"
                >
                  <div className="bg-primary/10 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
                    <IconComponent className="h-6 w-6 text-primary" />
                  </div>
                  <h3 className="text-xl font-semibold mb-2">{service.titre}</h3>
                  <p className="text-muted-foreground">{service.description}</p>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </section>
  )
}

