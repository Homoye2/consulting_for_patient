import { Link } from 'react-router-dom'
import { Button } from '../ui/button'
import { Heart } from 'lucide-react'

export const Header = ({ logoText }) => {
  return (
    <header className="sticky top-0 z-50 bg-card/95 backdrop-blur-sm border-b border-border">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 md:h-20">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <div className="rounded-lg bg-primary/20 p-2">
              <Heart className="h-6 w-6 md:h-8 md:w-8 text-primary" />
            </div>
            <span className="font-bold text-lg md:text-xl">{logoText}</span>
          </Link>

          {/* Bouton Connexion */}
          <Link to="/login">
            <Button>Connexion</Button>
          </Link>
        </div>
      </div>
    </header>
  )
}

