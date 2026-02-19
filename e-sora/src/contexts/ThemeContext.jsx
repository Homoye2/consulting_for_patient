import { createContext, useContext, useEffect, useState } from 'react'

const ThemeContext = createContext(undefined)

// Fonction pour obtenir le thème résolu
const getResolvedTheme = (theme) => {
  if (theme === 'system') {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  }
  return theme
}

// Appliquer le thème au document
const applyTheme = (theme) => {
  const resolved = getResolvedTheme(theme)
  const root = document.documentElement
  root.classList.remove('light', 'dark')
  root.classList.add(resolved)
}

// Initialiser le thème avant le rendu React
const initializeTheme = () => {
  const savedTheme = localStorage.getItem('theme') || 'system'
  applyTheme(savedTheme)
  return savedTheme
}

// Initialiser immédiatement
const initialTheme = initializeTheme()

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState(initialTheme)

  const [resolvedTheme, setResolvedTheme] = useState(() => getResolvedTheme(initialTheme))

  useEffect(() => {
    // Écouter les changements de préférence système
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    
    const handleChange = (e) => {
      if (theme === 'system') {
        const newResolved = e.matches ? 'dark' : 'light'
        setResolvedTheme(newResolved)
        applyTheme('system')
      }
    }

    mediaQuery.addEventListener('change', handleChange)

    return () => mediaQuery.removeEventListener('change', handleChange)
  }, [theme])

  useEffect(() => {
    // Appliquer le thème au document
    applyTheme(theme)
    
    // Sauvegarder dans localStorage
    localStorage.setItem('theme', theme)
    
    // Mettre à jour le thème résolu
    const resolved = getResolvedTheme(theme)
    setResolvedTheme(resolved)
  }, [theme])

  const setThemeValue = (newTheme) => {
    setTheme(newTheme)
  }

  return (
    <ThemeContext.Provider value={{ theme, setTheme: setThemeValue, resolvedTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider')
  }
  return context
}

