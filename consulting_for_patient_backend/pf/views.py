from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Sum, F
from django.utils import timezone
from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import (
    User, Patient, RendezVous,
    ConsultationPF, LandingPageContent, Service, Value, ContactMessage, Pharmacie,
    Hopital, Specialite, Specialiste, DisponibiliteSpecialiste,
    Produit, StockProduit, CommandePharmacie, LigneCommande,
    Notification, RapportConsultation, AvisSpecialiste,
    SessionUtilisateur, HistoriqueConnexion
)
from .serializers import (
    UserSerializer, UserCreateSerializer, PatientSerializer, PatientListSerializer,
    RendezVousSerializer, ConsultationPFSerializer,
    ConsultationPFListSerializer,
    LandingPageContentSerializer, LandingPageContentUpdateSerializer,
    ServiceSerializer, ValueSerializer, ContactMessageSerializer, PharmacieSerializer,
    HopitalSerializer, HopitalListSerializer, SpecialiteSerializer,
    SpecialisteSerializer, DisponibiliteSpecialisteSerializer,
    ProduitSerializer, StockProduitSerializer, CommandePharmacieSerializer,
    LigneCommandeSerializer, NotificationSerializer,
    RapportConsultationSerializer, AvisSpecialisteSerializer,
    SessionUtilisateurSerializer, HistoriqueConnexionSerializer
)
from .permissions import (
    IsAdminOrReadOnly, IsAdminOrMedicalStaff, IsAdminOrPharmacist,
    IsAdminOrReception, CanManageUsers, CanManageStock, CanManageConsultations,
    CanManageAppointments, IsPatientOrStaff, IsPatientOrAdmin,
    IsSuperAdmin, IsAdminHopital, IsSpecialiste, IsSpecialisteOfHopital,
    CanManagePharmacieCommandes, IsPatientOwner
)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des utilisateurs"""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, CanManageUsers]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'email']
    ordering_fields = ['nom', 'email', 'date_joined']
    ordering = ['nom']
    
    def get_permissions(self):
        """Override permissions for specific actions"""
        if self.action == 'change_password':
            # Only require authentication for password change
            return [IsAuthenticated()]
        return super().get_permissions()
    
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
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Changer le mot de passe de l'utilisateur connecté"""
        from django.contrib.auth import authenticate
        
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        
        if not current_password or not new_password:
            return Response(
                {'error': 'Mot de passe actuel et nouveau mot de passe requis'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier le mot de passe actuel
        user = authenticate(email=request.user.email, password=current_password)
        if not user:
            return Response(
                {'error': 'Mot de passe actuel incorrect'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Changer le mot de passe
        request.user.set_password(new_password)
        request.user.save()
        
        return Response({'status': 'Mot de passe changé avec succès'})


class PatientViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des patients"""
    queryset = Patient.objects.all()
    permission_classes = [IsAuthenticated, IsPatientOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sexe']
    search_fields = ['nom', 'prenom', 'telephone']
    ordering_fields = ['nom', 'prenom', 'dob', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PatientListSerializer
        return PatientSerializer
    
    def get_queryset(self):
        # Pour la génération du schéma Swagger, retourner un queryset vide
        if getattr(self, 'swagger_fake_view', False):
            return Patient.objects.none()
            
        queryset = super().get_queryset()
        user = self.request.user
        
        # Si l'utilisateur n'est pas authentifié, retourner un queryset vide
        if not user.is_authenticated:
            return Patient.objects.none()
        
        # Si c'est un patient, voir seulement son propre profil
        if hasattr(user, 'patient_profile'):
            patient = user.patient_profile
            queryset = queryset.filter(id=patient.id)
            return queryset
        
        # Si c'est un admin hôpital, voir seulement les patients liés à son hôpital
        if user.role == 'admin_hopital':
            try:
                from .models import Hopital, Registre
                hopital = Hopital.objects.get(admin_hopital=user)
                
                # Récupérer les IDs des patients qui ont des registres dans cet hôpital
                patient_ids = Registre.objects.filter(
                    hopital=hopital,
                    patient__isnull=False
                ).values_list('patient_id', flat=True).distinct()
                
                queryset = queryset.filter(id__in=patient_ids)
            except Hopital.DoesNotExist:
                return queryset.none()
        
        # Si c'est un spécialiste, voir les patients de son hôpital
        if user.role == 'specialiste':
            try:
                from .models import Specialiste, Registre
                specialiste = Specialiste.objects.get(user=user)
                
                # Récupérer les IDs des patients qui ont des registres dans l'hôpital du spécialiste
                patient_ids = Registre.objects.filter(
                    hopital=specialiste.hopital,
                    patient__isnull=False
                ).values_list('patient_id', flat=True).distinct()
                
                queryset = queryset.filter(id__in=patient_ids)
            except Specialiste.DoesNotExist:
                return queryset.none()
        
        return queryset
    
    def get_object(self):
        # Si c'est un patient, retourner son propre profil
        if hasattr(self.request.user, 'patient_profile'):
            return self.request.user.patient_profile
        return super().get_object()
    
    @action(detail=False, methods=['get', 'patch', 'put'])
    def me(self, request):
        """Retourne ou met à jour le profil du patient connecté"""
        if hasattr(request.user, 'patient_profile'):
            patient = request.user.patient_profile
            
            if request.method == 'GET':
                serializer = self.get_serializer(patient)
                return Response(serializer.data)
            
            elif request.method in ['PATCH', 'PUT']:
                partial = request.method == 'PATCH'
                serializer = self.get_serializer(patient, data=request.data, partial=partial)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        return Response({'error': 'Aucun profil patient trouvé'}, status=404)
    
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


class RendezVousViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des rendez-vous"""
    queryset = RendezVous.objects.all()
    serializer_class = RendezVousSerializer
    permission_classes = [IsAuthenticated, IsPatientOrStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['statut', 'patient', 'specialiste', 'hopital']
    search_fields = ['patient__nom', 'patient__prenom', 'notes']
    ordering_fields = ['datetime', 'created_at']
    ordering = ['-datetime']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Court-circuiter lors de la génération du schéma Swagger
        if getattr(self, 'swagger_fake_view', False):
            return queryset
        
        # Filtre par date
        date_debut = self.request.query_params.get('date_debut', None)
        date_fin = self.request.query_params.get('date_fin', None)
        
        if date_debut:
            queryset = queryset.filter(datetime__gte=date_debut)
        if date_fin:
            queryset = queryset.filter(datetime__lte=date_fin)
        
        # Si l'utilisateur n'est pas super admin, filtrer selon le rôle
        if self.request.user.role != 'super_admin':
            if self.request.user.role == 'admin_hopital':
                # Admin hôpital voit les rendez-vous de son hôpital
                try:
                    from .models import Hopital
                    hopital = Hopital.objects.get(admin_hopital=self.request.user)
                    queryset = queryset.filter(hopital=hopital)
                except:
                    queryset = queryset.none()
            elif self.request.user.role == 'specialiste':
                # Spécialiste voit seulement ses propres rendez-vous
                try:
                    from .models import Specialiste
                    specialiste = Specialiste.objects.get(user=self.request.user)
                    queryset = queryset.filter(specialiste=specialiste)
                except:
                    queryset = queryset.none()
            elif hasattr(self.request.user, 'patient_profile'):
                # Si c'est un patient, voir seulement ses propres rendez-vous
                patient = self.request.user.patient_profile
                queryset = queryset.filter(patient=patient)
        
        return queryset
    
    @swagger_auto_schema(
        method='get',
        operation_description="Récupère l'agenda d'un spécialiste pour une date donnée",
        manual_parameters=[
            openapi.Parameter('specialiste_id', openapi.IN_QUERY, description="ID du spécialiste", type=openapi.TYPE_INTEGER),
            openapi.Parameter('date', openapi.IN_QUERY, description="Date (format: YYYY-MM-DD)", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
        ],
        responses={200: RendezVousSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def agenda(self, request):
        """Récupère l'agenda d'un spécialiste"""
        specialiste_id = request.query_params.get('specialiste_id', None)
        date = request.query_params.get('date', None)
        
        queryset = self.get_queryset()
        
        if specialiste_id:
            queryset = queryset.filter(specialiste_id=specialiste_id)
        elif request.user.role not in ['super_admin', 'admin_hopital']:
            if request.user.role == 'specialiste':
                try:
                    from .models import Specialiste
                    specialiste = Specialiste.objects.get(user=request.user)
                    queryset = queryset.filter(specialiste=specialiste)
                except:
                    queryset = queryset.none()
            elif hasattr(request.user, 'patient_profile'):
                patient = request.user.patient_profile
                queryset = queryset.filter(patient=patient)
        
        if date:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
                queryset = queryset.filter(datetime__date=date_obj)
            except ValueError:
                pass
        
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
        """Annuler un rendez-vous avec option de reprogrammation"""
        rendez_vous = self.get_object()
        motif = request.data.get('motif', '')
        reprogrammer = request.data.get('reprogrammer', False)
        nouvelle_date = request.data.get('nouvelle_date')
        nouvelle_heure = request.data.get('nouvelle_heure')
        
        # Annuler le rendez-vous actuel
        rendez_vous.statut = 'annule'
        rendez_vous.motif_refus = motif  # Utiliser motif_refus pour stocker le motif d'annulation
        rendez_vous.save()
        
        # Créer un nouveau rendez-vous si reprogrammation demandée
        nouveau_rdv = None
        if reprogrammer and nouvelle_date and nouvelle_heure:
            try:
                # Parser la nouvelle date et heure
                from datetime import datetime
                nouvelle_datetime_str = f"{nouvelle_date} {nouvelle_heure}"
                nouvelle_datetime = datetime.strptime(nouvelle_datetime_str, '%Y-%m-%d %H:%M')
                
                # Rendre la datetime timezone-aware
                from django.utils import timezone
                nouvelle_datetime = timezone.make_aware(nouvelle_datetime)
                
                # Vérifier que la nouvelle date est dans le futur
                if nouvelle_datetime <= timezone.now():
                    return Response(
                        {'error': 'La nouvelle date doit être dans le futur'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Créer le nouveau rendez-vous
                nouveau_rdv = RendezVous.objects.create(
                    patient=rendez_vous.patient,
                    specialiste=rendez_vous.specialiste,
                    hopital=rendez_vous.hopital,
                    datetime=nouvelle_datetime,
                    motif=rendez_vous.motif,
                    statut='en_attente'
                )
                
                # Créer une notification pour le patient
                if hasattr(rendez_vous.patient, 'user') and rendez_vous.patient.user:
                    Notification.objects.create(
                        user=rendez_vous.patient.user,
                        type_notification='rendez_vous_nouveau',
                        titre='Rendez-vous reprogrammé',
                        message=f'Votre rendez-vous a été reprogrammé pour le {nouvelle_datetime.strftime("%d/%m/%Y à %H:%M")}.',
                        rendez_vous=nouveau_rdv
                    )
                
            except ValueError as e:
                return Response(
                    {'error': f'Format de date/heure invalide: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {'error': f'Erreur lors de la reprogrammation: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        response_data = {
            'status': 'Rendez-vous annulé',
            'motif': motif
        }
        
        if nouveau_rdv:
            from .serializers import RendezVousSerializer
            response_data['nouveau_rendez_vous'] = RendezVousSerializer(nouveau_rdv).data
            response_data['status'] = 'Rendez-vous annulé et reprogrammé'
        
        return Response(response_data)
    
    @action(detail=False, methods=['get'])
    def mes_rendez_vous(self, request):
        """Récupère les rendez-vous de l'utilisateur connecté"""
        queryset = self.get_queryset()
        
        if request.user.role == 'specialiste':
            try:
                from .models import Specialiste
                specialiste = Specialiste.objects.get(user=request.user)
                queryset = queryset.filter(specialiste=specialiste)
            except:
                queryset = queryset.none()
        elif hasattr(request.user, 'patient_profile'):
            patient = request.user.patient_profile
            queryset = queryset.filter(patient=patient)
        elif request.user.role == 'admin_hopital':
            try:
                from .models import Hopital
                hopital = Hopital.objects.get(admin_hopital=request.user)
                queryset = queryset.filter(hopital=hopital)
            except:
                queryset = queryset.none()
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ConsultationPFViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des consultations PF"""
    queryset = ConsultationPF.objects.all()
    permission_classes = [IsAuthenticated, IsPatientOrStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['patient', 'specialiste', 'hopital']
    search_fields = ['patient__nom', 'patient__prenom', 'notes', 'anamnese']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ConsultationPFListSerializer
        return ConsultationPFSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Court-circuiter lors de la génération du schéma Swagger
        if getattr(self, 'swagger_fake_view', False):
            return queryset
        
        # Filtre par date
        date_debut = self.request.query_params.get('date_debut', None)
        date_fin = self.request.query_params.get('date_fin', None)
        
        if date_debut:
            queryset = queryset.filter(date__gte=date_debut)
        if date_fin:
            queryset = queryset.filter(date__lte=date_fin)
        
        # Si l'utilisateur n'est pas super admin, filtrer selon le rôle
        if self.request.user.role != 'super_admin':
            if self.request.user.role == 'admin_hopital':
                try:
                    from .models import Hopital
                    hopital = Hopital.objects.get(admin_hopital=self.request.user)
                    queryset = queryset.filter(hopital=hopital)
                except:
                    queryset = queryset.none()
            elif self.request.user.role == 'specialiste':
                try:
                    from .models import Specialiste
                    specialiste = Specialiste.objects.get(user=self.request.user)
                    queryset = queryset.filter(specialiste=specialiste)
                except:
                    queryset = queryset.none()
            elif hasattr(self.request.user, 'patient_profile'):
                # Si c'est un patient, voir seulement ses propres consultations
                patient = self.request.user.patient_profile
                queryset = queryset.filter(patient=patient)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def mes_consultations(self, request):
        """Récupère les consultations de l'utilisateur connecté"""
        queryset = self.get_queryset()
        
        if request.user.role == 'specialiste':
            try:
                from .models import Specialiste
                specialiste = Specialiste.objects.get(user=request.user)
                queryset = queryset.filter(specialiste=specialiste)
            except:
                queryset = queryset.none()
        elif hasattr(request.user, 'patient_profile'):
            patient = request.user.patient_profile
            queryset = queryset.filter(patient=patient)
        elif request.user.role == 'admin_hopital':
            try:
                from .models import Hopital
                hopital = Hopital.objects.get(admin_hopital=request.user)
                queryset = queryset.filter(hopital=hopital)
            except:
                queryset = queryset.none()
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PharmacieViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des pharmacies"""
    queryset = Pharmacie.objects.all()
    serializer_class = PharmacieSerializer
    # Ne pas définir permission_classes ici, utiliser get_permissions() à la place
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['actif', 'user']
    search_fields = ['nom', 'adresse', 'telephone', 'email']
    ordering_fields = ['nom', 'created_at']
    ordering = ['nom']
    
    def get_permissions(self):
        """
        Permissions personnalisées:
        - list, retrieve: accès public (AllowAny)
        - autres actions (create, update, delete): authentification requise
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Court-circuiter lors de la génération du schéma Swagger
        if getattr(self, 'swagger_fake_view', False):
            return queryset
        
        # Pour les actions publiques (list, retrieve), montrer les pharmacies actives
        if self.action in ['list', 'retrieve']:
            # Si pas authentifié, montrer seulement les actives
            if not hasattr(self.request, 'user') or not self.request.user.is_authenticated:
                return queryset.filter(actif=True)
            
            # Si authentifié, vérifier le rôle
            # Les pharmaciens voient uniquement leurs propres pharmacies
            if self.request.user.role == 'pharmacien':
                return queryset.filter(user=self.request.user)
            # Les employés voient uniquement la pharmacie où ils travaillent
            elif self.request.user.role == 'employe_pharmacie':
                try:
                    from .models import EmployePharmacie
                    employe = EmployePharmacie.objects.get(user=self.request.user, actif=True)
                    return queryset.filter(id=employe.pharmacie.id)
                except EmployePharmacie.DoesNotExist:
                    return queryset.none()
            # Les super admins voient toutes les pharmacies
            elif self.request.user.role == 'super_admin':
                return queryset
            # Les autres utilisateurs (patients, etc.) voient les pharmacies actives
            else:
                return queryset.filter(actif=True)
        
        # Pour les autres actions (create, update, delete), vérifier l'authentification
        if not hasattr(self.request, 'user') or not self.request.user.is_authenticated:
            return queryset.none()
        
        # Les pharmaciens voient uniquement leurs propres pharmacies
        if self.request.user.role == 'pharmacien':
            queryset = queryset.filter(user=self.request.user)
        # Les employés voient uniquement la pharmacie où ils travaillent
        elif self.request.user.role == 'employe_pharmacie':
            try:
                from .models import EmployePharmacie
                employe = EmployePharmacie.objects.get(user=self.request.user, actif=True)
                queryset = queryset.filter(id=employe.pharmacie.id)
            except EmployePharmacie.DoesNotExist:
                queryset = queryset.none()
        # Les super admins voient toutes les pharmacies
        elif self.request.user.role == 'super_admin':
            queryset = queryset
        # Les autres utilisateurs ne peuvent pas modifier
        else:
            queryset = queryset.none()
        
        return queryset
    
    def perform_create(self, serializer):
        # Si c'est un pharmacien, associer automatiquement la pharmacie à l'utilisateur
        if self.request.user.role == 'pharmacien':
            serializer.save(user=self.request.user)
        else:
            # Si c'est un super admin qui crée une pharmacie, créer automatiquement un compte pharmacien
            pharmacie_data = serializer.validated_data
            email = pharmacie_data.get('email')
            nom = pharmacie_data.get('nom')
            
            if email and not pharmacie_data.get('user'):
                # Créer un utilisateur pharmacien avec le mot de passe par défaut
                try:
                    user = User.objects.create_user(
                        email=email,
                        password='admin123',
                        nom=f"Admin {nom}",
                        role='pharmacien',
                        actif=True
                    )
                    serializer.save(user=user)
                except Exception as e:
                    # Si l'utilisateur existe déjà, utiliser l'utilisateur existant
                    try:
                        user = User.objects.get(email=email, role='pharmacien')
                        serializer.save(user=user)
                    except User.DoesNotExist:
                        serializer.save()
            else:
                serializer.save()
    
    @action(detail=False, methods=['get'])
    def ma_pharmacie(self, request):
        """Récupère la pharmacie de l'utilisateur connecté (pharmacien)"""
        if request.user.role == 'pharmacien':
            try:
                pharmacie = Pharmacie.objects.get(user=request.user)
                serializer = self.get_serializer(pharmacie)
                return Response(serializer.data)
            except Pharmacie.DoesNotExist:
                return Response(
                    {'error': 'Aucune pharmacie trouvée pour cet utilisateur'},
                    status=status.HTTP_404_NOT_FOUND
                )
        elif request.user.role == 'employe_pharmacie':
            try:
                from .models import EmployePharmacie
                employe = EmployePharmacie.objects.get(user=request.user, actif=True)
                serializer = self.get_serializer(employe.pharmacie)
                return Response(serializer.data)
            except EmployePharmacie.DoesNotExist:
                return Response(
                    {'error': 'Aucune pharmacie trouvée pour cet employé'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {'error': 'Accès non autorisé'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    @action(detail=True, methods=['post'])
    def suspendre(self, request, pk=None):
        """Suspendre une pharmacie (mettre actif=False) et désactiver tous les utilisateurs liés"""
        pharmacie = self.get_object()
        pharmacie.actif = False
        pharmacie.save()
        
        # Désactiver l'administrateur de la pharmacie
        if pharmacie.user:
            pharmacie.user.actif = False
            pharmacie.user.save()
        
        # Désactiver tous les employés de la pharmacie
        from .models import EmployePharmacie
        employes = EmployePharmacie.objects.filter(pharmacie=pharmacie)
        for employe in employes:
            employe.user.actif = False
            employe.user.save()
        
        return Response({
            'status': 'Pharmacie suspendue avec succès',
            'message': f'Pharmacie et {1 + employes.count()} utilisateur(s) désactivé(s)'
        })
    
    @action(detail=True, methods=['post'])
    def activer(self, request, pk=None):
        """Activer une pharmacie et réactiver tous les utilisateurs liés"""
        pharmacie = self.get_object()
        pharmacie.actif = True
        pharmacie.save()
        
        # Réactiver l'administrateur de la pharmacie
        if pharmacie.user:
            pharmacie.user.actif = True
            pharmacie.user.save()
        
        # Réactiver tous les employés de la pharmacie
        from .models import EmployePharmacie
        employes = EmployePharmacie.objects.filter(pharmacie=pharmacie)
        for employe in employes:
            employe.user.actif = True
            employe.user.save()
        
        return Response({
            'status': 'Pharmacie activée avec succès',
            'message': f'Pharmacie et {1 + employes.count()} utilisateur(s) réactivé(s)'
        })
    
    @action(detail=True, methods=['post'])
    def reset_admin_password(self, request, pk=None):
        """Réinitialiser le mot de passe de l'administrateur de la pharmacie"""
        pharmacie = self.get_object()
        
        if pharmacie.user:
            pharmacie.user.set_password('admin123')
            pharmacie.user.save()
            return Response({
                'status': 'Mot de passe réinitialisé avec succès',
                'message': 'Le mot de passe a été réinitialisé à "admin123"'
            })
        else:
            return Response(
                {'error': 'Aucun administrateur associé à cette pharmacie'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @swagger_auto_schema(
        method='get',
        operation_description="Récupère les pharmacies de l'utilisateur connecté",
        responses={200: PharmacieSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def mes_pharmacies(self, request):
        """Récupère les pharmacies de l'utilisateur connecté"""
        if request.user.role == 'pharmacien':
            pharmacies = Pharmacie.objects.filter(user=request.user, actif=True)
        elif request.user.role == 'employe_pharmacie':
            try:
                from .models import EmployePharmacie
                employe = EmployePharmacie.objects.get(user=request.user, actif=True)
                pharmacies = Pharmacie.objects.filter(id=employe.pharmacie.id, actif=True)
            except EmployePharmacie.DoesNotExist:
                pharmacies = Pharmacie.objects.none()
        elif request.user.role == 'super_admin':
            pharmacies = Pharmacie.objects.all()
        else:
            pharmacies = Pharmacie.objects.none()
        
        serializer = self.get_serializer(pharmacies, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activer(self, request, pk=None):
        """Activer une pharmacie"""
        pharmacie = self.get_object()
        pharmacie.actif = True
        pharmacie.save()
        return Response({'status': 'Pharmacie activée'})
    
    @action(detail=True, methods=['post'])
    def desactiver(self, request, pk=None):
        """Désactiver une pharmacie"""
        pharmacie = self.get_object()
        pharmacie.actif = False
        pharmacie.save()
        return Response({'status': 'Pharmacie désactivée'})


# Views pour les statistiques et rapports
from rest_framework.views import APIView


class StatistiquesView(APIView):
    """API pour les statistiques générales"""
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Récupère les statistiques générales de l'application (filtrées par rôle)",
        responses={
            200: openapi.Response(
                description="Statistiques générales",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_specialistes': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'specialistes_actifs': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_rendez_vous': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'rendez_vous_en_attente': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'rendez_vous_confirmes': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_consultations': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'consultations_ce_mois': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'par_specialite': openapi.Schema(type=openapi.TYPE_OBJECT),
                    }
                )
            )
        }
    )
    def get(self, request):
        user = request.user
        
        # Pour admin_hopital : statistiques de son hôpital
        if user.role == 'admin_hopital':
            try:
                from .models import Hopital
                hopital = Hopital.objects.get(admin_hopital=user)
                
                # Statistiques des spécialistes
                total_specialistes = Specialiste.objects.filter(hopital=hopital).count()
                specialistes_actifs = Specialiste.objects.filter(hopital=hopital, actif=True).count()
                
                # Statistiques des rendez-vous
                total_rendez_vous = RendezVous.objects.filter(hopital=hopital).count()
                rendez_vous_en_attente = RendezVous.objects.filter(
                    hopital=hopital,
                    statut='en_attente'
                ).count()
                rendez_vous_confirmes = RendezVous.objects.filter(
                    hopital=hopital,
                    statut='confirme'
                ).count()
                
                # Statistiques des consultations
                total_consultations = ConsultationPF.objects.filter(hopital=hopital).count()
                
                # Consultations ce mois
                now = timezone.now()
                debut_mois = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                consultations_ce_mois = ConsultationPF.objects.filter(
                    hopital=hopital,
                    date__gte=debut_mois
                ).count()
                
                # Statistiques par spécialité
                from .models import Specialite
                specialites = Specialite.objects.filter(
                    specialistes__hopital=hopital,
                    specialistes__actif=True
                ).distinct()
                
                par_specialite = {}
                for specialite in specialites:
                    specialistes_count = Specialiste.objects.filter(
                        hopital=hopital,
                        specialite=specialite,
                        actif=True
                    ).count()
                    
                    rendez_vous_count = RendezVous.objects.filter(
                        hopital=hopital,
                        specialiste__specialite=specialite
                    ).count()
                    
                    consultations_count = ConsultationPF.objects.filter(
                        hopital=hopital,
                        specialiste__specialite=specialite
                    ).count()
                    
                    par_specialite[specialite.nom] = {
                        'specialistes': specialistes_count,
                        'rendez_vous': rendez_vous_count,
                        'consultations': consultations_count
                    }
                
                return Response({
                    'total_specialistes': total_specialistes,
                    'specialistes_actifs': specialistes_actifs,
                    'total_rendez_vous': total_rendez_vous,
                    'rendez_vous_en_attente': rendez_vous_en_attente,
                    'rendez_vous_confirmes': rendez_vous_confirmes,
                    'total_consultations': total_consultations,
                    'consultations_ce_mois': consultations_ce_mois,
                    'par_specialite': par_specialite,
                })
                
            except Hopital.DoesNotExist:
                return Response(
                    {'error': 'Aucun hôpital trouvé pour cet administrateur'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Pour les autres rôles : statistiques globales (super_admin, etc.)
        total_patients = Patient.objects.count()
        total_consultations = ConsultationPF.objects.count()
        total_rendez_vous = RendezVous.objects.count()
        total_stocks_produits = StockProduit.objects.count()
        
        # Consultations par période (30 derniers jours)
        date_limite = timezone.now() - timedelta(days=30)
        consultations_30j = ConsultationPF.objects.filter(date__gte=date_limite).count()
        
        # Rendez-vous à venir
        rendez_vous_a_venir = RendezVous.objects.filter(
            datetime__gte=timezone.now(),
            statut__in=['planifie', 'confirme']
        ).count()
        
        # Stocks en alerte
        stocks_alerte = StockProduit.objects.filter(
            quantite__lte=F('seuil_alerte')
        ).count()
        
        return Response({
            'total_patients': total_patients,
            'total_consultations': total_consultations,
            'total_rendez_vous': total_rendez_vous,
            'total_stocks_produits': total_stocks_produits,
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
    """API pour les statistiques des stocks de produits"""
    permission_classes = [IsAuthenticated, CanManageStock]
    
    @swagger_auto_schema(
        operation_description="Récupère les statistiques détaillées des stocks de produits",
        responses={200: openapi.Response(description="Statistiques des stocks", schema=openapi.Schema(type=openapi.TYPE_OBJECT))}
    )
    def get(self, request):
        # Stocks en rupture
        stocks_rupture = StockProduit.objects.filter(quantite__lte=0).count()
        
        # Stocks sous seuil
        stocks_sous_seuil = StockProduit.objects.filter(
            quantite__lte=F('seuil_alerte'),
            quantite__gt=0
        ).count()
        
        # Valeur totale du stock
        valeur_totale = StockProduit.objects.aggregate(
            total=Sum(F('quantite') * F('prix_vente'))
        )['total'] or 0
        
        # Total des produits en stock
        total_quantite = StockProduit.objects.aggregate(
            total=Sum('quantite')
        )['total'] or 0
        
        return Response({
            'stocks_rupture': stocks_rupture,
            'stocks_sous_seuil': stocks_sous_seuil,
            'total_quantite': total_quantite,
            'valeur_totale': valeur_totale,
        })


class AnalyticsDashboardView(APIView):
    """API pour les analytics du dashboard Super Admin"""
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Récupère les analytics complètes pour le dashboard Super Admin",
        responses={
            200: openapi.Response(
                description="Analytics du dashboard",
                schema=openapi.Schema(type=openapi.TYPE_OBJECT)
            )
        }
    )
    def get(self, request):
        from django.db.models import Avg, Count, Q, Sum, F
        from datetime import datetime, timedelta
        
        now = timezone.now()
        debut_mois = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        debut_annee = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        il_y_a_6_mois = now - timedelta(days=180)
        il_y_a_7_jours = now - timedelta(days=7)
        
        # 1. Taux de conversion (RDV confirmés / RDV totaux)
        total_rdv = RendezVous.objects.count()
        rdv_confirmes = RendezVous.objects.filter(statut='confirme').count()
        rdv_termines = RendezVous.objects.filter(statut='termine').count()
        
        # Conversion = (confirmés + terminés) / total
        rdv_reussis = rdv_confirmes + rdv_termines
        taux_conversion = (rdv_reussis / total_rdv * 100) if total_rdv > 0 else 0
        
        # 2. Temps moyen de consultation (en minutes)
        # Calculer la différence entre created_at et updated_at pour les consultations
        consultations_avec_duree = ConsultationPF.objects.filter(
            created_at__isnull=False,
            updated_at__isnull=False
        ).exclude(created_at=F('updated_at'))
        
        temps_moyen = 0
        if consultations_avec_duree.exists():
            durees = []
            for consultation in consultations_avec_duree:
                duree = (consultation.updated_at - consultation.created_at).total_seconds() / 60
                # Filtrer les valeurs aberrantes (entre 5 min et 180 min)
                if 5 <= duree <= 180:
                    durees.append(duree)
            
            if durees:
                temps_moyen = sum(durees) / len(durees)
        
        # Si pas de données, calculer une estimation basée sur le nombre de consultations
        if temps_moyen == 0:
            total_consultations = ConsultationPF.objects.count()
            # Estimation: 30 min par défaut si pas de données
            temps_moyen = 30 if total_consultations > 0 else 0
        
        # 3. Consultations par mois (6 derniers mois)
        # Utiliser une approche simple sans TruncMonth pour éviter les problèmes de timezone MySQL
        consultations_recentes = ConsultationPF.objects.filter(
            date__gte=il_y_a_6_mois
        ).values('date')
        
        # Créer un dictionnaire avec tous les 6 derniers mois (même si 0 consultations)
        mois_dict = {}
        for i in range(6):
            mois = (now - timedelta(days=30*i)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            key = f"{mois.year}-{mois.month:02d}"
            mois_dict[key] = {
                'label': mois.strftime('%b %Y'),
                'count': 0
            }
        
        # Compter manuellement les consultations par mois
        for consultation in consultations_recentes:
            date = consultation['date']
            if date:
                key = f"{date.year}-{date.month:02d}"
                if key in mois_dict:
                    mois_dict[key]['count'] += 1
        
        # Trier par date et formater
        mois_sorted = sorted(mois_dict.items(), key=lambda x: x[0])
        mois_labels = [item[1]['label'] for item in mois_sorted]
        mois_data = [item[1]['count'] for item in mois_sorted]
        
        # 4. Rendez-vous par statut
        rdv_par_statut = RendezVous.objects.values('statut').annotate(
            count=Count('id')
        ).order_by('-count')
        
        statut_labels = []
        statut_data = []
        statut_colors = {
            'confirme': '#10B981',
            'en_attente': '#F59E0B',
            'annule': '#EF4444',
            'termine': '#3B82F6',
            'refuse': '#EF4444'
        }
        statut_colors_list = []
        
        statut_names = {
            'confirme': 'Confirmé',
            'en_attente': 'En attente',
            'annule': 'Annulé',
            'termine': 'Terminé',
            'refuse': 'Refusé'
        }
        
        for item in rdv_par_statut:
            statut_labels.append(statut_names.get(item['statut'], item['statut']))
            statut_data.append(item['count'])
            statut_colors_list.append(statut_colors.get(item['statut'], '#6B7280'))
        
        # 5. Activité hebdomadaire (7 derniers jours)
        activite_hebdo = []
        jours_semaine = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
        
        for i in range(7):
            jour = now - timedelta(days=6-i)
            debut_jour = jour.replace(hour=0, minute=0, second=0, microsecond=0)
            fin_jour = debut_jour + timedelta(days=1)
            
            # Compter les RDV créés ce jour
            rdv_count = RendezVous.objects.filter(
                created_at__gte=debut_jour,
                created_at__lt=fin_jour
            ).count()
            
            # Compter les consultations créées ce jour
            consult_count = ConsultationPF.objects.filter(
                created_at__gte=debut_jour,
                created_at__lt=fin_jour
            ).count()
            
            jour_semaine_index = jour.weekday()  # 0 = Lundi, 6 = Dimanche
            
            activite_hebdo.append({
                'jour': jours_semaine[jour_semaine_index],
                'date': jour.strftime('%Y-%m-%d'),
                'rendez_vous': rdv_count,
                'consultations': consult_count,
                'total': rdv_count + consult_count
            })
        
        # 6. Utilisateurs par rôle
        utilisateurs_par_role = User.objects.filter(actif=True).values('role').annotate(
            count=Count('id')
        ).order_by('-count')
        
        role_labels = []
        role_data = []
        role_colors = []
        role_color_map = {
            'patient': '#10B981',
            'specialiste': '#3B82F6',
            'pharmacien': '#F59E0B',
            'employe_pharmacie': '#F97316',
            'admin_hopital': '#8B5CF6',
            'super_admin': '#EF4444',
            'agent_enregistrement': '#06B6D4'
        }
        
        role_names = {
            'patient': 'Patients',
            'specialiste': 'Spécialistes',
            'pharmacien': 'Pharmaciens',
            'employe_pharmacie': 'Employés Pharmacie',
            'admin_hopital': 'Admins Hôpital',
            'super_admin': 'Super Admins',
            'agent_enregistrement': 'Agents'
        }
        
        for item in utilisateurs_par_role:
            role_labels.append(role_names.get(item['role'], item['role']))
            role_data.append(item['count'])
            role_colors.append(role_color_map.get(item['role'], '#6B7280'))
        
        # 7. Métriques supplémentaires
        # Taux d'annulation
        rdv_annules = RendezVous.objects.filter(statut='annule').count()
        rdv_refuses = RendezVous.objects.filter(statut='refuse').count()
        taux_annulation = ((rdv_annules + rdv_refuses) / total_rdv * 100) if total_rdv > 0 else 0
        
        # Satisfaction patient (note moyenne des spécialistes)
        satisfaction = Specialiste.objects.filter(actif=True).aggregate(
            avg_note=Avg('note_moyenne')
        )['avg_note']
        
        # Si pas de notes, utiliser 0
        if satisfaction is None:
            satisfaction = 0
        
        return Response({
            'taux_conversion': round(taux_conversion, 1),
            'temps_moyen_consultation': round(temps_moyen, 0),
            'taux_annulation': round(taux_annulation, 1),
            'satisfaction_patient': round(satisfaction, 1),
            'consultations_par_mois': {
                'labels': mois_labels,
                'data': mois_data
            },
            'rendez_vous_par_statut': {
                'labels': statut_labels,
                'data': statut_data,
                'colors': statut_colors_list
            },
            'activite_hebdomadaire': activite_hebdo,
            'utilisateurs_par_role': {
                'labels': role_labels,
                'data': role_data,
                'colors': role_colors
            },
            # Métriques brutes pour debug
            'meta': {
                'total_rdv': total_rdv,
                'rdv_confirmes': rdv_confirmes,
                'rdv_termines': rdv_termines,
                'total_consultations': ConsultationPF.objects.count(),
                'total_utilisateurs': User.objects.filter(actif=True).count()
            }
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
    
    def update(self, request, *args, **kwargs):
        # Mise à jour complète
        content = LandingPageContent.get_content()
        serializer = self.get_serializer(content, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        # Mise à jour partielle
        content = LandingPageContent.get_content()
        serializer = self.get_serializer(content, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['ordre']
    ordering = ['ordre']
    
    def get_permissions(self):
        """Permet l'accès public en lecture seule pour retrieve et list"""
        from rest_framework.permissions import AllowAny
        if self.action in ['retrieve', 'list']:
            return [AllowAny()]
        return [IsAuthenticated(), CanManageUsers()]
    
    @action(detail=False, methods=['get'], permission_classes=[])
    def public(self, request):
        """Endpoint public pour récupérer tous les services (sans authentification)"""
        services = Service.objects.all().order_by('ordre')
        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)


class ValueViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des valeurs"""
    queryset = Value.objects.all()
    serializer_class = ValueSerializer
    permission_classes = [IsAuthenticated, CanManageUsers]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['ordre']
    ordering = ['ordre']
    
    def get_permissions(self):
        """Permet l'accès public en lecture seule pour retrieve et list"""
        from rest_framework.permissions import AllowAny
        if self.action in ['retrieve', 'list']:
            return [AllowAny()]
        return [IsAuthenticated(), CanManageUsers()]
    
    @action(detail=False, methods=['get'], permission_classes=[])
    def public(self, request):
        """Endpoint public pour récupérer toutes les valeurs (sans authentification)"""
        values = Value.objects.all().order_by('ordre')
        serializer = self.get_serializer(values, many=True)
        return Response(serializer.data)


class ContactMessageViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des messages de contact"""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date_creation']
    ordering = ['-date_creation']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Court-circuiter lors de la génération du schéma Swagger
        if getattr(self, 'swagger_fake_view', False):
            return queryset
        
        # Les patients voient seulement leurs propres messages
        if hasattr(self.request.user, 'patient_profile'):
            patient = self.request.user.patient_profile
            queryset = queryset.filter(patient=patient)
        # Les admins et le personnel voient tous les messages
        elif self.request.user.role not in ['super_admin', 'admin_hopital', 'specialiste', 'agent_enregistrement']:
            queryset = queryset.none()
        
        return queryset
    
    def perform_create(self, serializer):
        # Associer le message au patient si l'utilisateur a un profil patient
        if hasattr(self.request.user, 'patient_profile'):
            serializer.save(patient=self.request.user.patient_profile)
        else:
            serializer.save()


# Import des nouveaux ViewSets pour la nouvelle architecture
from .new_views import (
    HopitalViewSet, SpecialiteViewSet, SpecialisteViewSet,
    DisponibiliteSpecialisteViewSet, ProduitViewSet, StockProduitViewSet,
    CommandePharmacieViewSet, NotificationViewSet,
    RapportConsultationViewSet, AvisSpecialisteViewSet
)


# Vue spéciale pour l'authentification des pharmaciens
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import PharmacyTokenObtainPairSerializer
from .middleware import log_login_attempt


class PharmacyTokenObtainPairView(TokenObtainPairView):
    """Vue d'authentification spécialement conçue pour les pharmaciens"""
    serializer_class = PharmacyTokenObtainPairSerializer
    
    @swagger_auto_schema(
        operation_description="Authentification JWT pour pharmaciens - Obtenir un token d'accès",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description="Email du pharmacien"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description="Mot de passe"),
            }
        ),
        responses={
            200: openapi.Response(
                description="Token d'accès et informations pharmacien",
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
        tags=['Authentification Pharmacie']
    )
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            
            # Si la connexion est réussie, enregistrer dans l'historique
            if response.status_code == 200:
                email = request.data.get('email')
                try:
                    user = User.objects.get(email=email, role__in=['pharmacien', 'employe_pharmacie'])
                    log_login_attempt(user, request, 'succes', 'Connexion pharmacien réussie')
                except User.DoesNotExist:
                    pass
            
            return response
        except Exception as e:
            # En cas d'erreur, enregistrer la tentative échouée
            email = request.data.get('email')
            if email:
                try:
                    user = User.objects.get(email=email)
                    log_login_attempt(user, request, 'echec', f'Échec de connexion: {str(e)}')
                except User.DoesNotExist:
                    pass
            
            raise e


class HospitalTokenObtainPairView(TokenObtainPairView):
    """Vue d'authentification spécialement conçue pour les hôpitaux (admin et spécialistes)"""
    
    def get_serializer_class(self):
        from .serializers import HospitalTokenObtainPairSerializer
        return HospitalTokenObtainPairSerializer
    
    @swagger_auto_schema(
        operation_description="Authentification JWT pour hôpitaux - Obtenir un token d'accès",
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
        tags=['Authentification Hôpital']
    )
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            
            # Si la connexion est réussie, enregistrer dans l'historique
            if response.status_code == 200:
                email = request.data.get('email')
                try:
                    user = User.objects.get(email=email, role__in=['admin_hopital', 'specialiste'])
                    log_login_attempt(user, request, 'succes', 'Connexion hôpital réussie')
                except User.DoesNotExist:
                    pass
            
            return response
        except Exception as e:
            # En cas d'erreur, enregistrer la tentative échouée
            email = request.data.get('email')
            if email:
                try:
                    user = User.objects.get(email=email)
                    log_login_attempt(user, request, 'echec', f'Échec de connexion: {str(e)}')
                except User.DoesNotExist:
                    pass
            
            raise e


class SessionUtilisateurViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des sessions utilisateurs"""
    queryset = SessionUtilisateur.objects.all()
    serializer_class = SessionUtilisateurSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['active', 'user']
    ordering_fields = ['date_creation', 'derniere_activite']
    ordering = ['-derniere_activite']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Court-circuiter lors de la génération du schéma Swagger
        if getattr(self, 'swagger_fake_view', False):
            return queryset
        
        # Les utilisateurs voient seulement leurs propres sessions
        return queryset.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def mes_sessions(self, request):
        """Récupère les sessions actives de l'utilisateur connecté"""
        sessions = self.get_queryset().filter(active=True)
        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def terminer(self, request, pk=None):
        """Termine une session spécifique"""
        session = self.get_object()
        session.active = False
        session.save()
        return Response({'status': 'Session terminée'})
    
    @action(detail=False, methods=['post'])
    def terminer_autres(self, request):
        """Termine toutes les autres sessions sauf la session actuelle"""
        session_actuelle = request.META.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')
        sessions = self.get_queryset().filter(active=True).exclude(session_key=session_actuelle)
        sessions.update(active=False)
        return Response({'status': f'{sessions.count()} sessions terminées'})


class HistoriqueConnexionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour l'historique des connexions (lecture seule)"""
    queryset = HistoriqueConnexion.objects.all()
    serializer_class = HistoriqueConnexionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['statut', 'user']
    ordering_fields = ['date_tentative']
    ordering = ['-date_tentative']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Court-circuiter lors de la génération du schéma Swagger
        if getattr(self, 'swagger_fake_view', False):
            return queryset
        
        # Les utilisateurs voient seulement leur propre historique
        return queryset.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Récupère l'historique récent (30 derniers jours)"""
        from datetime import timedelta
        date_limite = timezone.now() - timedelta(days=30)
        historique = self.get_queryset().filter(date_tentative__gte=date_limite)
        serializer = self.get_serializer(historique, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """Récupère les statistiques de connexion"""
        from datetime import timedelta
        from django.db.models import Count
        
        date_limite = timezone.now() - timedelta(days=30)
        queryset = self.get_queryset().filter(date_tentative__gte=date_limite)
        
        stats = queryset.aggregate(
            total_tentatives=Count('id'),
            connexions_reussies=Count('id', filter=Q(statut='succes')),
            tentatives_echouees=Count('id', filter=Q(statut='echec'))
        )
        
        # Calcul du taux de réussite
        if stats['total_tentatives'] > 0:
            stats['taux_reussite'] = round(
                (stats['connexions_reussies'] / stats['total_tentatives']) * 100, 2
            )
        else:
            stats['taux_reussite'] = 0
        
        return Response(stats)
