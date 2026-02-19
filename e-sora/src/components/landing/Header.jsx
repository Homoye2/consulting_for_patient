import { Link } from 'react-router-dom'
import { Button } from '../ui/button'
import { Heart } from 'lucide-react'
import { ThemeToggle } from '../ui/theme-toggle'
import logo from "../../../public/e_sora.png"

export const Header = () => {
  return (
    <header className="sticky top-0 z-50 bg-card/95 backdrop-blur-sm border-b border-border">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 md:h-20">
         
          <Link to="/" className="flex items-center gap-2">
            <div className="rounded-lg  p-2 md:w-[180px] w-[80px]">
               <img src={logo} alt="logo-e-sora" />
            </div>
          </Link>

          {/* Actions */}
          <div className="flex items-center gap-2">
            <ThemeToggle />
            <Link to="/login">
              <Button className="bg-green-500/20 hover:bg-green-600 text-green-700 hover:text-white border border-green-500/30 hover:border-green-600 transition-all duration-300">
                Connexion Super Admin
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </header>
  )
}

