from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Patient, RendezVous,
    ConsultationPF, LandingPageContent, Service, Value, ContactMessage, Pharmacie,
    Hopital, Specialite, Specialiste, DisponibiliteSpecialiste,
    Produit, StockProduit, CommandePharmacie, LigneCommande,
    Notification, RapportConsultation, AvisSpecialiste
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin pour le modèle User personnalisé"""
    list_display = ['email', 'nom', 'role', 'actif', 'is_staff', 'date_joined']
    list_filter = ['role', 'actif', 'is_staff', 'is_superuser']
    search_fields = ['email', 'nom']
    ordering = ['email']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('nom', 'role')}),
        ('Permissions', {'fields': ('actif', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom', 'role', 'password1', 'password2', 'actif', 'is_staff', 'is_superuser'),
        }),
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """Admin pour le modèle Patient"""
    list_display = ['nom', 'prenom', 'dob', 'sexe', 'telephone', 'created_at']
    list_filter = ['sexe', 'created_at']
    search_fields = ['nom', 'prenom', 'telephone']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    """Admin pour le modèle RendezVous"""
    list_display = ['patient', 'specialiste', 'hopital', 'datetime', 'statut', 'created_at']
    list_filter = ['statut', 'datetime', 'hopital', 'specialiste__specialite']
    search_fields = ['patient__nom', 'patient__prenom', 'notes', 'specialiste__user__nom']
    date_hierarchy = 'datetime'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ConsultationPF)
class ConsultationPFAdmin(admin.ModelAdmin):
    """Admin pour le modèle ConsultationPF"""
    list_display = ['patient', 'specialiste', 'hopital', 'date', 'methode_posee', 'created_at']
    list_filter = ['date', 'methode_posee', 'hopital', 'specialiste__specialite']
    search_fields = ['patient__nom', 'patient__prenom', 'notes', 'anamnese', 'specialiste__user__nom']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Pharmacie)
class PharmacieAdmin(admin.ModelAdmin):
    """Admin pour le modèle Pharmacie"""
    list_display = ['nom', 'user', 'telephone', 'actif', 'created_at']
    list_filter = ['actif', 'created_at']
    search_fields = ['nom', 'adresse', 'telephone', 'email', 'user__nom', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


class ServiceInline(admin.TabularInline):
    """Inline pour les services dans l'admin"""
    model = Service
    extra = 1


class ValueInline(admin.TabularInline):
    """Inline pour les valeurs dans l'admin"""
    model = Value
    extra = 1


@admin.register(LandingPageContent)
class LandingPageContentAdmin(admin.ModelAdmin):
    """Admin pour le modèle LandingPageContent"""
    inlines = [ServiceInline, ValueInline]
    list_display = ['logo_text', 'hero_title', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Header', {
            'fields': ('logo_text',)
        }),
        ('Section Hero', {
            'fields': ('hero_title', 'hero_description', 'hero_button_primary', 'hero_button_secondary')
        }),
        ('Section À propos', {
            'fields': (
                'about_title', 'about_description_1', 'about_description_2',
                'about_stat_1_value', 'about_stat_1_label',
                'about_stat_2_value', 'about_stat_2_label'
            )
        }),
        ('Section Services', {
            'fields': ('services_title', 'services_subtitle')
        }),
        ('Section Valeurs', {
            'fields': ('values_title', 'values_subtitle')
        }),
        ('Footer', {
            'fields': (
                'footer_about_text', 'footer_address', 'footer_phone', 'footer_email',
                'footer_facebook', 'footer_twitter', 'footer_instagram', 'footer_linkedin'
            )
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Ne permettre qu'une seule instance
        return not LandingPageContent.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Empêcher la suppression
        return False


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin pour le modèle ContactMessage"""
    list_display = ['nom', 'email', 'sujet', 'patient', 'lu', 'date_creation']
    list_filter = ['lu', 'date_creation']
    search_fields = ['nom', 'email', 'sujet', 'message']
    readonly_fields = ['date_creation']
    date_hierarchy = 'date_creation'
    
    def mark_as_read(self, request, queryset):
        queryset.update(lu=True)
    mark_as_read.short_description = "Marquer comme lu"
    
    actions = [mark_as_read]


# Admin pour les nouveaux modèles

@admin.register(Hopital)
class HopitalAdmin(admin.ModelAdmin):
    """Admin pour le modèle Hopital"""
    list_display = ['nom', 'code_hopital', 'ville', 'admin_hopital', 'actif', 'created_at']
    list_filter = ['actif', 'ville', 'pays', 'created_at']
    search_fields = ['nom', 'code_hopital', 'ville', 'email', 'telephone']
    readonly_fields = ['created_at', 'updated_at', 'date_inscription']
    date_hierarchy = 'created_at'


@admin.register(Specialite)
class SpecialiteAdmin(admin.ModelAdmin):
    """Admin pour le modèle Specialite"""
    list_display = ['nom', 'code', 'actif', 'created_at']
    list_filter = ['actif']
    search_fields = ['nom', 'code', 'description']


@admin.register(Specialiste)
class SpecialisteAdmin(admin.ModelAdmin):
    """Admin pour le modèle Specialiste"""
    list_display = ['user', 'hopital', 'specialite', 'titre', 'numero_ordre', 'actif', 'note_moyenne']
    list_filter = ['actif', 'hopital', 'specialite', 'consultation_en_ligne']
    search_fields = ['user__nom', 'user__email', 'numero_ordre', 'titre']
    readonly_fields = ['created_at', 'updated_at', 'note_moyenne', 'nombre_avis']


@admin.register(DisponibiliteSpecialiste)
class DisponibiliteSpecialisteAdmin(admin.ModelAdmin):
    """Admin pour le modèle DisponibiliteSpecialiste"""
    list_display = ['specialiste', 'jour_semaine', 'heure_debut', 'heure_fin', 'actif']
    list_filter = ['jour_semaine', 'actif', 'specialiste__hopital']
    search_fields = ['specialiste__user__nom']


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    """Admin pour le modèle Produit"""
    list_display = ['nom', 'code_barre', 'categorie', 'prix_unitaire', 'prescription_requise', 'actif']
    list_filter = ['categorie', 'prescription_requise', 'actif', 'created_at']
    search_fields = ['nom', 'code_barre', 'fabricant', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(StockProduit)
class StockProduitAdmin(admin.ModelAdmin):
    """Admin pour le modèle StockProduit"""
    list_display = ['pharmacie', 'produit', 'quantite', 'seuil_alerte', 'prix_vente', 'date_expiration']
    list_filter = ['pharmacie', 'produit__categorie', 'date_expiration']
    search_fields = ['produit__nom', 'pharmacie__nom', 'numero_lot']
    readonly_fields = ['created_at', 'updated_at']


class LigneCommandeInline(admin.TabularInline):
    """Inline pour les lignes de commande"""
    model = LigneCommande
    extra = 1
    readonly_fields = ['prix_total']


@admin.register(CommandePharmacie)
class CommandePharmacieAdmin(admin.ModelAdmin):
    """Admin pour le modèle CommandePharmacie"""
    inlines = [LigneCommandeInline]
    list_display = ['numero_commande', 'patient', 'pharmacie', 'statut', 'montant_total', 'date_commande']
    list_filter = ['statut', 'date_commande', 'pharmacie']
    search_fields = ['numero_commande', 'patient__nom', 'patient__prenom', 'pharmacie__nom']
    readonly_fields = ['numero_commande', 'date_commande', 'created_at', 'updated_at']
    date_hierarchy = 'date_commande'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin pour le modèle Notification"""
    list_display = ['user', 'type_notification', 'titre', 'lu', 'created_at']
    list_filter = ['type_notification', 'lu', 'created_at']
    search_fields = ['user__nom', 'titre', 'message']
    readonly_fields = ['created_at', 'date_lecture']
    date_hierarchy = 'created_at'


@admin.register(RapportConsultation)
class RapportConsultationAdmin(admin.ModelAdmin):
    """Admin pour le modèle RapportConsultation"""
    list_display = ['consultation', 'suivi_necessaire', 'envoye_patient', 'date_envoi', 'created_at']
    list_filter = ['suivi_necessaire', 'envoye_patient', 'created_at']
    search_fields = ['consultation__patient__nom', 'diagnostic']
    readonly_fields = ['created_at', 'updated_at', 'date_envoi']


@admin.register(AvisSpecialiste)
class AvisSpecialisteAdmin(admin.ModelAdmin):
    """Admin pour le modèle AvisSpecialiste"""
    list_display = ['specialiste', 'patient', 'note', 'recommande', 'created_at']
    list_filter = ['note', 'recommande', 'created_at']
    search_fields = ['specialiste__user__nom', 'patient__nom', 'commentaire']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
