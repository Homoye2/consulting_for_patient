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
        title="API de Gestion de Planification Familiale",
        default_version='v1',
        description="""
        API REST complète pour la gestion de la planification familiale au Centre Hospitalier Abass Ndao.
        
        ## Fonctionnalités principales:
        - Gestion des patients et consultations PF
        - Gestion des rendez-vous et agenda
        - Gestion des stocks de méthodes contraceptives
        - Statistiques et rapports
        
        ## Authentification:
        Toutes les APIs nécessitent une authentification JWT. 
        Utilisez `/api/auth/login/` pour obtenir un token d'accès.
        
        ## Permissions:
        Les permissions sont basées sur les rôles des utilisateurs:
        - **Administrateur**: Accès complet
        - **Médecin/Sage-femme/Infirmier**: Gestion patients, consultations, rendez-vous
        - **Pharmacien**: Gestion des stocks
        - **Agent d'enregistrement**: Gestion des rendez-vous
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Propriétaire"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('pf.urls')),
    
    # Documentation Swagger/OpenAPI
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Servir les fichiers média en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
