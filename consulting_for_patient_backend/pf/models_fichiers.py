"""
Modèles pour les fichiers joints aux dossiers médicaux
"""
from django.db import models
from .models import DossierMedical


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
    
    id = models.BigAutoField(primary_key=True)
    
    # Liaison avec le dossier médical
    dossier_medical = models.ForeignKey(
        DossierMedical,
        on_delete=models.CASCADE,
        related_name='fichiers',
        verbose_name='Dossier médical'
    )
    
    # Type de fichier
    type_fichier = models.CharField(
        max_length=50,
        choices=TYPE_FICHIER_CHOICES,
        verbose_name='Type de fichier'
    )
    
    # Fichier
    fichier = models.FileField(
        upload_to='dossiers_medicaux/%Y/%m/%d/',
        verbose_name='Fichier'
    )
    
    # Nom original du fichier
    nom_fichier = models.CharField(
        max_length=255,
        verbose_name='Nom du fichier'
    )
    
    # Description optionnelle
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description'
    )
    
    # Métadonnées
    taille_fichier = models.IntegerField(
        verbose_name='Taille du fichier (octets)',
        null=True,
        blank=True
    )
    
    type_mime = models.CharField(
        max_length=100,
        verbose_name='Type MIME',
        blank=True,
        null=True
    )
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'fichiers_dossiers_medicaux'
        verbose_name = 'Fichier de dossier médical'
        verbose_name_plural = 'Fichiers de dossiers médicaux'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['dossier_medical', 'type_fichier']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.nom_fichier} ({self.get_type_fichier_display()})"
    
    def save(self, *args, **kwargs):
        # Extraire le nom du fichier si pas fourni
        if not self.nom_fichier and self.fichier:
            self.nom_fichier = self.fichier.name
        
        # Extraire la taille du fichier
        if self.fichier and not self.taille_fichier:
            self.taille_fichier = self.fichier.size
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Supprimer le fichier physique
        if self.fichier:
            self.fichier.delete(save=False)
        super().delete(*args, **kwargs)
