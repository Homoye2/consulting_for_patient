# 📋 Améliorations Dossiers Médicaux - Fichiers Joints

## 🎯 Objectif

Ajouter la possibilité de joindre des fichiers aux dossiers médicaux dans e-sora-hopital.

---

## ✅ Modifications Backend

### 1. Nouveau Modèle: FichierDossierMedical

**Fichier**: `consulting_for_patient_backend/pf/models.py`

```python
class FichierDossierMedical(models.Model):
    """Modèle pour les fichiers joints aux dossiers médicaux"""
    
    TYPE_FICHIER_CHOICES = [
        ('gyneco_obstetricaux', 'Gynéco-Obstétricaux'),
        ('chirurgicaux', 'Chirurgicaux'),
        ('examen_general', 'Examen général'),
        ('examen_physique', 'Examen physique'),
        ('hypothese_diagnostic', 'Hypothèse diagnostic'),
        ('diagnostic', 'Diagnostic'),
        ('biologie', 'Biologie'),
        ('imagerie', 'Imagerie'),
        ('autre', 'Autre'),
    ]
    
    dossier_medical = ForeignKey(DossierMedical, related_name='fichiers')
    type_fichier = CharField(max_length=50, choices=TYPE_FICHIER_CHOICES)
    fichier = FileField(upload_to='dossiers_medicaux/%Y/%m/%d/')
    nom_fichier = CharField(max_length=255)
    description = TextField(blank=True, null=True)
    taille_fichier = IntegerField(null=True, blank=True)
    type_mime = CharField(max_length=100, blank=True, null=True)
```

### 2. Nouveaux Serializers

**Fichier**: `consulting_for_patient_backend/pf/serializers.py`

- `FichierDossierMedicalSerializer` - Pour lire les fichiers
- `FichierDossierMedicalCreateSerializer` - Pour créer des fichiers
- `DossierMedicalDetailSerializer` - Dossier avec fichiers inclus

### 3. Migration à Créer

```bash
cd consulting_for_patient_backend
python manage.py makemigrations
python manage.py migrate
```

---

## 📁 Structure des Fichiers

### Stockage

Les fichiers seront stockés dans:
```
media/dossiers_medicaux/YYYY/MM/DD/
```

Exemple:
```
media/dossiers_medicaux/2026/02/12/examen_biologie_123.pdf
```

### Types de Fichiers Supportés

- **Gynéco-Obstétricaux**: Examens gynécologiques, échographies
- **Chirurgicaux**: Comptes-rendus opératoires, radiographies
- **Examen général**: Résultats d'examens généraux
- **Examen physique**: Photos, schémas
- **Hypothèse diagnostic**: Documents de diagnostic préliminaire
- **Diagnostic**: Rapports de diagnostic final
- **Biologie**: Analyses de sang, urines, etc.
- **Imagerie**: IRM, Scanner, Radiographies
- **Autre**: Autres documents

---

## 🔌 API Endpoints

### Dossiers Médicaux

```
GET    /api/dossiers-medicaux/              # Liste des dossiers
POST   /api/dossiers-medicaux/              # Créer un dossier
GET    /api/dossiers-medicaux/{id}/         # Détails (avec fichiers)
PUT    /api/dossiers-medicaux/{id}/         # Modifier
DELETE /api/dossiers-medicaux/{id}/         # Supprimer
POST   /api/dossiers-medicaux/{id}/upload_fichier/  # Ajouter un fichier
```

### Fichiers

```
GET    /api/fichiers-dossiers-medicaux/                    # Liste des fichiers
POST   /api/fichiers-dossiers-medicaux/                    # Créer un fichier
GET    /api/fichiers-dossiers-medicaux/{id}/               # Détails
DELETE /api/fichiers-dossiers-medicaux/{id}/               # Supprimer
GET    /api/fichiers-dossiers-medicaux/{id}/download/      # Télécharger
```

---

## 📤 Upload de Fichiers

### Format de la Requête

```javascript
// FormData pour l'upload
const formData = new FormData()
formData.append('dossier_medical', dossier_id)
formData.append('type_fichier', 'biologie')
formData.append('fichier', file)
formData.append('nom_fichier', file.name)
formData.append('description', 'Analyse de sang du 12/02/2026')

// Requête
await api.post('/fichiers-dossiers-medicaux/', formData, {
  headers: {
    'Content-Type': 'multipart/form-data'
  }
})
```

### Réponse

```json
{
  "id": 1,
  "dossier_medical": 123,
  "type_fichier": "biologie",
  "type_fichier_display": "Biologie",
  "fichier": "/media/dossiers_medicaux/2026/02/12/analyse_sang.pdf",
  "fichier_url": "http://localhost:8000/media/dossiers_medicaux/2026/02/12/analyse_sang.pdf",
  "nom_fichier": "analyse_sang.pdf",
  "description": "Analyse de sang du 12/02/2026",
  "taille_fichier": 245678,
  "taille_fichier_display": "240.0 Ko",
  "type_mime": "application/pdf",
  "created_at": "2026-02-12T10:30:00Z"
}
```

---

## 🎨 Frontend - e-sora-hopital

### 1. Formulaire de Création

Ajouter des champs d'upload pour chaque section:

```typescript
// État pour les fichiers
const [fichiers, setFichiers] = useState<{
  gyneco_obstetricaux: File[],
  chirurgicaux: File[],
  examen_general: File[],
  examen_physique: File[],
  hypothese_diagnostic: File[],
  diagnostic: File[],
  biologie: File[],
  imagerie: File[]
}>({
  gyneco_obstetricaux: [],
  chirurgicaux: [],
  examen_general: [],
  examen_physique: [],
  hypothese_diagnostic: [],
  diagnostic: [],
  biologie: [],
  imagerie: []
})

// Composant d'upload
<div>
  <Label>Gynéco-Obstétricaux</Label>
  <Textarea value={formData.gyneco_obstetricaux} ... />
  
  <div className="mt-2">
    <Label>Fichiers joints</Label>
    <Input
      type="file"
      multiple
      accept=".pdf,.jpg,.jpeg,.png,.doc,.docx"
      onChange={(e) => handleFileChange('gyneco_obstetricaux', e.target.files)}
    />
    {fichiers.gyneco_obstetricaux.length > 0 && (
      <div className="mt-2">
        {fichiers.gyneco_obstetricaux.map((file, index) => (
          <div key={index} className="flex items-center gap-2">
            <FileIcon className="h-4 w-4" />
            <span className="text-sm">{file.name}</span>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => removeFile('gyneco_obstetricaux', index)}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        ))}
      </div>
    )}
  </div>
</div>
```

### 2. Soumission du Formulaire

```typescript
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault()
  
  try {
    // 1. Créer le dossier médical
    const response = await dossiersMedicauxService.create(formData)
    const dossierId = response.data.id
    
    // 2. Upload des fichiers
    for (const [type, files] of Object.entries(fichiers)) {
      for (const file of files) {
        const formData = new FormData()
        formData.append('dossier_medical', dossierId)
        formData.append('type_fichier', type)
        formData.append('fichier', file)
        formData.append('nom_fichier', file.name)
        
        await fichiersDossiersMedicauxService.create(formData)
      }
    }
    
    showToast('Dossier médical créé avec succès', 'success')
    fetchDossiers()
    setDialogOpen(false)
  } catch (error) {
    console.error('Erreur:', error)
    showToast('Erreur lors de la création', 'error')
  }
}
```

### 3. Modal de Détails

```typescript
<Dialog open={showDetailsModal} onOpenChange={setShowDetailsModal}>
  <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
    <DialogHeader>
      <DialogTitle>Détails du Dossier Médical</DialogTitle>
    </DialogHeader>
    
    {selectedDossier && (
      <div className="space-y-6">
        {/* Informations générales */}
        <div>
          <h3 className="font-semibold">Patient</h3>
          <p>{selectedDossier.patient_nom} {selectedDossier.patient_prenom}</p>
        </div>
        
        {/* Gynéco-Obstétricaux */}
        <div>
          <h3 className="font-semibold">Gynéco-Obstétricaux</h3>
          <p>{selectedDossier.gyneco_obstetricaux}</p>
          
          {selectedDossier.fichiers_par_type?.gyneco_obstetricaux && (
            <div className="mt-2 space-y-2">
              <Label>Fichiers joints:</Label>
              {selectedDossier.fichiers_par_type.gyneco_obstetricaux.map((fichier) => (
                <div key={fichier.id} className="flex items-center gap-2 p-2 border rounded">
                  <FileIcon className="h-4 w-4" />
                  <div className="flex-1">
                    <p className="text-sm font-medium">{fichier.nom_fichier}</p>
                    <p className="text-xs text-muted-foreground">
                      {fichier.taille_fichier_display}
                    </p>
                  </div>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => window.open(fichier.fichier_url, '_blank')}
                  >
                    <Download className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          )}
        </div>
        
        {/* Répéter pour chaque section... */}
      </div>
    )}
  </DialogContent>
</Dialog>
```

---

## 🔧 Configuration Django

### settings.py

Ajouter la configuration pour les fichiers media:

```python
# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Taille maximale des fichiers (10 MB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB
```

### urls.py

Ajouter le serving des fichiers media en développement:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... vos URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 📊 Exemple Complet

### Créer un Dossier avec Fichiers

```typescript
// 1. Préparer les données du dossier
const dossierData = {
  registre: 123,
  motif_consultation: "Consultation de suivi",
  histoire_maladie: "Patient présente...",
  gyneco_obstetricaux: "G2P2, dernière grossesse en 2024",
  biologie: "Analyses demandées: NFS, CRP",
  imagerie: "Échographie abdominale prescrite"
}

// 2. Créer le dossier
const response = await api.post('/dossiers-medicaux/', dossierData)
const dossierId = response.data.id

// 3. Upload des fichiers
const files = {
  gyneco_obstetricaux: [file1, file2],
  biologie: [file3],
  imagerie: [file4]
}

for (const [type, fileList] of Object.entries(files)) {
  for (const file of fileList) {
    const formData = new FormData()
    formData.append('dossier_medical', dossierId)
    formData.append('type_fichier', type)
    formData.append('fichier', file)
    formData.append('nom_fichier', file.name)
    
    await api.post('/fichiers-dossiers-medicaux/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}
```

---

## ✅ Checklist d'Implémentation

### Backend
- [x] Créer le modèle `FichierDossierMedical`
- [x] Créer les serializers
- [ ] Créer les vues (ViewSet)
- [ ] Ajouter les URLs
- [ ] Créer la migration
- [ ] Appliquer la migration
- [ ] Tester les endpoints

### Frontend
- [ ] Ajouter les champs d'upload dans le formulaire
- [ ] Implémenter la gestion des fichiers (state)
- [ ] Implémenter l'upload lors de la création
- [ ] Afficher les fichiers dans le modal de détails
- [ ] Ajouter le téléchargement des fichiers
- [ ] Ajouter la suppression des fichiers
- [ ] Tester l'interface

---

## 🎯 Prochaines Étapes

1. **Créer la migration**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Créer les vues et URLs** (à faire)

3. **Tester l'API** avec Postman ou curl

4. **Implémenter le frontend** dans e-sora-hopital

5. **Tester l'upload et l'affichage** des fichiers
