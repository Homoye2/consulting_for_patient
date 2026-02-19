from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import CustomTokenObtainPairSerializer
from .google_auth import google_auth
from .views import (
    UserViewSet, PatientViewSet,
    RendezVousViewSet, ConsultationPFViewSet,
    StatistiquesView, StatistiquesConsultationsView,
    StatistiquesRendezVousView, StatistiquesStocksView,
    AnalyticsDashboardView,
    LandingPageContentViewSet, ServiceViewSet, ValueViewSet,
    ContactMessageViewSet, PharmacieViewSet,
    SpecialiteViewSet, SpecialisteViewSet,
    DisponibiliteSpecialisteViewSet, ProduitViewSet, StockProduitViewSet,
    CommandePharmacieViewSet, NotificationViewSet,
    RapportConsultationViewSet, AvisSpecialisteViewSet,
    PharmacyTokenObtainPairView, HospitalTokenObtainPairView, SessionUtilisateurViewSet,
    HistoriqueConnexionViewSet
)
from .admin_views import (
    SystemHealthView, RecentActivityView, SystemAlertsView,
    SecurityStatsView, SecurityAlertsView, LoginAttemptsView,
    BroadcastNotificationView
)
from .new_views import (
    HopitalViewSet, VentePharmacieViewSet, LigneVenteViewSet, 
    EmployePharmacieViewSet, RegistreViewSet, OrdonnanceViewSet, 
    LigneOrdonnanceViewSet, DossierMedicalViewSet, FichierDossierMedicalViewSet,
    FournisseurViewSet, FactureFournisseurViewSet
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    @swagger_auto_schema(
        operation_description="Authentification JWT - Obtenir un token d'accès",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description="Email de l'utilisateur"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description="Mot de passe"),
            }
        ),
        responses={
            200: openapi.Response(
                description="Token d'accès et informations utilisateur",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description="Token d'accès JWT"),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description="Token de rafraîchissement"),
                        'user': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                                'nom': openapi.Schema(type=openapi.TYPE_STRING),
                                'role': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        ),
                    }
                )
            ),
            401: openapi.Response(description="Identifiants invalides")
        },
        tags=['Authentification']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'rendez-vous', RendezVousViewSet, basename='rendez-vous')
router.register(r'consultations', ConsultationPFViewSet, basename='consultation')
router.register(r'landing-page', LandingPageContentViewSet, basename='landing-page')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'values', ValueViewSet, basename='value')
router.register(r'contact-messages', ContactMessageViewSet, basename='contact-message')
router.register(r'pharmacies', PharmacieViewSet, basename='pharmacie')

# Nouvelles routes pour la nouvelle architecture
router.register(r'hopitaux', HopitalViewSet, basename='hopital')
router.register(r'specialites', SpecialiteViewSet, basename='specialite')
router.register(r'specialistes', SpecialisteViewSet, basename='specialiste')
router.register(r'disponibilites', DisponibiliteSpecialisteViewSet, basename='disponibilite')
router.register(r'produits', ProduitViewSet, basename='produit')
router.register(r'stocks-produits', StockProduitViewSet, basename='stock-produit')
router.register(r'commandes', CommandePharmacieViewSet, basename='commande')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'rapports-consultations', RapportConsultationViewSet, basename='rapport-consultation')
router.register(r'avis-specialistes', AvisSpecialisteViewSet, basename='avis-specialiste')
router.register(r'sessions', SessionUtilisateurViewSet, basename='session')
router.register(r'historique-connexions', HistoriqueConnexionViewSet, basename='historique-connexion')
router.register(r'ventes', VentePharmacieViewSet, basename='vente')
router.register(r'lignes-ventes', LigneVenteViewSet, basename='ligne-vente')
router.register(r'employes', EmployePharmacieViewSet, basename='employe')
router.register(r'registres', RegistreViewSet, basename='registre')
router.register(r'ordonnances', OrdonnanceViewSet, basename='ordonnance')
router.register(r'lignes-ordonnances', LigneOrdonnanceViewSet, basename='ligne-ordonnance')
router.register(r'dossiers-medicaux', DossierMedicalViewSet, basename='dossier-medical')
router.register(r'fichiers-dossiers-medicaux', FichierDossierMedicalViewSet, basename='fichier-dossier-medical')
router.register(r'fournisseurs', FournisseurViewSet, basename='fournisseur')
router.register(r'factures-fournisseurs', FactureFournisseurViewSet, basename='facture-fournisseur')

urlpatterns = [
    # Authentification JWT
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/pharmacy-login/', PharmacyTokenObtainPairView.as_view(), name='pharmacy_token_obtain_pair'),
    path('auth/hospital-login/', HospitalTokenObtainPairView.as_view(), name='hospital_token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/change-password/', UserViewSet.as_view({'post': 'change_password'}), name='change_password'),
    path('auth/google/', google_auth, name='google_auth'),
    
    # APIs CRUD
    path('', include(router.urls)),
    
    # Endpoints publics spécifiques
    path('landing-page/public/', LandingPageContentViewSet.as_view({'get': 'public'}), name='landing-page-public'),
    path('services/public/', ServiceViewSet.as_view({'get': 'public'}), name='services-public'),
    path('values/public/', ValueViewSet.as_view({'get': 'public'}), name='values-public'),
    
    # APIs Statistiques
    path('statistiques/', StatistiquesView.as_view(), name='statistiques'),
    path('statistiques/consultations/', StatistiquesConsultationsView.as_view(), name='statistiques-consultations'),
    path('statistiques/rendez-vous/', StatistiquesRendezVousView.as_view(), name='statistiques-rendez-vous'),
    path('statistiques/stocks/', StatistiquesStocksView.as_view(), name='statistiques-stocks'),
    path('analytics/dashboard/', AnalyticsDashboardView.as_view(), name='analytics-dashboard'),
    
    # APIs Admin Dashboard
    path('admin/system-health/', SystemHealthView.as_view(), name='admin-system-health'),
    path('admin/recent-activity/', RecentActivityView.as_view(), name='admin-recent-activity'),
    path('admin/system-alerts/', SystemAlertsView.as_view(), name='admin-system-alerts'),
    path('admin/security-stats/', SecurityStatsView.as_view(), name='admin-security-stats'),
    path('admin/security-alerts/', SecurityAlertsView.as_view(), name='admin-security-alerts'),
    path('admin/login-attempts/', LoginAttemptsView.as_view(), name='admin-login-attempts'),
    path('admin/broadcast-notification/', BroadcastNotificationView.as_view(), name='admin-broadcast-notification'),
]

