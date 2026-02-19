import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card'
import { Button } from '../../ui/button'
import { Input } from '../../ui/input'
import { Label } from '../../ui/label'
import { Textarea } from '../../ui/textarea'
import { 
  Save, 
  RefreshCw, 
  MessageSquare, 
  Plus, 
  Edit, 
  Trash2,
  Star,
  Quote
} from 'lucide-react'
import { 
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '../../ui/dialog'

export const TestimonialsManager = ({ onUpdate }) => {
  const [testimonials, setTestimonials] = useState([
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
  ])
  
  const [editingTestimonial, setEditingTestimonial] = useState(null)
  const [showTestimonialDialog, setShowTestimonialDialog] = useState(false)
  const [saving, setSaving] = useState(false)

  const handleTestimonialSave = async (testimonialData) => {
    try {
      setSaving(true)
      
      if (editingTestimonial?.id) {
        // Modifier un témoignage existant
        setTestimonials(prev => prev.map(t => 
          t.id === editingTestimonial.id ? { ...t, ...testimonialData } : t
        ))
      } else {
        // Ajouter un nouveau témoignage
        const newTestimonial = {
          ...testimonialData,
          id: Math.max(...testimonials.map(t => t.id)) + 1,
          avatar: testimonialData.name.split(' ').map(n => n[0]).join('').toUpperCase()
        }
        setTestimonials(prev => [...prev, newTestimonial])
      }
      
      setShowTestimonialDialog(false)
      setEditingTestimonial(null)
      alert('Témoignage sauvegardé avec succès !')
      
      // Note: Dans une vraie application, vous feriez un appel API ici
      // await testimonialsService.save(testimonialData)
      
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error)
      alert('Erreur lors de la sauvegarde')
    } finally {
      setSaving(false)
    }
  }

  const handleTestimonialDelete = async (testimonialId) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce témoignage ?')) return
    
    try {
      setTestimonials(prev => prev.filter(t => t.id !== testimonialId))
      alert('Témoignage supprimé avec succès !')
      
      // Note: Dans une vraie application, vous feriez un appel API ici
      // await testimonialsService.delete(testimonialId)
      
    } catch (error) {
      console.error('Erreur lors de la suppression:', error)
      alert('Erreur lors de la suppression')
    }
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <MessageSquare className="h-5 w-5 text-green-600" />
              Gestion des Témoignages ({testimonials.length})
            </CardTitle>
            <CardDescription>
              Gérer les témoignages de patientes affichés sur la landing page
            </CardDescription>
          </div>
          <Dialog open={showTestimonialDialog} onOpenChange={setShowTestimonialDialog}>
            <DialogTrigger asChild>
              <Button 
                onClick={() => {
                  setEditingTestimonial({ name: '', role: 'Patiente', content: '', rating: 5 })
                  setShowTestimonialDialog(true)
                }}
              >
                <Plus className="h-4 w-4 mr-2" />
                Ajouter un Témoignage
              </Button>
            </DialogTrigger>
            <TestimonialDialog
              testimonial={editingTestimonial}
              onSave={handleTestimonialSave}
              onCancel={() => {
                setShowTestimonialDialog(false)
                setEditingTestimonial(null)
              }}
              saving={saving}
            />
          </Dialog>
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {testimonials.map((testimonial) => (
            <div key={testimonial.id} className="bg-muted p-6 rounded-lg border relative">
              <Quote className="h-6 w-6 text-green-500/20 absolute top-4 right-4" />
              
              <div className="flex items-center mb-4">
                <div className="w-10 h-10 bg-green-500/10 rounded-full flex items-center justify-center mr-3">
                  <span className="text-green-600 font-semibold text-sm">{testimonial.avatar}</span>
                </div>
                <div>
                  <h4 className="font-semibold text-sm">{testimonial.name}</h4>
                  <p className="text-xs text-muted-foreground">{testimonial.role}</p>
                </div>
              </div>
              
              <div className="flex mb-3">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <Star key={i} className="h-3 w-3 text-yellow-400 fill-current" />
                ))}
              </div>
              
              <p className="text-muted-foreground text-sm italic mb-4 line-clamp-3">
                "{testimonial.content}"
              </p>

              <div className="flex gap-2">
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => {
                    setEditingTestimonial(testimonial)
                    setShowTestimonialDialog(true)
                  }}
                >
                  <Edit className="h-3 w-3 mr-1" />
                  Modifier
                </Button>
                <Button
                  size="sm"
                  variant="destructive"
                  onClick={() => handleTestimonialDelete(testimonial.id)}
                >
                  <Trash2 className="h-3 w-3 mr-1" />
                  Supprimer
                </Button>
              </div>
            </div>
          ))}
        </div>

        {testimonials.length === 0 && (
          <div className="text-center py-8 text-muted-foreground">
            <MessageSquare className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <p>Aucun témoignage configuré</p>
            <p className="text-sm">Cliquez sur "Ajouter un Témoignage" pour commencer</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

const TestimonialDialog = ({ testimonial, onSave, onCancel, saving }) => {
  const [formData, setFormData] = useState({
    name: testimonial?.name || '',
    role: testimonial?.role || 'Patiente',
    content: testimonial?.content || '',
    rating: testimonial?.rating || 5
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!formData.name || !formData.content) {
      alert('Veuillez remplir tous les champs obligatoires')
      return
    }
    onSave(formData)
  }

  return (
    <DialogContent className="max-w-md">
      <DialogHeader>
        <DialogTitle>
          {testimonial?.id ? 'Modifier le Témoignage' : 'Ajouter un Témoignage'}
        </DialogTitle>
        <DialogDescription>
          Remplissez les informations du témoignage
        </DialogDescription>
      </DialogHeader>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <Label htmlFor="name">Nom *</Label>
          <Input
            id="name"
            value={formData.name}
            onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
            placeholder="Nom de la patiente"
            required
          />
        </div>

        <div>
          <Label htmlFor="role">Rôle</Label>
          <Input
            id="role"
            value={formData.role}
            onChange={(e) => setFormData(prev => ({ ...prev, role: e.target.value }))}
            placeholder="Patiente"
          />
        </div>

        <div>
          <Label htmlFor="content">Témoignage *</Label>
          <Textarea
            id="content"
            value={formData.content}
            onChange={(e) => setFormData(prev => ({ ...prev, content: e.target.value }))}
            placeholder="Contenu du témoignage"
            rows={4}
            required
          />
        </div>

        <div>
          <Label htmlFor="rating">Note (sur 5)</Label>
          <select
            id="rating"
            value={formData.rating}
            onChange={(e) => setFormData(prev => ({ ...prev, rating: parseInt(e.target.value) }))}
            className="w-full px-3 py-2 border border-border rounded-md bg-background"
          >
            {[1, 2, 3, 4, 5].map(rating => (
              <option key={rating} value={rating}>
                {rating} étoile{rating > 1 ? 's' : ''}
              </option>
            ))}
          </select>
        </div>

        <div className="flex gap-3 pt-4">
          <Button type="submit" disabled={saving}>
            {saving ? (
              <>
                <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                Sauvegarde...
              </>
            ) : (
              <>
                <Save className="mr-2 h-4 w-4" />
                Sauvegarder
              </>
            )}
          </Button>
          <Button type="button" variant="outline" onClick={onCancel}>
            Annuler
          </Button>
        </div>
      </form>
    </DialogContent>
  )
}