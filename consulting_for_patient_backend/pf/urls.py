from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import CustomTokenObtainPairSerializer
from .views import (
    UserViewSet, PatientViewSet, MethodeContraceptiveViewSet,
    RendezVousViewSet, ConsultationPFViewSet, StockItemViewSet,
    PrescriptionViewSet, MouvementStockViewSet,
    StatistiquesView, StatistiquesConsultationsView,
    StatistiquesRendezVousView, StatistiquesStocksView,
    LandingPageContentViewSet, ServiceViewSet, ValueViewSet
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
router.register(r'methodes-contraceptives', MethodeContraceptiveViewSet, basename='methode-contraceptive')
router.register(r'rendez-vous', RendezVousViewSet, basename='rendez-vous')
router.register(r'consultations', ConsultationPFViewSet, basename='consultation')
router.register(r'stocks', StockItemViewSet, basename='stock')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')
router.register(r'mouvements-stock', MouvementStockViewSet, basename='mouvement-stock')
router.register(r'landing-page', LandingPageContentViewSet, basename='landing-page')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'values', ValueViewSet, basename='value')

urlpatterns = [
    # Authentification JWT
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # APIs CRUD
    path('', include(router.urls)),
    
    # APIs Statistiques
    path('statistiques/', StatistiquesView.as_view(), name='statistiques'),
    path('statistiques/consultations/', StatistiquesConsultationsView.as_view(), name='statistiques-consultations'),
    path('statistiques/rendez-vous/', StatistiquesRendezVousView.as_view(), name='statistiques-rendez-vous'),
    path('statistiques/stocks/', StatistiquesStocksView.as_view(), name='statistiques-stocks'),
]

