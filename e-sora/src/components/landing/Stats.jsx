import { AnimatedContainer, AnimatedStagger } from '../ui/animated-page'

export const Stats = ({ stats = [] }) => {
  return (
    <section className="py-16 md:py-20 bg-green-500/5">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <AnimatedContainer className="max-w-4xl mx-auto">
          <AnimatedStagger className="grid grid-cols-2 md:grid-cols-4 gap-8" staggerDelay={0.1}>
            {stats.map((stat, index) => (
              <div key={index} className="text-center group">
                <div className="text-3xl md:text-4xl font-bold text-green-600 group-hover:text-green-700 mb-2 transition-colors">
                  {stat.value}
                </div>
                <div className="text-sm md:text-base text-muted-foreground">
                  {stat.label}
                </div>
              </div>
            ))}
          </AnimatedStagger>
        </AnimatedContainer>
      </div>
    </section>
  )
}