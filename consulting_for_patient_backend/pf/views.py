from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Sum, F
from django.utils import timezone
from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import (
    User, Patient, MethodeContraceptive, RendezVous,
    ConsultationPF, StockItem, Prescription, MouvementStock,
    LandingPageContent, Service, Value
)
from .serializers import (
    UserSerializer, UserCreateSerializer, PatientSerializer, PatientListSerializer,
    MethodeContraceptiveSerializer, RendezVousSerializer, ConsultationPFSerializer,
    ConsultationPFListSerializer, StockItemSerializer, PrescriptionSerializer,
    MouvementStockSerializer, MouvementStockCreateSerializer,
    LandingPageContentSerializer, LandingPageContentUpdateSerializer,
    ServiceSerializer, ValueSerializer
)
from .permissions import (
    IsAdminOrReadOnly, IsAdminOrMedicalStaff, IsAdminOrPharmacist,
    IsAdminOrReception, CanManageUsers, CanManageStock, CanManageConsultations,
    CanManageAppointments
)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des utilisateurs"""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, CanManageUsers]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'email']
    ordering_fields = ['nom', 'email', 'date_joined']
    ordering = ['nom']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Retourne les informations de l'utilisateur connecté"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activer un utilisateur"""
        user = self.get_object()
        user.actif = True
        user.save()
        return Response({'status': 'Utilisateur activé'})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Désactiver un utilisateur"""
        user = self.get_object()
        user.actif = False
        user.save()
        return Response({'status': 'Utilisateur désactivé'})


class PatientViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des patients"""
    queryset = Patient.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrMedicalStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sexe']
    search_fields = ['nom', 'prenom', 'telephone']
    ordering_fields = ['nom', 'prenom', 'dob', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PatientListSerializer
        return PatientSerializer
    
    @action(detail=True, methods=['get'])
    def consultations(self, request, pk=None):
        """Récupère toutes les consultations d'un patient"""
        patient = self.get_object()
        consultations = ConsultationPF.objects.filter(patient=patient).order_by('-date')
        serializer = ConsultationPFListSerializer(consultations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def rendez_vous(self, request, pk=None):
        """Récupère tous les rendez-vous d'un patient"""
        patient = self.get_object()
        rendez_vous = RendezVous.objects.filter(patient=patient).order_by('-datetime')
        serializer = RendezVousSerializer(rendez_vous, many=True)
        return Response(serializer.data)


class MethodeContraceptiveViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des méthodes contraceptives"""
    queryset = MethodeContraceptive.objects.all()
    serializer_class = MethodeContraceptiveSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categorie']
    search_fields = ['nom', 'description']
    ordering_fields = ['nom', 'categorie']
    ordering = ['nom']


class RendezVousViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des rendez-vous"""
    queryset = RendezVous.objects.all()
    serializer_class = RendezVousSerializer
    permission_classes = [IsAuthenticated, CanManageAppointments]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['statut', 'patient', 'user']
    search_fields = ['patient__nom', 'patient__prenom', 'notes']
    ordering_fields = ['datetime', 'created_at']
    ordering = ['-datetime']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtre par date
        date_debut = self.request.query_params.get('date_debut', None)
        date_fin = self.request.query_params.get('date_fin', None)
        
        if date_debut:
            queryset = queryset.filter(datetime__gte=date_debut)
        if date_fin:
            queryset = queryset.filter(datetime__lte=date_fin)
        
        # Si l'utilisateur n'est pas admin, voir seulement ses rendez-vous ou ceux de ses patients
        if self.request.user.role != 'administrateur':
            if self.request.user.role in ['medecin', 'sage_femme', 'infirmier']:
                queryset = queryset.filter(user=self.request.user)
        
        return queryset
    
    @swagger_auto_schema(
        method='get',
        operation_description="Récupère l'agenda d'un professionnel de santé pour une date donnée",
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY, description="ID du professionnel", type=openapi.TYPE_INTEGER),
            openapi.Parameter('date', openapi.IN_QUERY, description="Date (format: YYYY-MM-DD)", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
        ],
        responses={200: RendezVousSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def agenda(self, request):
        """Récupère l'agenda d'un professionnel"""
        user_id = request.query_params.get('user_id', None)
        date = request.query_params.get('date', None)
        
        queryset = self.get_queryset()
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        elif request.user.role != 'administrateur':
            queryset = queryset.filter(user=request.user)
        
        if date:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            queryset = queryset.filter(datetime__date=date_obj)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def confirmer(self, request, pk=None):
        """Confirmer un rendez-vous"""
        rendez_vous = self.get_object()
        rendez_vous.statut = 'confirme'
        rendez_vous.save()
        return Response({'status': 'Rendez-vous confirmé'})
    
    @action(detail=True, methods=['post'])
    def annuler(self, request, pk=None):
        """Annuler un rendez-vous"""
        rendez_vous = self.get_object()
        rendez_vous.statut = 'annule'
        rendez_vous.save()
        return Response({'status': 'Rendez-vous annulé'})


class ConsultationPFViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des consultations PF"""
    queryset = ConsultationPF.objects.all()
    permission_classes = [IsAuthenticated, CanManageConsultations]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['patient', 'user', 'methode_prescite', 'methode_posee']
    search_fields = ['patient__nom', 'patient__prenom', 'notes', 'anamnese']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ConsultationPFListSerializer
        return ConsultationPFSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtre par date
        date_debut = self.request.query_params.get('date_debut', None)
        date_fin = self.request.query_params.get('date_fin', None)
        
        if date_debut:
            queryset = queryset.filter(date__gte=date_debut)
        if date_fin:
            queryset = queryset.filter(date__lte=date_fin)
        
        # Si l'utilisateur n'est pas admin, voir seulement ses consultations
        if self.request.user.role != 'administrateur':
            queryset = queryset.filter(user=self.request.user)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def prescriptions(self, request, pk=None):
        """Récupère les prescriptions d'une consultation"""
        consultation = self.get_object()
        prescriptions = Prescription.objects.filter(consultation=consultation)
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data)


class StockItemViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des stocks"""
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer
    permission_classes = [IsAuthenticated, CanManageStock]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['methode']
    search_fields = ['methode__nom']
    ordering_fields = ['quantite', 'methode__nom']
    ordering = ['methode__nom']
    
    @swagger_auto_schema(
        method='get',
        operation_description="Récupère tous les stocks en alerte (quantité sous le seuil d'alerte)",
        responses={200: StockItemSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def alertes(self, request):
        """Récupère les stocks en alerte (sous seuil ou en rupture)"""
        stocks = StockItem.objects.filter(
            Q(quantite__lte=F('seuil'))
        )
        serializer = self.get_serializer(stocks, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        method='get',
        operation_description="Récupère tous les stocks en rupture (quantité = 0)",
        responses={200: StockItemSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def ruptures(self, request):
        """Récupère les stocks en rupture"""
        stocks = StockItem.objects.filter(quantite__lte=0)
        serializer = self.get_serializer(stocks, many=True)
        return Response(serializer.data)


class PrescriptionViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des prescriptions"""
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, CanManageConsultations]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['consultation', 'methode']
    ordering_fields = ['date_prescription']
    ordering = ['-date_prescription']


class MouvementStockViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des mouvements de stock"""
    queryset = MouvementStock.objects.all()
    permission_classes = [IsAuthenticated, CanManageStock]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type_mouvement', 'stock_item']
    ordering_fields = ['date_mouvement']
    ordering = ['-date_mouvement']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MouvementStockCreateSerializer
        return MouvementStockSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Views pour les statistiques et rapports
from rest_framework.views import APIView


class StatistiquesView(APIView):
    """API pour les statistiques générales"""
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Récupère les statistiques générales de l'application",
        responses={
            200: openapi.Response(
                description="Statistiques générales",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_patients': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_consultations': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_rendez_vous': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_stocks': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'consultations_30j': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'rendez_vous_a_venir': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'stocks_alerte': openapi.Schema(type=openapi.TYPE_INTEGER),
                    }
                )
            )
        }
    )
    def get(self, request):
        # Statistiques générales
        total_patients = Patient.objects.count()
        total_consultations = ConsultationPF.objects.count()
        total_rendez_vous = RendezVous.objects.count()
        total_stocks = StockItem.objects.count()
        
        # Consultations par période (30 derniers jours)
        date_limite = timezone.now() - timedelta(days=30)
        consultations_30j = ConsultationPF.objects.filter(date__gte=date_limite).count()
        
        # Rendez-vous à venir
        rendez_vous_a_venir = RendezVous.objects.filter(
            datetime__gte=timezone.now(),
            statut__in=['planifie', 'confirme']
        ).count()
        
        # Stocks en alerte
        stocks_alerte = StockItem.objects.filter(
            quantite__lte=F('seuil')
        ).count()
        
        return Response({
            'total_patients': total_patients,
            'total_consultations': total_consultations,
            'total_rendez_vous': total_rendez_vous,
            'total_stocks': total_stocks,
            'consultations_30j': consultations_30j,
            'rendez_vous_a_venir': rendez_vous_a_venir,
            'stocks_alerte': stocks_alerte,
        })


class StatistiquesConsultationsView(APIView):
    """API pour les statistiques des consultations"""
    permission_classes = [IsAuthenticated, IsAdminOrMedicalStaff]
    
    @swagger_auto_schema(
        operation_description="Récupère les statistiques détaillées des consultations PF",
        manual_parameters=[
            openapi.Parameter('date_debut', openapi.IN_QUERY, description="Date de début (YYYY-MM-DD)", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('date_fin', openapi.IN_QUERY, description="Date de fin (YYYY-MM-DD)", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
        ],
        responses={
            200: openapi.Response(
                description="Statistiques des consultations",
                schema=openapi.Schema(type=openapi.TYPE_OBJECT)
            )
        }
    )
    def get(self, request):
        date_debut = request.query_params.get('date_debut', None)
        date_fin = request.query_params.get('date_fin', None)
        
        queryset = ConsultationPF.objects.all()
        
        if date_debut:
            queryset = queryset.filter(date__gte=date_debut)
        if date_fin:
            queryset = queryset.filter(date__lte=date_fin)
        
        # Nombre de consultations par période
        total = queryset.count()
        
        # Distribution des méthodes prescrites
        methodes_distribution = queryset.values('methode_prescite__nom').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Consultations avec méthode posée
        methodes_posees = queryset.filter(methode_posee=True).count()
        
        return Response({
            'total_consultations': total,
            'methodes_distribution': list(methodes_distribution),
            'methodes_posees': methodes_posees,
            'taux_pose': (methodes_posees / total * 100) if total > 0 else 0,
        })


class StatistiquesRendezVousView(APIView):
    """API pour les statistiques des rendez-vous"""
    permission_classes = [IsAuthenticated, CanManageAppointments]
    
    @swagger_auto_schema(
        operation_description="Récupère les statistiques détaillées des rendez-vous",
        manual_parameters=[
            openapi.Parameter('date_debut', openapi.IN_QUERY, description="Date de début (YYYY-MM-DD)", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('date_fin', openapi.IN_QUERY, description="Date de fin (YYYY-MM-DD)", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
        ],
        responses={200: openapi.Response(description="Statistiques des rendez-vous", schema=openapi.Schema(type=openapi.TYPE_OBJECT))}
    )
    def get(self, request):
        date_debut = request.query_params.get('date_debut', None)
        date_fin = request.query_params.get('date_fin', None)
        
        queryset = RendezVous.objects.all()
        
        if date_debut:
            queryset = queryset.filter(datetime__gte=date_debut)
        if date_fin:
            queryset = queryset.filter(datetime__lte=date_fin)
        
        # Total
        total = queryset.count()
        
        # Par statut
        par_statut = queryset.values('statut').annotate(count=Count('id'))
        
        # Taux d'assiduité (terminés / (terminés + absents))
        termines = queryset.filter(statut='termine').count()
        absents = queryset.filter(statut='absent').count()
        taux_assiduite = (termines / (termines + absents) * 100) if (termines + absents) > 0 else 0
        
        return Response({
            'total_rendez_vous': total,
            'par_statut': list(par_statut),
            'termines': termines,
            'absents': absents,
            'taux_assiduite': round(taux_assiduite, 2),
        })


class StatistiquesStocksView(APIView):
    """API pour les statistiques des stocks"""
    permission_classes = [IsAuthenticated, CanManageStock]
    
    @swagger_auto_schema(
        operation_description="Récupère les statistiques détaillées des stocks",
        responses={200: openapi.Response(description="Statistiques des stocks", schema=openapi.Schema(type=openapi.TYPE_OBJECT))}
    )
    def get(self, request):
        # Stocks en rupture
        stocks_rupture = StockItem.objects.filter(quantite__lte=0).count()
        
        # Stocks sous seuil
        stocks_sous_seuil = StockItem.objects.filter(
            quantite__lte=F('seuil'),
            quantite__gt=0
        ).count()
        
        # Valeur totale du stock (approximation)
        total_quantite = StockItem.objects.aggregate(
            total=Sum('quantite')
        )['total'] or 0
        
        # Mouvements récents (7 derniers jours)
        date_limite = timezone.now() - timedelta(days=7)
        mouvements_recents = MouvementStock.objects.filter(
            date_mouvement__gte=date_limite
        ).count()
        
        return Response({
            'stocks_rupture': stocks_rupture,
            'stocks_sous_seuil': stocks_sous_seuil,
            'total_quantite': total_quantite,
            'mouvements_7j': mouvements_recents,
        })


class LandingPageContentViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion du contenu de la landing page"""
    queryset = LandingPageContent.objects.all()
    permission_classes = [IsAuthenticated, CanManageUsers]  # Seuls les admins peuvent modifier
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return LandingPageContentUpdateSerializer
        return LandingPageContentSerializer
    
    def get_object(self):
        # Retourne toujours l'instance unique (pk=1)
        content, created = LandingPageContent.get_content()
        return content
    
    def list(self, request, *args, **kwargs):
        # Retourne l'instance unique directement
        content = LandingPageContent.get_content()
        serializer = self.get_serializer(content)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        # Retourne l'instance unique
        content = LandingPageContent.get_content()
        serializer = self.get_serializer(content)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[])
    def public(self, request):
        """Endpoint public pour récupérer le contenu de la landing page (sans authentification)"""
        content = LandingPageContent.get_content()
        serializer = self.get_serializer(content)
        return Response(serializer.data)


class ServiceViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des services"""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, CanManageUsers]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['ordre']
    ordering = ['ordre']


class ValueViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des valeurs"""
    queryset = Value.objects.all()
    serializer_class = ValueSerializer
    permission_classes = [IsAuthenticated, CanManageUsers]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['ordre']
    ordering = ['ordre']
