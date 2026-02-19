import { Star, Quote } from 'lucide-react'
import { AnimatedContainer, AnimatedStagger } from '../ui/animated-page'

export const Testimonials = () => {
  const testimonials = [
    {
      id: 1,
      name: "Aïssatou Diallo",
      role: "Patiente",
      content: "Un service exceptionnel ! L'équipe médicale est très professionnelle et à l'écoute. Je recommande vivement cette plateforme.",
      rating: 5,
      avatar: "AD"
    },
    {
      id: 2,
      name: "Fatou Sall",
      role: "Patiente",
      content: "Grâce à cette plateforme, j'ai pu avoir accès facilement à des consultations de qualité. Le suivi est excellent.",
      rating: 5,
      avatar: "FS"
    },
    {
      id: 3,
      name: "Mariama Ba",
      role: "Patiente",
      content: "Interface intuitive et personnel médical compétent. Une vraie révolution dans l'accès aux soins de planification familiale.",
      rating: 5,
      avatar: "MB"
    }
  ]

  return (
    <section className="py-16 md:py-24 bg-card">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <AnimatedContainer className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4 text-foreground">
              Ce que disent nos patientes
            </h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Découvrez les témoignages de celles qui nous font confiance pour leur santé reproductive
            </p>
            <div className="w-24 h-1 bg-green-500 mx-auto mt-4"></div>
          </AnimatedContainer>
          
          <AnimatedStagger className="grid md:grid-cols-3 gap-8" staggerDelay={0.2}>
            {testimonials.map((testimonial) => (
              <div key={testimonial.id} className="bg-background h-60 p-6 rounded-lg border border-border relative">
                <Quote className="h-8 w-8 text-green-500/20 absolute top-4 right-4" />
                
                <div className="flex items-center mb-4">
                  <div className="w-12 h-12 bg-green-500/10 rounded-full flex items-center justify-center mr-4">
                    <span className="text-green-600 font-semibold">{testimonial.avatar}</span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-foreground">{testimonial.name}</h4>
                    <p className="text-sm text-muted-foreground">{testimonial.role}</p>
                  </div>
                </div>
                
                <div className="flex mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="h-4 w-4 text-yellow-400 fill-current" />
                  ))}
                </div>
                
                <p className="text-muted-foreground italic line-clamp-4">
                  "{testimonial.content}"
                </p>
              </div>
            ))}
          </AnimatedStagger>
        </div>
      </div>
    </section>
  )
}