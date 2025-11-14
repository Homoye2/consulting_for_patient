from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Patient, MethodeContraceptive, RendezVous,
    ConsultationPF, StockItem, Prescription, MouvementStock,
    LandingPageContent, Service, Value, ContactMessage
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


@admin.register(MethodeContraceptive)
class MethodeContraceptiveAdmin(admin.ModelAdmin):
    """Admin pour le modèle MethodeContraceptive"""
    list_display = ['nom', 'categorie', 'created_at']
    list_filter = ['categorie']
    search_fields = ['nom', 'description']


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    """Admin pour le modèle RendezVous"""
    list_display = ['patient', 'user', 'datetime', 'statut', 'created_at']
    list_filter = ['statut', 'datetime', 'user']
    search_fields = ['patient__nom', 'patient__prenom', 'notes']
    date_hierarchy = 'datetime'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ConsultationPF)
class ConsultationPFAdmin(admin.ModelAdmin):
    """Admin pour le modèle ConsultationPF"""
    list_display = ['patient', 'user', 'date', 'methode_prescite', 'methode_posee', 'created_at']
    list_filter = ['date', 'methode_posee', 'user', 'methode_prescite']
    search_fields = ['patient__nom', 'patient__prenom', 'notes', 'anamnese']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    """Admin pour le modèle StockItem"""
    list_display = ['methode', 'quantite', 'seuil', 'est_en_rupture', 'est_sous_seuil']
    list_filter = ['methode__categorie']
    search_fields = ['methode__nom']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    """Admin pour le modèle Prescription"""
    list_display = ['consultation', 'methode', 'dosage', 'date_prescription']
    list_filter = ['date_prescription', 'methode']
    search_fields = ['consultation__patient__nom', 'methode__nom']


@admin.register(MouvementStock)
class MouvementStockAdmin(admin.ModelAdmin):
    """Admin pour le modèle MouvementStock"""
    list_display = ['stock_item', 'type_mouvement', 'quantite', 'user', 'date_mouvement']
    list_filter = ['type_mouvement', 'date_mouvement']
    search_fields = ['stock_item__methode__nom', 'motif']
    readonly_fields = ['date_mouvement']
    date_hierarchy = 'date_mouvement'


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
