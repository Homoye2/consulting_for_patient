"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuration Swagger/OpenAPI
schema_view = get_schema_view(
    openapi.Info(
        title="API Système de Consultation pour Patients - Multi-Tenant",
        default_version='v1.0.0',
        description="""
        # API REST complète pour la gestion d'un système de consultation médicale multi-tenant
        
        ## 🏥 Architecture Multi-Tenant
        
        ### Rôles d'utilisateurs:
        - **Super Admin** (1): Gestion globale du système (hôpitaux, pharmacies, utilisateurs)
        - **Admin Hôpital** (3): Gestion de son propre hôpital et spécialistes
        - **Spécialiste** (12): Gestion des disponibilités, rendez-vous, consultations
        - **Pharmacien** (5): Gestion des stocks, commandes et ventes manuelles
        - **Patient** (50): Accès aux consultations, rendez-vous, commandes
        - **Agent Enregistrement** (5): Saisie des données
        
        ## 🚀 Fonctionnalités principales
        
        ### Gestion Hospitalière:
        - Gestion des hôpitaux avec configuration personnalisée
        - Gestion des spécialités et spécialistes
        - Gestion des disponibilités et créneaux libres
        - Système de rendez-vous avec acceptation/refus
        - Consultations et rapports médicaux
        
        ### Gestion Pharmaceutique:
        - Gestion des produits pharmaceutiques
        - Gestion des stocks avec alertes et expirations
        - Système de commandes pour pharmacies
        - **Ventes manuelles** avec gestion complète des transactions
        - **Revenus combinés** (commandes + ventes manuelles)
        - Statistiques détaillées par période
        
        ### Système de Notifications:
        - Notifications en temps réel
        - Messages personnalisés aux patients
        - Historique des notifications
        
        ### Sécurité et Audit:
        - Gestion des sessions utilisateur
        - Historique des connexions
        - Statistiques de sécurité
        - Authentification JWT sécurisée
        
        ## 🔐 Authentification
        
        ### Endpoints d'authentification:
        - `POST /api/auth/login/` - Connexion générale
        - `POST /api/auth/pharmacy-login/` - Connexion spécialisée pharmacie
        - `POST /api/auth/refresh/` - Rafraîchissement du token
        - `POST /api/auth/change-password/` - Changement de mot de passe
        
        ### Utilisation:
        1. Obtenez un token via `/api/auth/login/` ou `/api/auth/pharmacy-login/`
        2. Incluez le token dans l'en-tête: `Authorization: Bearer <token>`
        
        ## 📊 Statistiques et Revenus
        
        ### Ventes manuelles:
        - `GET /api/ventes/statistiques/` - Statistiques des ventes par période
        - `POST /api/ventes/` - Créer une vente manuelle
        - Support des remises, différents modes de paiement
        
        ### Revenus combinés:
        - `GET /api/ventes/revenus_combines/` - Revenus totaux (ventes + commandes)
        - Calculs automatiques par période
        - Graphiques des ventes par jour
        - Panier moyen et croissance mensuelle
        
        ## 🔍 Filtres et Recherche
        
        ### Paramètres courants:
        - `?periode=ce_mois` - Filtrer par période (aujourd_hui, cette_semaine, ce_mois, cette_annee)
        - `?pharmacie=11` - Filtrer par pharmacie
        - `?statut=en_attente` - Filtrer par statut
        - `?search=terme` - Recherche textuelle
        - `?ordering=-date_creation` - Tri
        - `?page=1&page_size=20` - Pagination
        
        ## 🏪 Comptes de test
        
        ### Pharmacien:
        - Email: `abdou.diouf@pharma.sn`
        - Mot de passe: `pharmacie123`
        - Pharmacie: Pharmacie Centrale
        
        ### Super Admin:
        - Email: `admin@system.sn`
        - Accès complet au système
        
        ## 📱 Applications Frontend
        
        - **Application Patient**: Interface pour les consultations et commandes
        - **Application Pharmacie**: Interface pour la gestion des stocks et ventes
        - **Panel Admin**: Interface d'administration
        
        ## 🔧 Configuration
        
        - **Timezone**: Africa/Dakar
        - **Langue**: Français (fr-fr)
        - **Base de données**: MySQL
        - **Authentification**: JWT avec refresh tokens
        
        ## 📞 Support
        
        Pour toute question technique, contactez l'équipe de développement.
        
        **Version**: 1.0.0 | **Dernière mise à jour**: 7 janvier 2026
        """,
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(
            name="Équipe de développement",
            email="dev@consultation-patients.sn",
            url="https://www.consultation-patients.sn"
        ),
        license=openapi.License(name="Propriétaire - Tous droits réservés"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Documentation Swagger/OpenAPI (doit être AVANT le include pour /api/swagger/)
    re_path(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='api-schema-json'),
    re_path(r'^api/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='api-schema-swagger-ui'),
    re_path(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='api-schema-redoc'),
    
    # Routes API
    path('api/', include('pf.urls')),
    
    # Documentation Swagger/OpenAPI (accessible aussi via /swagger/)
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Servir les fichiers média en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
