# Nouveaux ViewSets pour la nouvelle architecture
# Ce fichier contient les ViewSets pour les nouveaux modèles
# À ajouter dans views.py

from rest_framework import viewsets, status, filters
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def get_user_from_request(request):
    """Helper pour obtenir l'utilisateur depuis request en gérant le cas de génération du schéma"""
    if not request or not hasattr(request, 'user') or not request.user.is_authenticated:
        return None
    return request.user
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import (
    IsAdminOrMedicalStaff, IsSpecialiste, IsAdminHopital
)
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Sum, F, Avg
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import (
    Hopital, Specialite, Specialiste, DisponibiliteSpecialiste,
    Produit, StockProduit, CommandePharmacie, LigneCommande,
    Notification, RapportConsultation, AvisSpecialiste, RendezVous, Patient,
    ConsultationPF, Pharmacie, VentePharmacie, LigneVente, EmployePharmacie,
    Registre, Ordonnance, LigneOrdonnance, DossierMedical, FichierDossierMedical,
    Fournisseur, FactureFournisseur, LigneFactureFournisseur, User
)
from .serializers import (
    HopitalSerializer, HopitalListSerializer, SpecialiteSerializer,
    SpecialisteSerializer, DisponibiliteSpecialisteSerializer,
    ProduitSerializer, StockProduitSerializer, CommandePharmacieSerializer,
    CommandePharmacieCreateSerializer, LigneCommandeSerializer, NotificationSerializer,
    RapportConsultationSerializer, AvisSpecialisteSerializer,
    VentePharmacieSerializer, VentePharmacieCreateSerializer, LigneVenteSerializer,
    EmployePharmacieSerializer, EmployePharmacieCreateSerializer, EmployePharmacieUpdateSerializer,
    RegistreSerializer, RegistreCreateSerializer, RegistreUpdateSerializer, RegistreListSerializer,
    OrdonnanceSerializer, OrdonnanceCreateSerializer, OrdonnanceUpdateSerializer, OrdonnanceListSerializer,
    LigneOrdonnanceSerializer, LigneOrdonnanceCreateSerializer,
    DossierMedicalSerializer, DossierMedicalCreateSerializer, DossierMedicalUpdateSerializer, DossierMedicalListSerializer,
    DossierMedicalDetailSerializer, FichierDossierMedicalSerializer, FichierDossierMedicalCreateSerializer,
    FournisseurSerializer, FactureFournisseurSerializer, FactureFournisseurCreateSerializer,
    LigneFactureFournisseurSerializer, FactureFournisseurValidationSerializer
)
from .permissions import (
    IsSuperAdmin, IsAdminHopital, IsSpecialiste, IsSpecialisteOfHopital,
    CanManagePharmacieCommandes, IsPatientOwner, IsAdminOrReadOnly
)


class HopitalViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des hôpitaux"""
    queryset = Hopital.objects.all()
    # Ne pas définir permission_classes ici, utiliser get_permissions() à la place
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ville', 'actif']
    search_fields = ['nom', 'code_hopital', 'ville']
    ordering_fields = ['nom', 'ville', 'date_inscription']
    ordering = ['nom']
    
    def get_permissions(self):
        """
        Permissions personnalisées:
        - list, retrieve, proximite, specialistes, specialites: accès public (AllowAny)
        - autres actions (create, update, delete): authentification requise
        """
        if self.action in ['list', 'retrieve', 'proximite', 'specialistes', 'specialites']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return HopitalListSerializer
        return HopitalSerializer
    
    def perform_create(self, serializer):
        """Créer automatiquement un admin hôpital lors de la création d'un hôpital"""
        
        hopital = serializer.save()
        
        # Utiliser l'email de l'hôpital comme email de l'admin
        admin_email = hopital.email
        
        # Vérifier si un utilisateur avec cet email existe déjà
        if User.objects.filter(email=admin_email).exists():
            # Si l'utilisateur existe, on le met à jour pour être admin de cet hôpital
            admin_user = User.objects.get(email=admin_email)
            admin_user.role = 'admin_hopital'
            admin_user.nom = f"Admin {hopital.nom}"
            admin_user.set_password('admin123')  # Réinitialiser le mot de passe
            admin_user.actif = True
            admin_user.save()
        else:
            # Créer un nouvel utilisateur admin avec l'email de l'hôpital
            admin_user = User.objects.create_user(
                email=admin_email,
                nom=f"Admin {hopital.nom}",
                role='admin_hopital',
                password='admin123',
                actif=True
            )
        
        # Associer l'admin à l'hôpital
        hopital.admin_hopital = admin_user
        hopital.save()
        
        return hopital
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = get_user_from_request(self.request)
        
        # Pour les actions publiques, montrer seulement les hôpitaux actifs
        if self.action in ['list', 'retrieve', 'proximite', 'specialistes', 'specialites']:
            # Si pas authentifié, montrer seulement les actifs
            if not user or user.role not in ['super_admin', 'admin_hopital']:
                return queryset.filter(actif=True)
        
        # Si pas de request (génération du schéma Swagger), retourner tous les objets actifs
        if not user:
            return queryset.filter(actif=True)
        
        # Super admin voit tout (actifs et inactifs)
        if user.role == 'super_admin':
            return queryset
        
        # Admin hôpital voit seulement son hôpital (actif ou inactif)
        if user.role == 'admin_hopital':
            return queryset.filter(admin_hopital=user)
        
        # Autres rôles voient seulement les hôpitaux actifs (public)
        return queryset.filter(actif=True)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def proximite(self, request):
        """Récupère les hôpitaux proches d'une position"""
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        rayon = float(request.query_params.get('rayon', 50))  # km
        
        if not lat or not lng:
            return Response(
                {'error': 'lat et lng sont requis'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filtrage simple par proximité (pourrait être amélioré avec PostGIS)
        hopitaux = Hopital.objects.filter(actif=True, latitude__isnull=False, longitude__isnull=False)
        serializer = HopitalListSerializer(hopitaux, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def specialistes(self, request, pk=None):
        """Récupère les spécialistes d'un hôpital"""
        hopital = self.get_object()
        specialistes = Specialiste.objects.filter(hopital=hopital, actif=True)
        serializer = SpecialisteSerializer(specialistes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def specialites(self, request, pk=None):
        """Récupère les spécialités disponibles dans un hôpital"""
        hopital = self.get_object()
        specialites = Specialite.objects.filter(
            specialistes__hopital=hopital,
            specialistes__actif=True
        ).distinct()
        serializer = SpecialiteSerializer(specialites, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def mon_hopital(self, request):
        """Récupère l'hôpital de l'admin connecté"""
        if request.user.role != 'admin_hopital':
            return Response(
                {'error': 'Accès réservé aux administrateurs d\'hôpital'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            hopital = Hopital.objects.get(admin_hopital=request.user)
            serializer = self.get_serializer(hopital)
            return Response(serializer.data)
        except Hopital.DoesNotExist:
            return Response(
                {'error': 'Aucun hôpital trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def suspendre(self, request, pk=None):
        """Suspendre un hôpital (super admin seulement) et désactiver tous les utilisateurs liés"""
        if request.user.role != 'super_admin':
            return Response(
                {'error': 'Accès refusé'},
                status=status.HTTP_403_FORBIDDEN
            )
        hopital = self.get_object()
        hopital.actif = False
        hopital.save()
        
        # Désactiver l'administrateur de l'hôpital
        if hopital.admin_hopital:
            hopital.admin_hopital.actif = False
            hopital.admin_hopital.save()
        
        # Désactiver tous les spécialistes de l'hôpital
        specialistes = Specialiste.objects.filter(hopital=hopital)
        for specialiste in specialistes:
            specialiste.user.actif = False
            specialiste.user.save()
        
        return Response({
            'status': 'Hôpital suspendu avec succès',
            'message': f'Hôpital et {1 + specialistes.count()} utilisateur(s) désactivé(s)'
        })
    
    @action(detail=True, methods=['post'])
    def activer(self, request, pk=None):
        """Activer un hôpital (super admin seulement) et réactiver tous les utilisateurs liés"""
        if request.user.role != 'super_admin':
            return Response(
                {'error': 'Accès refusé'},
                status=status.HTTP_403_FORBIDDEN
            )
        hopital = self.get_object()
        hopital.actif = True
        hopital.save()
        
        # Réactiver l'administrateur de l'hôpital
        if hopital.admin_hopital:
            hopital.admin_hopital.actif = True
            hopital.admin_hopital.save()
        
        # Réactiver tous les spécialistes de l'hôpital
        specialistes = Specialiste.objects.filter(hopital=hopital)
        for specialiste in specialistes:
            specialiste.user.actif = True
            specialiste.user.save()
        
        return Response({
            'status': 'Hôpital activé avec succès',
            'message': f'Hôpital et {1 + specialistes.count()} utilisateur(s) réactivé(s)'
        })
    
    @action(detail=True, methods=['post'])
    def reset_admin_password(self, request, pk=None):
        """Réinitialiser le mot de passe de l'admin hôpital (super admin seulement)"""
        if request.user.role != 'super_admin':
            return Response(
                {'error': 'Accès refusé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        hopital = self.get_object()
        
        if not hopital.admin_hopital:
            return Response(
                {'error': 'Aucun administrateur associé à cet hôpital'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Réinitialiser le mot de passe à "admin123"
        hopital.admin_hopital.set_password('admin123')
        hopital.admin_hopital.save()
        
        return Response({
            'status': 'Mot de passe réinitialisé',
            'message': f'Le mot de passe de {hopital.admin_hopital.email} a été réinitialisé à "admin123"',
            'admin_email': hopital.admin_hopital.email
        })


class SpecialiteViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des spécialités"""
    queryset = Specialite.objects.all()
    serializer_class = SpecialiteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'code', 'description']
    ordering_fields = ['nom', 'code']
    ordering = ['nom']
    
    def get_permissions(self):
        """Seul le super admin peut modifier, recherche publique"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsSuperAdmin()]
        if self.action in ['recherche_avec_hopitaux']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # En lecture, montrer seulement les spécialités actives
        if self.action in ['list', 'retrieve']:
            queryset = queryset.filter(actif=True)
        return queryset
    
    @action(detail=False, methods=['get'])
    def recherche_avec_hopitaux(self, request):
        """Recherche de spécialités avec leurs hôpitaux et spécialistes"""
        query = request.query_params.get('q', '')
        
        if not query:
            return Response([])
        
        # Rechercher les spécialités
        specialites = Specialite.objects.filter(
            Q(nom__icontains=query) |
            Q(description__icontains=query),
            actif=True
        )[:5]  # Limiter à 5 résultats
        
        results = []
        for specialite in specialites:
            # Récupérer les spécialistes de cette spécialité
            specialistes = Specialiste.objects.filter(
                specialite=specialite,
                actif=True,
                hopital__actif=True
            ).select_related('hopital', 'user')
            
            # Grouper par hôpital
            hopitaux_dict = {}
            for spec in specialistes:
                hopital_id = spec.hopital.id
                if hopital_id not in hopitaux_dict:
                    hopitaux_dict[hopital_id] = {
                        'hopital_id': spec.hopital.id,
                        'hopital_nom': spec.hopital.nom,
                        'hopital_adresse': spec.hopital.adresse,
                        'hopital_ville': spec.hopital.ville,
                        'hopital_telephone': spec.hopital.telephone,
                        'hopital_latitude': float(spec.hopital.latitude) if spec.hopital.latitude else None,
                        'hopital_longitude': float(spec.hopital.longitude) if spec.hopital.longitude else None,
                        'specialistes': []
                    }
                
                hopitaux_dict[hopital_id]['specialistes'].append({
                    'id': spec.id,
                    'user_nom': spec.user.nom,
                    'titre': spec.titre,
                    'annees_experience': spec.annees_experience,
                    'tarif_consultation': str(spec.tarif_consultation),
                    'note_moyenne': str(spec.note_moyenne),
                    'accepte_nouveaux_patients': spec.accepte_nouveaux_patients,
                })
            
            if hopitaux_dict:  # Seulement inclure les spécialités avec des hôpitaux
                results.append({
                    'specialite_id': specialite.id,
                    'specialite_nom': specialite.nom,
                    'hopitaux': list(hopitaux_dict.values())
                })
        
        return Response(results)


class SpecialisteViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des spécialistes"""
    queryset = Specialiste.objects.all()
    serializer_class = SpecialisteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['hopital', 'specialite', 'actif']
    search_fields = ['user__nom', 'user__email', 'numero_ordre', 'titre']
    ordering_fields = ['user__nom', 'note_moyenne', 'created_at']
    ordering = ['user__nom']
    
    def get_permissions(self):
        """
        Permissions personnalisées:
        - list et retrieve: accès public (AllowAny)
        - autres actions: authentification requise
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = get_user_from_request(self.request)
        
        # Pour les actions publiques, montrer seulement les spécialistes actifs
        if self.action in ['list', 'retrieve']:
            return queryset.filter(actif=True)
        
        # Si pas de request (génération du schéma Swagger), retourner tous les spécialistes actifs
        if not user:
            return queryset.filter(actif=True)
        
        # Super admin voit tout
        if user.role == 'super_admin':
            return queryset
        
        # Admin hôpital voit seulement les spécialistes de son hôpital
        if user.role == 'admin_hopital':
            try:
                hopital = Hopital.objects.get(admin_hopital=user)
                return queryset.filter(hopital=hopital)
            except Hopital.DoesNotExist:
                return queryset.none()
        
        # Spécialiste voit seulement son propre profil
        if user.role == 'specialiste':
            return queryset.filter(user=user)
        
        # Autres rôles voient seulement les spécialistes actifs (public)
        return queryset.filter(actif=True)
    
    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        """Récupère ou met à jour le profil du spécialiste connecté"""
        if request.user.role != 'specialiste':
            return Response(
                {'error': 'Accès réservé aux spécialistes'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            specialiste = Specialiste.objects.get(user=request.user)
            
            if request.method == 'GET':
                serializer = self.get_serializer(specialiste)
                return Response(serializer.data)
            
            elif request.method == 'PATCH':
                serializer = self.get_serializer(specialiste, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Specialiste.DoesNotExist:
            return Response(
                {'error': 'Aucun profil spécialiste trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'], url_path='me/statistiques')
    def me_statistiques(self, request):
        """Récupère les statistiques du spécialiste connecté"""
        if request.user.role != 'specialiste':
            return Response(
                {'error': 'Accès réservé aux spécialistes'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            specialiste = Specialiste.objects.get(user=request.user)
            
            stats = {
                'nombre_consultations': ConsultationPF.objects.filter(
                    specialiste=specialiste
                ).count(),
                'nombre_rendez_vous': RendezVous.objects.filter(
                    specialiste=specialiste
                ).count(),
                'rendez_vous_en_attente': RendezVous.objects.filter(
                    specialiste=specialiste,
                    statut='en_attente'
                ).count(),
                'note_moyenne': float(specialiste.note_moyenne),
                'nombre_avis': specialiste.nombre_avis,
            }
            
            return Response(stats)
                
        except Specialiste.DoesNotExist:
            return Response(
                {'error': 'Aucun profil spécialiste trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def disponibilites(self, request, pk=None):
        """Récupère les disponibilités d'un spécialiste"""
        specialiste = self.get_object()
        disponibilites = DisponibiliteSpecialiste.objects.filter(
            specialiste=specialiste,
            actif=True
        )
        serializer = DisponibiliteSpecialisteSerializer(disponibilites, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def creneaux_libres(self, request, pk=None):
        """Récupère les créneaux libres d'un spécialiste pour une date"""
        specialiste = self.get_object()
        date_str = request.query_params.get('date')
        
        if not date_str:
            return Response(
                {'error': 'Le paramètre date est requis (format: YYYY-MM-DD)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Format de date invalide. Utilisez YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Récupérer les disponibilités pour le jour de la semaine
        jour_semaine = date_obj.strftime('%A').lower()  # lundi, mardi, etc.
        jours_fr = {
            'monday': 'lundi', 'tuesday': 'mardi', 'wednesday': 'mercredi',
            'thursday': 'jeudi', 'friday': 'vendredi', 'saturday': 'samedi', 'sunday': 'dimanche'
        }
        jour_semaine_fr = jours_fr.get(jour_semaine, jour_semaine)
        
        disponibilites = DisponibiliteSpecialiste.objects.filter(
            specialiste=specialiste,
            jour_semaine=jour_semaine_fr,
            actif=True
        )
        
        # Récupérer les rendez-vous déjà pris pour cette date
        # Utiliser une approche plus robuste pour gérer les timezones
        from django.utils import timezone as django_timezone
        
        # Créer les bornes de la journée en timezone local
        start_of_day = django_timezone.make_aware(
            datetime.combine(date_obj, datetime.min.time())
        )
        end_of_day = django_timezone.make_aware(
            datetime.combine(date_obj, datetime.max.time())
        )
        
        rendez_vous_pris = RendezVous.objects.filter(
            specialiste=specialiste,
            datetime__gte=start_of_day,
            datetime__lt=end_of_day,
            statut__in=['en_attente', 'confirme']
        )
        
        # Créer un set des heures prises pour une comparaison plus efficace
        heures_prises = set()
        for rdv in rendez_vous_pris:
            # Convertir en timezone local
            rdv_local = django_timezone.localtime(rdv.datetime)
            
            # Extraire seulement l'heure et minute
            heure_minute = rdv_local.time().replace(second=0, microsecond=0)
            heures_prises.add(heure_minute)
        
        # Générer les créneaux libres
        creneaux_libres = []
        for dispo in disponibilites:
            debut = datetime.combine(date_obj, dispo.heure_debut)
            fin = datetime.combine(date_obj, dispo.heure_fin)
            duree = timedelta(minutes=specialiste.duree_consultation)
            
            creneau = debut
            while creneau + duree <= fin:
                # Vérifier si ce créneau est pris en comparant seulement l'heure
                heure_creneau = creneau.time().replace(second=0, microsecond=0)
                is_taken = heure_creneau in heures_prises
                
                if not is_taken:
                    creneaux_libres.append({
                        'heure_debut': creneau.strftime('%H:%M'),
                        'heure_fin': (creneau + duree).strftime('%H:%M'),
                        'datetime': creneau.isoformat()
                    })
                creneau += duree
        
        return Response({'date': date_str, 'creneaux_libres': creneaux_libres})
    
    @action(detail=True, methods=['get'])
    def avis(self, request, pk=None):
        """Récupère les avis d'un spécialiste"""
        specialiste = self.get_object()
        avis = AvisSpecialiste.objects.filter(specialiste=specialiste)
        serializer = AvisSpecialisteSerializer(avis, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def statistiques(self, request, pk=None):
        """Récupère les statistiques d'un spécialiste"""
        specialiste = self.get_object()
        
        stats = {
            'nombre_consultations': ConsultationPF.objects.filter(
                specialiste=specialiste
            ).count(),
            'nombre_rendez_vous': RendezVous.objects.filter(
                specialiste=specialiste
            ).count(),
            'rendez_vous_en_attente': RendezVous.objects.filter(
                specialiste=specialiste,
                statut='en_attente'
            ).count(),
            'note_moyenne': float(specialiste.note_moyenne),
            'nombre_avis': specialiste.nombre_avis,
        }
        
        return Response(stats)
    
    @action(detail=True, methods=['patch'])
    def update_complete(self, request, pk=None):
        """Met à jour les informations complètes du spécialiste (utilisateur + spécialiste)"""
        specialiste = self.get_object()
        
        # Vérifier les permissions
        if request.user.role not in ['super_admin', 'admin_hopital']:
            if request.user.role != 'specialiste' or specialiste.user != request.user:
                return Response(
                    {'error': 'Accès refusé'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        # Séparer les données utilisateur et spécialiste
        user_data = {}
        specialiste_data = {}
        
        # Champs utilisateur
        if 'nom' in request.data:
            user_data['nom'] = request.data['nom']
        if 'email' in request.data:
            user_data['email'] = request.data['email']
        if 'password' in request.data and request.data['password']:
            user_data['password'] = request.data['password']
        
        # Champs spécialiste
        specialiste_fields = [
            'specialite', 'numero_ordre', 'titre', 'annees_experience', 'bio',
            'tarif_consultation', 'duree_consultation', 'accepte_nouveaux_patients',
            'consultation_en_ligne'
        ]
        
        for field in specialiste_fields:
            if field in request.data:
                specialiste_data[field] = request.data[field]
        
        try:
            # Mettre à jour l'utilisateur si nécessaire
            if user_data:
                user = specialiste.user
                for field, value in user_data.items():
                    if field == 'password':
                        user.set_password(value)
                    else:
                        setattr(user, field, value)
                user.save()
            
            # Mettre à jour le spécialiste si nécessaire
            if specialiste_data:
                for field, value in specialiste_data.items():
                    if field == 'specialite':
                        # Handle foreign key properly
                        try:
                            specialite_obj = Specialite.objects.get(id=value)
                            specialiste.specialite = specialite_obj
                        except Specialite.DoesNotExist:
                            return Response(
                                {'error': f'Spécialité avec l\'ID {value} non trouvée'},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                    else:
                        setattr(specialiste, field, value)
                specialiste.save()
            
            # Retourner les données mises à jour
            serializer = self.get_serializer(specialiste)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de la mise à jour: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class DisponibiliteSpecialisteViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des disponibilités des spécialistes"""
    queryset = DisponibiliteSpecialiste.objects.all()
    serializer_class = DisponibiliteSpecialisteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['specialiste', 'jour_semaine', 'actif']
    ordering_fields = ['jour_semaine', 'heure_debut']
    ordering = ['jour_semaine', 'heure_debut']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = get_user_from_request(self.request)
        
        # Si pas de request (génération du schéma Swagger), retourner tous les objets
        if not user:
            return queryset
        
        # Super admin et admin hôpital voient tout (filtré par hôpital)
        if user.role in ['super_admin', 'admin_hopital']:
            hopital_id = self.request.query_params.get('hopital')
            if hopital_id:
                queryset = queryset.filter(specialiste__hopital_id=hopital_id)
            return queryset
        
        # Spécialiste voit seulement ses propres disponibilités
        if user.role == 'specialiste':
            try:
                specialiste = Specialiste.objects.get(user=user)
                return queryset.filter(specialiste=specialiste)
            except Specialiste.DoesNotExist:
                return queryset.none()
        
        return queryset.none()
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Créer plusieurs disponibilités en une fois"""
        if request.user.role != 'specialiste':
            return Response(
                {'error': 'Accès réservé aux spécialistes'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            specialiste = Specialiste.objects.get(user=request.user)
        except Specialiste.DoesNotExist:
            return Response(
                {'error': 'Aucun profil spécialiste trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        disponibilites_data = request.data.get('disponibilites', [])
        created = []
        
        for dispo_data in disponibilites_data:
            dispo_data['specialiste'] = specialiste.id
            serializer = self.get_serializer(data=dispo_data)
            if serializer.is_valid():
                serializer.save()
                created.append(serializer.data)
            else:
                return Response(
                    {'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response({'created': created}, status=status.HTTP_201_CREATED)


class ProduitViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des produits"""
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categorie', 'prescription_requise', 'actif']
    search_fields = ['nom', 'code_barre', 'fabricant']
    ordering_fields = ['nom', 'prix_unitaire', 'created_at']
    ordering = ['nom']
    
    def get_permissions(self):
        """Super admin, pharmaciens et employés avec peut_gerer_stock peuvent modifier, recherche publique"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            user = get_user_from_request(self.request)
            if user and user.role in ['super_admin', 'pharmacien']:
                return [IsAuthenticated()]
            elif user and user.role == 'employe_pharmacie':
                try:
                    employe = EmployePharmacie.objects.get(user=user, actif=True)
                    if employe.peut_gerer_stock:
                        return [IsAuthenticated()]
                except EmployePharmacie.DoesNotExist:
                    pass
            return [IsAuthenticated(), IsSuperAdmin()]
        if self.action in ['recherche_avec_stocks', 'recherche']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # En lecture, montrer seulement les produits actifs
        if self.action in ['list', 'retrieve']:
            queryset = queryset.filter(actif=True)
        return queryset
    
    @action(detail=False, methods=['get'])
    def recherche(self, request):
        """Recherche avancée de produits"""
        query = request.query_params.get('q', '')
        categorie = request.query_params.get('categorie')
        
        queryset = Produit.objects.filter(actif=True)
        
        if query:
            queryset = queryset.filter(
                Q(nom__icontains=query) |
                Q(code_barre__icontains=query) |
                Q(description__icontains=query)
            )
        
        if categorie:
            queryset = queryset.filter(categorie=categorie)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recherche_avec_stocks(self, request):
        """Recherche de produits avec leurs stocks dans les pharmacies"""
        query = request.query_params.get('q', '')
        
        if not query:
            return Response([])
        
        # Séparer la requête en mots pour une recherche plus flexible
        mots = query.strip().split()
        
        # Construire une requête Q pour rechercher n'importe quel mot
        # Cela permet de trouver "Paracétamol 500mg" même si on cherche "Paracétamol 1g"
        q_objects = Q()
        for mot in mots:
            q_objects |= (
                Q(nom__icontains=mot) |
                Q(code_barre__icontains=mot) |
                Q(description__icontains=mot) |
                Q(fabricant__icontains=mot)
            )
        
        # Rechercher les produits avec au moins un des mots
        produits = Produit.objects.filter(
            q_objects,
            actif=True
        ).distinct()[:10]  # Limiter à 10 résultats
        
        results = []
        for produit in produits:
            # Récupérer les stocks disponibles pour ce produit
            stocks = StockProduit.objects.filter(
                produit=produit,
                quantite__gt=0,
                pharmacie__actif=True
            ).select_related('pharmacie')
            
            pharmacies_data = []
            for stock in stocks:
                pharmacies_data.append({
                    'pharmacie_id': stock.pharmacie.id,
                    'pharmacie_nom': stock.pharmacie.nom,
                    'pharmacie_adresse': stock.pharmacie.adresse,
                    'pharmacie_ville': stock.pharmacie.ville,
                    'pharmacie_telephone': stock.pharmacie.telephone,
                    'pharmacie_latitude': float(stock.pharmacie.latitude) if stock.pharmacie.latitude else None,
                    'pharmacie_longitude': float(stock.pharmacie.longitude) if stock.pharmacie.longitude else None,
                    'quantite': stock.quantite,
                    'prix_vente': str(stock.prix_vente),
                })
            
            if pharmacies_data:  # Seulement inclure les produits disponibles
                results.append({
                    'id': produit.id,
                    'nom': produit.nom,
                    'description': produit.description,
                    'categorie': produit.categorie,
                    'pharmacies': pharmacies_data
                })
        
        return Response(results)
    
    @action(detail=True, methods=['get'])
    def disponibilite(self, request, pk=None):
        """Récupère les pharmacies où le produit est disponible"""
        produit = self.get_object()
        stocks = StockProduit.objects.filter(
            produit=produit,
            quantite__gt=0
        ).select_related('pharmacie')
        
        pharmacies = [stock.pharmacie for stock in stocks]
        # Import ici pour éviter les imports circulaires
        from .serializers import PharmacieSerializer
        serializer = PharmacieSerializer(pharmacies, many=True)
        return Response(serializer.data)


class StockProduitViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des stocks de produits"""
    queryset = StockProduit.objects.all()
    serializer_class = StockProduitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['pharmacie', 'produit', 'date_expiration']
    search_fields = ['produit__nom', 'pharmacie__nom', 'numero_lot']
    ordering_fields = ['quantite', 'date_expiration']
    
    def get_permissions(self):
        """Vérifier les permissions pour les actions de modification"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Vérification personnalisée dans perform_create, perform_update, etc.
            return [IsAuthenticated()]
        return [IsAuthenticated()]
    
    def _can_manage_stock(self, user):
        """Vérifier si l'utilisateur peut gérer les stocks"""
        if user.role in ['super_admin', 'pharmacien']:
            return True
        
        if user.role == 'employe_pharmacie':
            try:
                employe = EmployePharmacie.objects.get(user=user, actif=True)
                return employe.peut_gerer_stock
            except EmployePharmacie.DoesNotExist:
                return False
        
        return False
    
    def perform_create(self, serializer):
        """Vérifier les permissions avant de créer un stock"""
        if not self._can_manage_stock(self.request.user):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Vous n'avez pas la permission de gérer les stocks.")
        serializer.save()
    
    def perform_update(self, serializer):
        """Vérifier les permissions avant de modifier un stock"""
        if not self._can_manage_stock(self.request.user):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Vous n'avez pas la permission de gérer les stocks.")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Vérifier les permissions avant de supprimer un stock"""
        if not self._can_manage_stock(self.request.user):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Vous n'avez pas la permission de gérer les stocks.")
        instance.delete()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = get_user_from_request(self.request)
        
        # Si pas de request (génération du schéma Swagger), retourner tous les objets
        if not user:
            return queryset
        
        # Super admin voit tout
        if user.role == 'super_admin':
            return queryset
        
        # Pharmacien voit seulement les stocks de ses pharmacies
        if user.role == 'pharmacien':
            pharmacies = Pharmacie.objects.filter(user=user, actif=True)
            return queryset.filter(pharmacie__in=pharmacies)
        
        # Employé voit les stocks de sa pharmacie (selon ses permissions)
        if user.role == 'employe_pharmacie':
            try:
                employe = EmployePharmacie.objects.get(user=user, actif=True)
                # L'employé peut voir les stocks s'il peut gérer le stock OU s'il peut vendre
                if employe.peut_gerer_stock or employe.peut_vendre:
                    return queryset.filter(pharmacie=employe.pharmacie)
            except EmployePharmacie.DoesNotExist:
                pass
        
        return queryset.none()
    
    @action(detail=False, methods=['get'])
    def alertes(self, request):
        """Récupère les stocks en alerte"""
        queryset = self.get_queryset()
        stocks = queryset.filter(Q(quantite__lte=F('seuil_alerte')) | Q(quantite__lte=0))
        serializer = self.get_serializer(stocks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def expirations(self, request):
        """Récupère les produits proches d'expiration"""
        queryset = self.get_queryset()
        date_limite = timezone.now().date() + timedelta(days=30)
        stocks = queryset.filter(
            date_expiration__isnull=False,
            date_expiration__lte=date_limite,
            date_expiration__gte=timezone.now().date(),
            quantite__gt=0
        )
        serializer = self.get_serializer(stocks, many=True)
        return Response(serializer.data)


class CommandePharmacieViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des commandes de pharmacie"""
    queryset = CommandePharmacie.objects.all()
    serializer_class = CommandePharmacieSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['patient', 'pharmacie', 'statut']
    search_fields = ['numero_commande', 'patient__nom', 'patient__prenom']
    ordering_fields = ['date_commande', 'montant_total']
    ordering = ['-date_commande']
    
    def get_serializer_class(self):
        """Utiliser le serializer de création pour POST"""
        if self.action == 'create':
            return CommandePharmacieCreateSerializer
        return CommandePharmacieSerializer
    
    def _can_manage_commandes(self, user):
        """Vérifier si l'utilisateur peut gérer les commandes"""
        if user.role in ['super_admin', 'pharmacien']:
            return True
        
        if user.role == 'employe_pharmacie':
            try:
                employe = EmployePharmacie.objects.get(user=user, actif=True)
                return employe.peut_traiter_commandes
            except EmployePharmacie.DoesNotExist:
                return False
        
        return False
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = get_user_from_request(self.request)
        
        # Si pas de request (génération du schéma Swagger), retourner tous les objets
        if not user:
            return queryset
        
        # Super admin voit tout
        if user.role == 'super_admin':
            return queryset
        
        # Pharmacien voit seulement les commandes de ses pharmacies
        if user.role == 'pharmacien':
            pharmacies = Pharmacie.objects.filter(user=user, actif=True)
            return queryset.filter(pharmacie__in=pharmacies)
        
        # Employé voit les commandes de sa pharmacie (selon ses permissions)
        if user.role == 'employe_pharmacie':
            try:
                employe = EmployePharmacie.objects.get(user=user, actif=True)
                # L'employé peut voir les commandes s'il a la permission peut_voir_commandes
                if employe.peut_voir_commandes:
                    return queryset.filter(pharmacie=employe.pharmacie)
            except EmployePharmacie.DoesNotExist:
                pass
        
        # Patient voit seulement ses propres commandes
        if hasattr(user, 'patient_profile'):
            patient = user.patient_profile
            return queryset.filter(patient=patient)
        
        return queryset.none()
    
    def perform_create(self, serializer):
        """Créer une commande - le patient et les lignes sont gérés par le serializer"""
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def confirmer(self, request, pk=None):
        """Confirmer une commande"""
        if not self._can_manage_commandes(request.user):
            return Response(
                {'error': 'Accès refusé'},
                status=status.HTTP_403_FORBIDDEN
            )
        commande = self.get_object()
        commande.statut = 'confirmee'
        commande.date_confirmation = timezone.now()
        commande.save()
        
        # Créer une notification pour le patient
        Notification.objects.create(
            user=commande.patient.user,
            type_notification='commande_confirmee',
            titre='Commande confirmée',
            message=f'Votre commande {commande.numero_commande} a été confirmée.',
            commande=commande
        )
        
        return Response({'status': 'Commande confirmée'})
    
    @action(detail=True, methods=['post'])
    def preparer(self, request, pk=None):
        """Marquer une commande comme préparée"""
        if not self._can_manage_commandes(request.user):
            return Response(
                {'error': 'Accès refusé'},
                status=status.HTTP_403_FORBIDDEN
            )
        commande = self.get_object()
        commande.statut = 'preparee'
        commande.date_preparation = timezone.now()
        commande.save()
        return Response({'status': 'Commande préparée'})
    
    @action(detail=True, methods=['post'])
    def prete(self, request, pk=None):
        """Marquer une commande comme prête"""
        if not self._can_manage_commandes(request.user):
            return Response(
                {'error': 'Accès refusé'},
                status=status.HTTP_403_FORBIDDEN
            )
        commande = self.get_object()
        commande.statut = 'prete'
        commande.date_prete = timezone.now()
        commande.save()
        
        # Créer une notification pour le patient
        Notification.objects.create(
            user=commande.patient.user,
            type_notification='commande_prete',
            titre='Commande prête',
            message=f'Votre commande {commande.numero_commande} est prête à être récupérée.',
            commande=commande
        )
        
        return Response({'status': 'Commande prête'})
    
    @action(detail=True, methods=['post'])
    def recuperer(self, request, pk=None):
        """Marquer une commande comme récupérée"""
        if not self._can_manage_commandes(request.user):
            return Response(
                {'error': 'Accès refusé'},
                status=status.HTTP_403_FORBIDDEN
            )
        commande = self.get_object()
        commande.statut = 'recuperee'
        commande.date_recuperation = timezone.now()
        commande.save()
        return Response({'status': 'Commande récupérée'})
    
    @action(detail=True, methods=['post'])
    def annuler(self, request, pk=None):
        """Annuler une commande"""
        commande = self.get_object()
        
        # Le patient peut annuler ses propres commandes en attente
        if hasattr(request.user, 'patient_profile') and commande.patient == request.user.patient_profile:
            if commande.statut not in ['en_attente', 'confirmee']:
                return Response(
                    {'error': 'Impossible d\'annuler cette commande'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif not self._can_manage_commandes(request.user):
            return Response(
                {'error': 'Accès refusé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        commande.statut = 'annulee'
        commande.save()
        return Response({'status': 'Commande annulée'})

    @action(detail=True, methods=['patch'], url_path='update-with-notification')
    def update_with_notification(self, request, pk=None):
        """Mettre à jour le statut d'une commande avec notification personnalisée"""
        if not self._can_manage_commandes(request.user):
            return Response(
                {'error': 'Accès refusé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        commande = self.get_object()
        new_statut = request.data.get('statut')
        message_patient = request.data.get('message_patient', '')
        
        if not new_statut:
            return Response(
                {'error': 'Le statut est obligatoire'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Valider le statut
        valid_statuts = ['confirmee', 'preparee', 'prete', 'recuperee', 'annulee']
        if new_statut not in valid_statuts:
            return Response(
                {'error': f'Statut invalide. Statuts valides: {", ".join(valid_statuts)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mettre à jour le statut et les dates correspondantes
        old_statut = commande.statut
        commande.statut = new_statut
        
        if new_statut == 'confirmee':
            commande.date_confirmation = timezone.now()
        elif new_statut == 'preparee':
            commande.date_preparation = timezone.now()
        elif new_statut == 'prete':
            commande.date_prete = timezone.now()
        elif new_statut == 'recuperee':
            commande.date_recuperation = timezone.now()
        
        # Ajouter le message du pharmacien aux notes
        if message_patient:
            if commande.notes_pharmacie:
                commande.notes_pharmacie += f"\n\n[{timezone.now().strftime('%d/%m/%Y %H:%M')}] {message_patient}"
            else:
                commande.notes_pharmacie = f"[{timezone.now().strftime('%d/%m/%Y %H:%M')}] {message_patient}"
        
        commande.save()
        
        # Créer une notification pour le patient si il a un compte utilisateur
        if hasattr(commande.patient, 'user') and commande.patient.user:
            # Déterminer le type de notification et le titre
            notification_config = {
                'confirmee': {
                    'type': 'commande_confirmee',
                    'titre': 'Commande confirmée',
                    'message_default': f'Votre commande {commande.numero_commande} a été confirmée.'
                },
                'preparee': {
                    'type': 'commande_confirmee',
                    'titre': 'Commande en préparation',
                    'message_default': f'Votre commande {commande.numero_commande} est en cours de préparation.'
                },
                'prete': {
                    'type': 'commande_prete',
                    'titre': 'Commande prête',
                    'message_default': f'Votre commande {commande.numero_commande} est prête à être récupérée.'
                },
                'recuperee': {
                    'type': 'commande_confirmee',
                    'titre': 'Commande récupérée',
                    'message_default': f'Votre commande {commande.numero_commande} a été récupérée avec succès.'
                },
                'annulee': {
                    'type': 'commande_confirmee',
                    'titre': 'Commande annulée',
                    'message_default': f'Votre commande {commande.numero_commande} a été annulée.'
                }
            }
            
            config = notification_config.get(new_statut)
            if config:
                # Utiliser le message personnalisé ou le message par défaut
                notification_message = message_patient if message_patient else config['message_default']
                
                Notification.objects.create(
                    user=commande.patient.user,
                    type_notification=config['type'],
                    titre=config['titre'],
                    message=notification_message,
                    commande=commande,
                    data={
                        'statut_precedent': old_statut,
                        'nouveau_statut': new_statut,
                        'pharmacie_nom': commande.pharmacie.nom,
                        'message_pharmacien': message_patient
                    }
                )
        
        # Sérialiser la commande mise à jour
        serializer = self.get_serializer(commande)
        return Response({
            'status': 'Commande mise à jour avec succès',
            'commande': serializer.data,
            'notification_envoyee': hasattr(commande.patient, 'user') and commande.patient.user is not None
        })
    
    
    @action(detail=False, methods=['get'])
    def mes_commandes(self, request):
        """Récupère les commandes du patient connecté"""
        if not hasattr(request.user, 'patient_profile'):
            return Response(
                {'error': 'Accès réservé aux patients'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        patient = request.user.patient_profile
        commandes = CommandePharmacie.objects.filter(patient=patient)
        serializer = self.get_serializer(commandes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pharmacie(self, request, pk=None):
        """Récupère les commandes d'une pharmacie"""
        pharmacie_id = request.query_params.get('pharmacie_id') or pk
        
        if request.user.role not in ['super_admin', 'pharmacien']:
            return Response(
                {'error': 'Accès refusé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if request.user.role == 'pharmacien':
            pharmacies = Pharmacie.objects.filter(user=request.user, actif=True)
            try:
                pharmacie = pharmacies.get(id=pharmacie_id)
            except Pharmacie.DoesNotExist:
                return Response(
                    {'error': 'Pharmacie non trouvée'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            try:
                pharmacie = Pharmacie.objects.get(id=pharmacie_id)
            except Pharmacie.DoesNotExist:
                return Response(
                    {'error': 'Pharmacie non trouvée'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        commandes = CommandePharmacie.objects.filter(pharmacie=pharmacie)
        serializer = self.get_serializer(commandes, many=True)
        return Response(serializer.data)


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des notifications"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type_notification', 'lu']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Chaque utilisateur voit seulement ses propres notifications
        user = get_user_from_request(self.request)
        if not user:
            return Notification.objects.none()
        return Notification.objects.filter(user=user)
    
    @action(detail=True, methods=['post'])
    def marquer_lu(self, request, pk=None):
        """Marquer une notification comme lue"""
        notification = self.get_object()
        if notification.user != request.user:
            return Response(
                {'error': 'Accès refusé'},
                status=status.HTTP_403_FORBIDDEN
            )
        notification.lu = True
        notification.date_lecture = timezone.now()
        notification.save()
        return Response({'status': 'Notification marquée comme lue'})
    
    @action(detail=False, methods=['post'])
    def marquer_toutes_lues(self, request):
        """Marquer toutes les notifications comme lues"""
        Notification.objects.filter(
            user=request.user,
            lu=False
        ).update(lu=True, date_lecture=timezone.now())
        return Response({'status': 'Toutes les notifications ont été marquées comme lues'})
    
    @action(detail=False, methods=['get'])
    def non_lues(self, request):
        """Récupère le nombre de notifications non lues"""
        count = Notification.objects.filter(user=request.user, lu=False).count()
        return Response({'count': count})


class RapportConsultationViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des rapports de consultation"""
    queryset = RapportConsultation.objects.all()
    serializer_class = RapportConsultationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrMedicalStaff]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['consultation', 'envoye_patient']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = get_user_from_request(self.request)
        
        # Si pas de request (génération du schéma Swagger), retourner tous les objets
        if not user:
            return queryset
        
        # Super admin voit tout
        if user.role == 'super_admin':
            return queryset
        
        # Admin hôpital voit les rapports de son hôpital
        if user.role == 'admin_hopital':
            try:
                hopital = Hopital.objects.get(admin_hopital=user)
                return queryset.filter(consultation__hopital=hopital)
            except Hopital.DoesNotExist:
                return queryset.none()
        
        # Spécialiste voit seulement ses propres rapports
        if user.role == 'specialiste':
            try:
                specialiste = Specialiste.objects.get(user=user)
                return queryset.filter(consultation__specialiste=specialiste)
            except Specialiste.DoesNotExist:
                return queryset.none()
        
        # Patient voit seulement les rapports de ses consultations
        if hasattr(user, 'patient_profile'):
            patient = user.patient_profile
            return queryset.filter(consultation__patient=patient)
        
        return queryset.none()
    
    @action(detail=True, methods=['post'])
    def envoyer_patient(self, request, pk=None):
        """Envoyer le rapport au patient"""
        rapport = self.get_object()
        
        if request.user.role not in ['super_admin', 'admin_hopital', 'specialiste']:
            return Response(
                {'error': 'Accès refusé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        rapport.envoye_patient = True
        rapport.date_envoi = timezone.now()
        rapport.save()
        
        # Créer une notification pour le patient
        Notification.objects.create(
            user=rapport.consultation.patient.user,
            type_notification='consultation_rapport',
            titre='Rapport de consultation disponible',
            message=f'Le rapport de votre consultation du {rapport.consultation.date.strftime("%d/%m/%Y")} est disponible.',
            rendez_vous=rapport.consultation.rendez_vous,
            data={'rapport_id': rapport.id}
        )
        
        return Response({'status': 'Rapport envoyé au patient'})


class AvisSpecialisteViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des avis sur les spécialistes"""
    queryset = AvisSpecialiste.objects.all()
    serializer_class = AvisSpecialisteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['specialiste', 'patient']
    ordering_fields = ['created_at', 'note']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # En lecture, tout le monde peut voir les avis publics
        if self.action in ['list', 'retrieve']:
            return queryset
        
        # En écriture, seuls les patients peuvent créer des avis
        return queryset
    
    def perform_create(self, serializer):
        """Créer un avis et mettre à jour la note moyenne du spécialiste"""
        from rest_framework import serializers as drf_serializers
        if not hasattr(self.request.user, 'patient_profile'):
            raise drf_serializers.ValidationError('Seuls les patients peuvent donner un avis')
        
        patient = self.request.user.patient_profile
        serializer.save(patient=patient)
        
        # Mettre à jour la note moyenne du spécialiste
        specialiste = serializer.instance.specialiste
        avis = AvisSpecialiste.objects.filter(specialiste=specialiste)
        note_moyenne = avis.aggregate(avg_note=Avg('note'))['avg_note'] or 0
        nombre_avis = avis.count()
        
        specialiste.note_moyenne = note_moyenne
        specialiste.nombre_avis = nombre_avis
        specialiste.save()


class VentePharmacieViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des ventes de pharmacie"""
    queryset = VentePharmacie.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['pharmacie', 'mode_paiement', 'vendeur']
    search_fields = ['numero_vente', 'nom_client', 'telephone_client']
    ordering_fields = ['date_vente', 'montant_total']
    ordering = ['-date_vente']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return VentePharmacieCreateSerializer
        return VentePharmacieSerializer
    
    def get_queryset(self):
        # Pour la génération du schéma Swagger
        if getattr(self, 'swagger_fake_view', False):
            return VentePharmacie.objects.none()
            
        queryset = super().get_queryset()
        
        # Si l'utilisateur n'est pas authentifié
        if not self.request.user.is_authenticated:
            return VentePharmacie.objects.none()
        
        # Filtrer par pharmacie si l'utilisateur est pharmacien ou employé
        if self.request.user.role in ['pharmacien', 'employe_pharmacie']:
            if self.request.user.role == 'pharmacien':
                try:
                    pharmacie = Pharmacie.objects.get(user=self.request.user)
                    queryset = queryset.filter(pharmacie=pharmacie)
                except Pharmacie.DoesNotExist:
                    queryset = queryset.none()
            elif self.request.user.role == 'employe_pharmacie':
                try:
                    employe = EmployePharmacie.objects.get(user=self.request.user)
                    # Vérifier si l'employé a la permission de voir les ventes
                    if employe.peut_vendre:
                        queryset = queryset.filter(pharmacie=employe.pharmacie)
                    else:
                        queryset = queryset.none()
                except EmployePharmacie.DoesNotExist:
                    queryset = queryset.none()
        else:
            queryset = queryset.none()
        
        # Filtrer par période si spécifiée
        periode = self.request.query_params.get('periode')
        if periode:
            from datetime import datetime, timedelta
            from django.utils import timezone
            
            now = timezone.now()
            today = now.date()
            
            if periode == 'aujourd_hui':
                # Pour aujourd'hui, utiliser un range de datetime
                start_of_day = timezone.make_aware(datetime.combine(today, datetime.min.time()))
                end_of_day = start_of_day + timedelta(days=1)
                queryset = queryset.filter(date_vente__gte=start_of_day, date_vente__lt=end_of_day)
            elif periode == 'cette_semaine':
                # Début de la semaine (lundi)
                start_week = today - timedelta(days=today.weekday())
                start_of_week = timezone.make_aware(datetime.combine(start_week, datetime.min.time()))
                queryset = queryset.filter(date_vente__gte=start_of_week)
            elif periode == 'ce_mois':
                # Début du mois
                start_month = today.replace(day=1)
                start_of_month = timezone.make_aware(datetime.combine(start_month, datetime.min.time()))
                queryset = queryset.filter(date_vente__gte=start_of_month)
            elif periode == 'cette_annee':
                # Début de l'année
                start_year = today.replace(month=1, day=1)
                start_of_year = timezone.make_aware(datetime.combine(start_year, datetime.min.time()))
                queryset = queryset.filter(date_vente__gte=start_of_year)
        
        return queryset
    
    def perform_create(self, serializer):
        """Attribuer automatiquement le vendeur lors de la création d'une vente"""
        # Vérifier les permissions pour les employés
        if self.request.user.role == 'employe_pharmacie':
            try:
                employe = EmployePharmacie.objects.get(user=self.request.user)
                if not employe.peut_vendre:
                    from rest_framework.exceptions import PermissionDenied
                    raise PermissionDenied("Vous n'avez pas la permission d'effectuer des ventes.")
            except EmployePharmacie.DoesNotExist:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("Profil employé non trouvé.")
        
        # Le vendeur est automatiquement l'utilisateur connecté
        serializer.save(vendeur=self.request.user)
    
    @swagger_auto_schema(
        operation_description="Obtenir les statistiques des ventes manuelles",
        manual_parameters=[
            openapi.Parameter(
                'periode',
                openapi.IN_QUERY,
                description="Période de filtrage (aujourd_hui, cette_semaine, ce_mois, cette_annee)",
                type=openapi.TYPE_STRING,
                enum=['aujourd_hui', 'cette_semaine', 'ce_mois', 'cette_annee']
            ),
            openapi.Parameter(
                'pharmacie',
                openapi.IN_QUERY,
                description="ID de la pharmacie (automatique pour les pharmaciens)",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: openapi.Response(
                description="Statistiques des ventes",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_ventes': openapi.Schema(type=openapi.TYPE_INTEGER, description="Nombre total de ventes"),
                        'chiffre_affaires_total': openapi.Schema(type=openapi.TYPE_NUMBER, description="Chiffre d'affaires total"),
                        'panier_moyen': openapi.Schema(type=openapi.TYPE_NUMBER, description="Panier moyen"),
                        'par_periode': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="Statistiques par période",
                            additional_properties=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'nombre_ventes': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'chiffre_affaires': openapi.Schema(type=openapi.TYPE_NUMBER),
                                }
                            )
                        ),
                        'top_produits': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'produit__nom': openapi.Schema(type=openapi.TYPE_STRING),
                                    'quantite_totale': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'chiffre_affaires': openapi.Schema(type=openapi.TYPE_NUMBER),
                                }
                            )
                        ),
                        'modes_paiement': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'mode_paiement': openapi.Schema(type=openapi.TYPE_STRING),
                                    'nombre': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'montant': openapi.Schema(type=openapi.TYPE_NUMBER),
                                }
                            )
                        ),
                    }
                )
            )
        },
        tags=['Ventes Manuelles - Statistiques']
    )
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """Obtenir les statistiques des ventes"""
        queryset = self.get_queryset()
        
        from django.db.models import Sum, Count, Avg
        from datetime import datetime, timedelta
        from django.utils import timezone
        
        today = timezone.now().date()
        
        # Statistiques générales
        stats = {
            'total_ventes': queryset.count(),
            'chiffre_affaires_total': float(queryset.aggregate(
                total=Sum('montant_total')
            )['total'] or 0),
            'panier_moyen': float(queryset.aggregate(
                moyenne=Avg('montant_total')
            )['moyenne'] or 0),
        }
        
        # Statistiques par période - corriger les filtres de date
        periodes_dates = {
            'aujourd_hui': today,
            'cette_semaine': today - timedelta(days=today.weekday()),
            'ce_mois': today.replace(day=1),
            'cette_annee': today.replace(month=1, day=1),
        }
        
        stats['par_periode'] = {}
        for periode_nom, date_debut in periodes_dates.items():
            if periode_nom == 'aujourd_hui':
                # Pour aujourd'hui, utiliser un range de datetime
                date_debut_dt = timezone.make_aware(datetime.combine(date_debut, datetime.min.time()))
                date_fin_dt = date_debut_dt + timedelta(days=1)
                qs = queryset.filter(
                    date_vente__gte=date_debut_dt,
                    date_vente__lt=date_fin_dt
                )
            else:
                # Pour les autres périodes
                date_debut_dt = timezone.make_aware(datetime.combine(date_debut, datetime.min.time()))
                qs = queryset.filter(date_vente__gte=date_debut_dt)
            
            stats['par_periode'][periode_nom] = {
                'nombre_ventes': qs.count(),
                'chiffre_affaires': float(qs.aggregate(
                    total=Sum('montant_total')
                )['total'] or 0),
            }
        
        # Top produits vendus
        from django.db.models import F
        top_produits = LigneVente.objects.filter(
            vente__in=queryset
        ).values(
            'produit__nom'
        ).annotate(
            quantite_totale=Sum('quantite'),
            chiffre_affaires=Sum('prix_total')
        ).order_by('-quantite_totale')[:10]
        
        stats['top_produits'] = list(top_produits)
        
        # Répartition par mode de paiement
        modes_paiement = queryset.values('mode_paiement').annotate(
            nombre=Count('id'),
            montant=Sum('montant_total')
        ).order_by('-nombre')
        
        stats['modes_paiement'] = list(modes_paiement)
        
        return Response(stats)
    
    @swagger_auto_schema(
        operation_description="Obtenir les revenus combinés (ventes manuelles + commandes récupérées)",
        responses={
            200: openapi.Response(
                description="Revenus combinés avec statistiques détaillées",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'statistiques_par_periode': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="Statistiques par période",
                            additional_properties=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'chiffre_affaires_total': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'nombre_ventes_manuelles': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'nombre_commandes': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'nombre_total': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'ca_ventes_manuelles': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'ca_commandes': openapi.Schema(type=openapi.TYPE_NUMBER),
                                }
                            )
                        ),
                        'panier_moyen': openapi.Schema(type=openapi.TYPE_NUMBER, description="Panier moyen global"),
                        'croissance_mois': openapi.Schema(type=openapi.TYPE_NUMBER, description="Croissance mensuelle en %"),
                        'ventes_par_jour': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            description="Données des 7 derniers jours",
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                                    'montant_total': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'ventes_manuelles': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'commandes': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'total_transactions': openapi.Schema(type=openapi.TYPE_INTEGER),
                                }
                            )
                        ),
                    }
                )
            )
        },
        tags=['Revenus Combinés']
    )
    @action(detail=False, methods=['get'])
    def revenus_combines(self, request):
        """Obtenir les revenus combinés (commandes + ventes manuelles)"""
        from django.db.models import Sum, Count, Q
        from datetime import datetime, timedelta
        from django.utils import timezone
        
        # Filtrer par pharmacie si l'utilisateur est pharmacien
        pharmacie_id = None
        if request.user.role == 'pharmacien':
            try:
                pharmacie = Pharmacie.objects.get(user=request.user)
                pharmacie_id = pharmacie.id
            except Pharmacie.DoesNotExist:
                return Response({'error': 'Pharmacie non trouvée'}, status=404)
        
        today = timezone.now().date()
        
        # Obtenir les ventes manuelles
        ventes_queryset = self.get_queryset()
        if pharmacie_id:
            ventes_queryset = ventes_queryset.filter(pharmacie_id=pharmacie_id)
        
        # Obtenir les commandes récupérées
        commandes_queryset = CommandePharmacie.objects.filter(statut='recuperee')
        if pharmacie_id:
            commandes_queryset = commandes_queryset.filter(pharmacie_id=pharmacie_id)
        
        # Définir les périodes actuelles
        periodes = {
            'aujourd_hui': today,
            'cette_semaine': today - timedelta(days=today.weekday()),
            'ce_mois': today.replace(day=1),
            'cette_annee': today.replace(month=1, day=1),
        }
        
        # Définir les périodes passées
        semaine_passee_debut = today - timedelta(days=today.weekday() + 7)
        semaine_passee_fin = today - timedelta(days=today.weekday() + 1)
        
        mois_passe_debut = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        mois_passe_fin = today.replace(day=1) - timedelta(days=1)
        
        annee_passee_debut = today.replace(month=1, day=1, year=today.year - 1)
        annee_passee_fin = today.replace(month=12, day=31, year=today.year - 1)
        
        periodes_passees = {
            'semaine_passee': (semaine_passee_debut, semaine_passee_fin),
            'mois_passe': (mois_passe_debut, mois_passe_fin),
            'annee_passee': (annee_passee_debut, annee_passee_fin),
        }
        
        stats = {}
        
        # Calculer les stats pour les périodes actuelles
        for periode_nom, date_debut in periodes.items():
            # Ventes manuelles pour cette période - utiliser datetime ranges
            if periode_nom == 'aujourd_hui':
                # Pour aujourd'hui, utiliser un range de datetime
                date_debut_dt = timezone.make_aware(datetime.combine(date_debut, datetime.min.time()))
                date_fin_dt = date_debut_dt + timedelta(days=1)
                ventes_periode = ventes_queryset.filter(
                    date_vente__gte=date_debut_dt,
                    date_vente__lt=date_fin_dt
                )
                commandes_periode = commandes_queryset.filter(
                    date_recuperation__gte=date_debut_dt,
                    date_recuperation__lt=date_fin_dt
                )
            else:
                # Pour les autres périodes, utiliser le filtre normal
                date_debut_dt = timezone.make_aware(datetime.combine(date_debut, datetime.min.time()))
                ventes_periode = ventes_queryset.filter(date_vente__gte=date_debut_dt)
                commandes_periode = commandes_queryset.filter(date_recuperation__gte=date_debut_dt)
            
            ca_ventes = ventes_periode.aggregate(total=Sum('montant_total'))['total'] or 0
            nb_ventes = ventes_periode.count()
            
            # Commandes pour cette période (utiliser date_recuperation)
            ca_commandes = commandes_periode.aggregate(total=Sum('montant_total'))['total'] or 0
            nb_commandes = commandes_periode.count()
            
            # Totaux combinés
            stats[periode_nom] = {
                'chiffre_affaires_total': float(ca_ventes) + float(ca_commandes),
                'nombre_ventes_manuelles': nb_ventes,
                'nombre_commandes': nb_commandes,
                'nombre_total': nb_ventes + nb_commandes,
                'ca_ventes_manuelles': float(ca_ventes),
                'ca_commandes': float(ca_commandes),
            }
        
        # Calculer les stats pour les périodes passées
        for periode_nom, (date_debut, date_fin) in periodes_passees.items():
            date_debut_dt = timezone.make_aware(datetime.combine(date_debut, datetime.min.time()))
            date_fin_dt = timezone.make_aware(datetime.combine(date_fin, datetime.max.time()))
            
            ventes_periode = ventes_queryset.filter(
                date_vente__gte=date_debut_dt,
                date_vente__lte=date_fin_dt
            )
            commandes_periode = commandes_queryset.filter(
                date_recuperation__gte=date_debut_dt,
                date_recuperation__lte=date_fin_dt
            )
            
            ca_ventes = ventes_periode.aggregate(total=Sum('montant_total'))['total'] or 0
            nb_ventes = ventes_periode.count()
            
            ca_commandes = commandes_periode.aggregate(total=Sum('montant_total'))['total'] or 0
            nb_commandes = commandes_periode.count()
            
            stats[periode_nom] = {
                'chiffre_affaires_total': float(ca_ventes) + float(ca_commandes),
                'nombre_ventes_manuelles': nb_ventes,
                'nombre_commandes': nb_commandes,
                'nombre_total': nb_ventes + nb_commandes,
                'ca_ventes_manuelles': float(ca_ventes),
                'ca_commandes': float(ca_commandes),
            }
        
        # Calcul du panier moyen global
        total_transactions = stats['cette_annee']['nombre_total']
        total_ca = stats['cette_annee']['chiffre_affaires_total']
        panier_moyen = total_ca / total_transactions if total_transactions > 0 else 0
        
        # Croissance mensuelle
        ca_mois_actuel = stats['ce_mois']['chiffre_affaires_total']
        
        # Mois précédent
        mois_precedent_debut = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        mois_precedent_fin = today.replace(day=1) - timedelta(days=1)
        
        # Convertir en datetime avec timezone
        mois_precedent_debut_dt = timezone.make_aware(datetime.combine(mois_precedent_debut, datetime.min.time()))
        mois_precedent_fin_dt = timezone.make_aware(datetime.combine(mois_precedent_fin, datetime.max.time()))
        
        ventes_mois_precedent = ventes_queryset.filter(
            date_vente__gte=mois_precedent_debut_dt,
            date_vente__lte=mois_precedent_fin_dt
        )
        commandes_mois_precedent = commandes_queryset.filter(
            date_recuperation__gte=mois_precedent_debut_dt,
            date_recuperation__lte=mois_precedent_fin_dt
        )
        
        ca_ventes_precedent = ventes_mois_precedent.aggregate(total=Sum('montant_total'))['total'] or 0
        ca_commandes_precedent = commandes_mois_precedent.aggregate(total=Sum('montant_total'))['total'] or 0
        ca_mois_precedent = float(ca_ventes_precedent) + float(ca_commandes_precedent)
        
        croissance_mois = 0
        if ca_mois_precedent > 0:
            croissance_mois = ((ca_mois_actuel - ca_mois_precedent) / ca_mois_precedent) * 100
        elif ca_mois_actuel > 0:
            croissance_mois = 100
        
        # Données pour graphique des 7 derniers jours
        ventes_par_jour = []
        for i in range(6, -1, -1):
            date_jour = today - timedelta(days=i)
            
            # Convertir en datetime avec timezone pour les filtres
            date_debut_dt = timezone.make_aware(datetime.combine(date_jour, datetime.min.time()))
            date_fin_dt = date_debut_dt + timedelta(days=1)
            
            # Ventes manuelles du jour
            ventes_jour = ventes_queryset.filter(
                date_vente__gte=date_debut_dt,
                date_vente__lt=date_fin_dt
            )
            ca_ventes_jour = ventes_jour.aggregate(total=Sum('montant_total'))['total'] or 0
            nb_ventes_jour = ventes_jour.count()
            
            # Commandes du jour
            commandes_jour = commandes_queryset.filter(
                date_recuperation__gte=date_debut_dt,
                date_recuperation__lt=date_fin_dt
            )
            ca_commandes_jour = commandes_jour.aggregate(total=Sum('montant_total'))['total'] or 0
            nb_commandes_jour = commandes_jour.count()
            
            ventes_par_jour.append({
                'date': date_jour.strftime('%Y-%m-%d'),
                'montant_total': float(ca_ventes_jour) + float(ca_commandes_jour),
                'ventes_manuelles': nb_ventes_jour,
                'commandes': nb_commandes_jour,
                'total_transactions': nb_ventes_jour + nb_commandes_jour
            })
        
        return Response({
            'statistiques_par_periode': stats,
            'panier_moyen': panier_moyen,
            'croissance_mois': croissance_mois,
            'ventes_par_jour': ventes_par_jour
        })
    
    @action(detail=True, methods=['get'])
    def recu(self, request, pk=None):
        """Générer un reçu de vente"""
        vente = self.get_object()
        
        # Données pour le reçu
        recu_data = {
            'vente': VentePharmacieSerializer(vente).data,
            'pharmacie': {
                'nom': vente.pharmacie.nom,
                'adresse': vente.pharmacie.adresse,
                'telephone': vente.pharmacie.telephone,
                'email': vente.pharmacie.email,
            },
            'date_generation': timezone.now(),
        }
        
        return Response(recu_data)
    
    @swagger_auto_schema(
        operation_description="Annuler une vente et restituer le stock",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['motif_annulation'],
            properties={
                'motif_annulation': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Motif de l'annulation (obligatoire)"
                ),
            }
        ),
        responses={
            200: openapi.Response(
                description="Vente annulée avec succès",
                schema=VentePharmacieSerializer
            ),
            400: "Erreur de validation",
            403: "Permission refusée",
        },
        tags=['Ventes Manuelles']
    )
    @action(detail=True, methods=['post'])
    def annuler(self, request, pk=None):
        """Annuler une vente et restituer le stock"""
        vente = self.get_object()
        
        # Vérifier les permissions
        user = request.user
        if user.role == 'employe_pharmacie':
            try:
                employe = EmployePharmacie.objects.get(user=user)
                if not employe.peut_annuler_vente:
                    return Response(
                        {'error': "Vous n'avez pas la permission d'annuler des ventes."},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except EmployePharmacie.DoesNotExist:
                return Response(
                    {'error': "Employé non trouvé."},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        # Vérifier que la vente n'est pas déjà annulée
        if vente.annulee:
            return Response(
                {'error': 'Cette vente est déjà annulée.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Récupérer le motif d'annulation
        motif_annulation = request.data.get('motif_annulation', '').strip()
        if not motif_annulation:
            return Response(
                {'error': 'Le motif d\'annulation est obligatoire.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Restituer le stock pour chaque ligne de vente
        from django.db import transaction
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            with transaction.atomic():
                lignes = vente.lignes.all()
                logger.info(f"Annulation de la vente {vente.numero_vente} avec {lignes.count()} lignes")
                
                for ligne in lignes:
                    # Utiliser directement le stock_produit référencé dans la ligne
                    stock = ligne.stock_produit
                    quantite_avant = stock.quantite
                    
                    # Restituer la quantité
                    stock.quantite += ligne.quantite
                    stock.save()
                    
                    logger.info(f"Stock {stock.id} - Produit {ligne.produit.nom}: {quantite_avant} + {ligne.quantite} = {stock.quantite}")
                
                # Marquer la vente comme annulée
                vente.annulee = True
                vente.motif_annulation = motif_annulation
                vente.date_annulation = timezone.now()
                vente.annulee_par = user
                vente.save()
                
                logger.info(f"Vente {vente.numero_vente} annulée avec succès")
        
        except Exception as e:
            logger.error(f"Erreur lors de l'annulation de la vente: {str(e)}")
            return Response(
                {'error': f'Erreur lors de l\'annulation de la vente: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        serializer = VentePharmacieSerializer(vente)
        return Response(serializer.data)


class LigneVenteViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour consulter les lignes de vente (lecture seule)"""
    queryset = LigneVente.objects.all()
    serializer_class = LigneVenteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['vente', 'produit']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Pour la génération du schéma Swagger
        if getattr(self, 'swagger_fake_view', False):
            return LigneVente.objects.none()
            
        queryset = super().get_queryset()
        
        # Si l'utilisateur n'est pas authentifié
        if not self.request.user.is_authenticated:
            return LigneVente.objects.none()
        
        # Filtrer par pharmacie si l'utilisateur est pharmacien
        if self.request.user.role == 'pharmacien':
            try:
                pharmacie = Pharmacie.objects.get(user=self.request.user)
                queryset = queryset.filter(vente__pharmacie=pharmacie)
            except Pharmacie.DoesNotExist:
                queryset = queryset.none()
        
        return queryset


class EmployePharmacieViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des employés de pharmacie"""
    queryset = EmployePharmacie.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['pharmacie', 'actif', 'peut_vendre', 'peut_gerer_stock']
    search_fields = ['user__nom', 'user__email', 'poste']
    ordering_fields = ['user__nom', 'date_embauche', 'created_at']
    ordering = ['user__nom']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EmployePharmacieCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return EmployePharmacieUpdateSerializer
        return EmployePharmacieSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = get_user_from_request(self.request)
        
        # Si pas de request (génération du schéma Swagger), retourner tous les objets
        if not user:
            return queryset
        
        # Super admin voit tout
        if user.role == 'super_admin':
            return queryset
        
        # Pharmacien voit seulement les employés de ses pharmacies
        if user.role == 'pharmacien':
            pharmacies = Pharmacie.objects.filter(user=user, actif=True)
            return queryset.filter(pharmacie__in=pharmacies)
        
        # Employé voit seulement son propre profil
        if user.role == 'employe_pharmacie':
            return queryset.filter(user=user)
        
        return queryset.none()
    
    def perform_create(self, serializer):
        """Créer un employé en s'assurant qu'il appartient à une pharmacie du pharmacien connecté"""
        if self.request.user.role == 'pharmacien':
            pharmacie = serializer.validated_data.get('pharmacie')
            # Vérifier que la pharmacie appartient au pharmacien connecté
            if not Pharmacie.objects.filter(id=pharmacie.id, user=self.request.user).exists():
                raise serializers.ValidationError("Vous ne pouvez créer des employés que pour vos propres pharmacies.")
        
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def activer(self, request, pk=None):
        """Activer un employé"""
        employe = self.get_object()
        
        # Vérifier les permissions
        if request.user.role == 'pharmacien':
            if not Pharmacie.objects.filter(id=employe.pharmacie.id, user=request.user).exists():
                return Response(
                    {'error': 'Vous ne pouvez gérer que les employés de vos pharmacies'},
                    status=status.HTTP_403_FORBIDDEN
                )
        elif request.user.role != 'super_admin':
            return Response(
                {'error': 'Accès refusé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        employe.actif = True
        employe.user.actif = True
        employe.save()
        employe.user.save()
        
        return Response({'status': 'Employé activé avec succès'})
    
    @action(detail=True, methods=['post'])
    def desactiver(self, request, pk=None):
        """Désactiver un employé"""
        employe = self.get_object()
        
        # Vérifier les permissions
        if request.user.role == 'pharmacien':
            if not Pharmacie.objects.filter(id=employe.pharmacie.id, user=request.user).exists():
                return Response(
                    {'error': 'Vous ne pouvez gérer que les employés de vos pharmacies'},
                    status=status.HTTP_403_FORBIDDEN
                )
        elif request.user.role != 'super_admin':
            return Response(
                {'error': 'Accès refusé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        employe.actif = False
        employe.user.actif = False
        employe.save()
        employe.user.save()
        
        return Response({'status': 'Employé désactivé avec succès'})
    
    @action(detail=True, methods=['post'])
    def changer_mot_de_passe(self, request, pk=None):
        """Changer le mot de passe d'un employé"""
        employe = self.get_object()
        nouveau_mot_de_passe = request.data.get('nouveau_mot_de_passe')
        
        if not nouveau_mot_de_passe:
            return Response(
                {'error': 'Le nouveau mot de passe est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier les permissions
        if request.user.role == 'pharmacien':
            if not Pharmacie.objects.filter(id=employe.pharmacie.id, user=request.user).exists():
                return Response(
                    {'error': 'Vous ne pouvez gérer que les employés de vos pharmacies'},
                    status=status.HTTP_403_FORBIDDEN
                )
        elif request.user.role != 'super_admin':
            return Response(
                {'error': 'Accès refusé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Valider le mot de passe
        try:
            validate_password(nouveau_mot_de_passe, employe.user)
        except ValidationError as e:
            return Response(
                {'error': list(e.messages)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Changer le mot de passe
        employe.user.set_password(nouveau_mot_de_passe)
        employe.user.save()
        
        return Response({'status': 'Mot de passe changé avec succès'})
    
    @action(detail=False, methods=['get'])
    def mes_employes(self, request):
        """Récupérer les employés du pharmacien connecté"""
        if request.user.role != 'pharmacien':
            return Response(
                {'error': 'Accès réservé aux pharmaciens'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        pharmacies = Pharmacie.objects.filter(user=request.user, actif=True)
        employes = EmployePharmacie.objects.filter(pharmacie__in=pharmacies)
        serializer = self.get_serializer(employes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def mon_profil(self, request):
        """Récupérer le profil de l'employé connecté"""
        if request.user.role != 'employe_pharmacie':
            return Response(
                {'error': 'Accès réservé aux employés'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            employe = EmployePharmacie.objects.get(user=request.user)
            serializer = self.get_serializer(employe)
            return Response(serializer.data)
        except EmployePharmacie.DoesNotExist:
            return Response(
                {'error': 'Profil employé non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """Obtenir les statistiques des employés"""
        queryset = self.get_queryset()
        
        stats = {
            'total_employes': queryset.count(),
            'employes_actifs': queryset.filter(actif=True).count(),
            'employes_inactifs': queryset.filter(actif=False).count(),
            'par_pharmacie': {},
            'par_poste': {},
            'permissions': {
                'peuvent_vendre': queryset.filter(peut_vendre=True).count(),
                'peuvent_gerer_stock': queryset.filter(peut_gerer_stock=True).count(),
                'peuvent_voir_commandes': queryset.filter(peut_voir_commandes=True).count(),
                'peuvent_traiter_commandes': queryset.filter(peut_traiter_commandes=True).count(),
            }
        }
        
        # Statistiques par pharmacie
        for pharmacie in Pharmacie.objects.filter(employes__in=queryset).distinct():
            employes_pharmacie = queryset.filter(pharmacie=pharmacie)
            stats['par_pharmacie'][pharmacie.nom] = {
                'total': employes_pharmacie.count(),
                'actifs': employes_pharmacie.filter(actif=True).count(),
            }
        
        # Statistiques par poste
        postes = queryset.values_list('poste', flat=True).distinct()
        for poste in postes:
            stats['par_poste'][poste] = queryset.filter(poste=poste).count()
        
        return Response(stats)


class RegistreViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des registres hospitaliers"""
    queryset = Registre.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['hopital', 'specialiste', 'sexe', 'actif', 'examen_labo_type']
    search_fields = ['nom', 'prenom', 'numero_cni', 'numero_cne', 'diagnostic', 'motif_symptomes']
    ordering_fields = ['date_creation', 'nom', 'prenom', 'age']
    ordering = ['-date_creation']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return RegistreCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return RegistreUpdateSerializer
        return RegistreSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = get_user_from_request(self.request)
        
        # Si pas de request (génération du schéma Swagger), retourner tous les objets actifs
        if not user:
            return queryset.filter(actif=True)
        
        # Super admin voit tout
        if user.role == 'super_admin':
            return queryset
        
        # Admin hôpital voit les registres de son hôpital
        if user.role == 'admin_hopital':
            try:
                hopital = Hopital.objects.get(admin_hopital=user)
                return queryset.filter(hopital=hopital)
            except Hopital.DoesNotExist:
                return queryset.none()
        
        # Spécialiste voit seulement ses registres
        if user.role == 'specialiste':
            try:
                specialiste = Specialiste.objects.get(user=user)
                return queryset.filter(specialiste=specialiste)
            except Specialiste.DoesNotExist:
                return queryset.none()
        
        # Autres rôles n'ont pas accès
        return queryset.none()
    
    def perform_create(self, serializer):
        """Créer un registre et gérer la liaison/création du patient"""
        user = self.request.user
        
        # Déterminer l'hôpital et le spécialiste
        if user.role == 'specialiste':
            try:
                specialiste = Specialiste.objects.get(user=user)
                hopital = specialiste.hopital
            except Specialiste.DoesNotExist:
                raise ValidationError("Profil spécialiste non trouvé")
        elif user.role == 'admin_hopital':
            try:
                hopital = Hopital.objects.get(admin_hopital=user)
                # Pour un admin, il faut spécifier le spécialiste
                specialiste_id = self.request.data.get('specialiste')
                if not specialiste_id:
                    raise ValidationError("Le spécialiste est requis")
                specialiste = Specialiste.objects.get(id=specialiste_id, hopital=hopital)
            except (Hopital.DoesNotExist, Specialiste.DoesNotExist):
                raise ValidationError("Hôpital ou spécialiste non trouvé")
        else:
            raise ValidationError("Accès refusé")
        
        # Sauvegarder le registre
        registre = serializer.save(hopital=hopital, specialiste=specialiste)
        
        # Créer ou lier le patient
        patient, cree = registre.creer_ou_lier_patient()
        
        # Créer une notification pour informer de la création
        if cree:
            message = f"Nouveau patient créé automatiquement: {patient.nom} {patient.prenom}"
        else:
            message = f"Patient existant lié au registre: {patient.nom} {patient.prenom}"
        
        Notification.objects.create(
            user=user,
            type_notification='autre',
            titre='Registre créé',
            message=message,
            data={'registre_id': registre.id, 'patient_cree': cree}
        )
    
    def perform_update(self, serializer):
        """Mettre à jour un registre"""
        registre = serializer.save()
        
        # Si les informations d'identité ont changé, essayer de re-lier le patient
        if any(field in serializer.validated_data for field in ['numero_cni', 'numero_cne']):
            patient, cree = registre.creer_ou_lier_patient()
    
    def perform_destroy(self, instance):
        """Supprimer un registre (soft delete)"""
        # Ne pas supprimer physiquement, juste désactiver
        instance.actif = False
        instance.save()
    
    @action(detail=True, methods=['post'])
    def lier_patient(self, request, pk=None):
        """Lier manuellement un registre à un patient existant"""
        registre = self.get_object()
        patient_id = request.data.get('patient_id')
        
        if not patient_id:
            return Response(
                {'error': 'patient_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            patient = Patient.objects.get(id=patient_id)
            registre.patient = patient
            registre.save()
            
            return Response({
                'status': 'Patient lié avec succès',
                'patient': {
                    'id': patient.id,
                    'nom': patient.nom,
                    'prenom': patient.prenom
                }
            })
        except Patient.DoesNotExist:
            return Response(
                {'error': 'Patient non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def creer_patient(self, request, pk=None):
        """Créer un nouveau patient à partir du registre"""
        registre = self.get_object()
        
        if registre.patient:
            return Response(
                {'error': 'Ce registre est déjà lié à un patient'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        patient, cree = registre.creer_ou_lier_patient()
        
        if cree:
            return Response({
                'status': 'Patient créé avec succès',
                'patient': {
                    'id': patient.id,
                    'nom': patient.nom,
                    'prenom': patient.prenom
                }
            })
        else:
            return Response({
                'status': 'Patient existant lié',
                'patient': {
                    'id': patient.id,
                    'nom': patient.nom,
                    'prenom': patient.prenom
                }
            })
    
    @action(detail=False, methods=['get'])
    def mes_registres(self, request):
        """Récupérer les registres du spécialiste connecté"""
        if request.user.role != 'specialiste':
            return Response(
                {'error': 'Accès réservé aux spécialistes'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            specialiste = Specialiste.objects.get(user=request.user)
            registres = self.get_queryset().filter(specialiste=specialiste)
            
            # Pagination
            page = self.paginate_queryset(registres)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(registres, many=True)
            return Response(serializer.data)
        except Specialiste.DoesNotExist:
            return Response(
                {'error': 'Profil spécialiste non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """Obtenir les statistiques des registres"""
        queryset = self.get_queryset()
        
        # Statistiques de base
        stats = {
            'total_registres': queryset.count(),
            'registres_actifs': queryset.filter(actif=True).count(),
            'registres_inactifs': queryset.filter(actif=False).count(),
            'par_sexe': {
                'masculin': queryset.filter(sexe='M').count(),
                'feminin': queryset.filter(sexe='F').count(),
            },
            'par_examen_labo': {
                'positif': queryset.filter(examen_labo_type='positif').count(),
                'negatif': queryset.filter(examen_labo_type='negatif').count(),
            },
            'par_consultation': {
                'nc_oui': queryset.filter(consultation_nc='oui').count(),
                'ac_oui': queryset.filter(consultation_ac='oui').count(),
                'refere_asc_oui': queryset.filter(consultation_refere_asc='oui').count(),
            },
            'moyennes': {
                'age': queryset.aggregate(Avg('age'))['age__avg'] or 0,
                'poids': queryset.aggregate(Avg('poids_kg'))['poids_kg__avg'] or 0,
                'taille': queryset.aggregate(Avg('taille_cm'))['taille_cm__avg'] or 0,
                'imc': queryset.aggregate(Avg('imc'))['imc__avg'] or 0,
            }
        }
        
        # Statistiques par spécialiste (si admin hôpital)
        if request.user.role == 'admin_hopital':
            stats['par_specialiste'] = {}
            for specialiste in Specialiste.objects.filter(hopital__admin_hopital=request.user):
                count = queryset.filter(specialiste=specialiste).count()
                stats['par_specialiste'][f"{specialiste.user.nom}"] = count
        
        # Statistiques par tranche d'âge
        stats['par_age'] = {
            '0-18': queryset.filter(age__lte=18).count(),
            '19-35': queryset.filter(age__gte=19, age__lte=35).count(),
            '36-50': queryset.filter(age__gte=36, age__lte=50).count(),
            '51-65': queryset.filter(age__gte=51, age__lte=65).count(),
            '65+': queryset.filter(age__gt=65).count(),
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def rechercher_patient(self, request):
        """Rechercher un patient existant par CNI/CNE"""
        numero_cni = request.query_params.get('numero_cni')
        numero_cne = request.query_params.get('numero_cne')
        
        if not numero_cni and not numero_cne:
            return Response(
                {'error': 'numero_cni ou numero_cne est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        patients = Patient.objects.none()
        
        if numero_cni:
            patients = Patient.objects.filter(numero_cni=numero_cni)
        elif numero_cne:
            patients = Patient.objects.filter(numero_cne=numero_cne)
        
        if patients.exists():
            patient = patients.first()
            return Response({
                'trouve': True,
                'patient': {
                    'id': patient.id,
                    'nom': patient.nom,
                    'prenom': patient.prenom,
                    'sexe': patient.sexe,
                    'age': patient.age,
                    'telephone': patient.telephone,
                    'email': patient.email,
                    'numero_cni': patient.numero_cni,
                    'numero_cne': patient.numero_cne,
                }
            })
        else:
            return Response({
                'trouve': False,
                'message': 'Aucun patient trouvé avec ce numéro'
            })

class OrdonnanceViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des ordonnances"""
    queryset = Ordonnance.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['statut', 'specialiste', 'hopital', 'registre']
    search_fields = ['numero_ordonnance', 'patient_nom', 'patient_prenom', 'diagnostic']
    ordering_fields = ['date_prescription', 'date_expiration', 'patient_nom']
    ordering = ['-date_prescription']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrdonnanceCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OrdonnanceUpdateSerializer
        elif self.action == 'list':
            return OrdonnanceListSerializer
        return OrdonnanceSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = get_user_from_request(self.request)
        
        # Si pas de request (génération du schéma Swagger), retourner tous les objets
        if not user:
            return queryset
        
        # Super admin voit tout
        if user.role == 'super_admin':
            return queryset
        
        # Admin hôpital voit les ordonnances de son hôpital
        if user.role == 'admin_hopital':
            try:
                hopital = Hopital.objects.get(admin_hopital=user)
                return queryset.filter(hopital=hopital)
            except Hopital.DoesNotExist:
                return queryset.none()
        
        # Spécialiste voit seulement ses ordonnances
        if user.role == 'specialiste':
            try:
                specialiste = Specialiste.objects.get(user=user)
                return queryset.filter(specialiste=specialiste)
            except Specialiste.DoesNotExist:
                return queryset.none()
        
        # Pharmaciens voient les ordonnances validées
        if user.role in ['pharmacien', 'employe_pharmacie']:
            return queryset.filter(statut__in=['validee', 'delivree'])
        
        # Autres rôles n'ont pas accès
        return queryset.none()
    
    def perform_create(self, serializer):
        """Créer une ordonnance"""
        user = self.request.user
        
        # Déterminer le spécialiste et l'hôpital
        if user.role == 'specialiste':
            try:
                specialiste = Specialiste.objects.get(user=user)
                hopital = specialiste.hopital
            except Specialiste.DoesNotExist:
                raise ValidationError("Profil spécialiste non trouvé")
        elif user.role == 'admin_hopital':
            try:
                hopital = Hopital.objects.get(admin_hopital=user)
                # Pour un admin, il faut spécifier le spécialiste
                registre = serializer.validated_data.get('registre')
                if registre and registre.specialiste:
                    specialiste = registre.specialiste
                else:
                    raise ValidationError("Impossible de déterminer le spécialiste")
            except Hopital.DoesNotExist:
                raise ValidationError("Hôpital non trouvé")
        else:
            raise ValidationError("Accès refusé")
        
        # Sauvegarder l'ordonnance
        ordonnance = serializer.save(specialiste=specialiste, hopital=hopital)
        
        # Créer une notification
        Notification.objects.create(
            user=user,
            type_notification='autre',
            titre='Ordonnance créée',
            message=f"Ordonnance {ordonnance.numero_ordonnance} créée pour {ordonnance.patient_nom} {ordonnance.patient_prenom}",
            data={'ordonnance_id': ordonnance.id}
        )
    
    @action(detail=True, methods=['post'])
    def valider(self, request, pk=None):
        """Valider une ordonnance"""
        ordonnance = self.get_object()
        
        # Vérifier les permissions
        if request.user.role not in ['specialiste', 'admin_hopital']:
            return Response(
                {'error': 'Seuls les spécialistes et admins peuvent valider une ordonnance'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Vérifier que l'ordonnance peut être validée
        if ordonnance.statut != 'brouillon':
            return Response(
                {'error': 'Seules les ordonnances en brouillon peuvent être validées'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Valider l'ordonnance
        ordonnance.statut = 'validee'
        ordonnance.date_validation = timezone.now()
        ordonnance.save()
        
        return Response({
            'status': 'Ordonnance validée avec succès',
            'numero_ordonnance': ordonnance.numero_ordonnance
        })
    
    @action(detail=True, methods=['post'])
    def annuler(self, request, pk=None):
        """Annuler une ordonnance"""
        ordonnance = self.get_object()
        
        # Vérifier les permissions
        if request.user.role not in ['specialiste', 'admin_hopital']:
            return Response(
                {'error': 'Seuls les spécialistes et admins peuvent annuler une ordonnance'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Vérifier que l'ordonnance peut être annulée
        if ordonnance.statut == 'delivree':
            return Response(
                {'error': 'Une ordonnance délivrée ne peut pas être annulée'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Annuler l'ordonnance
        ordonnance.statut = 'annulee'
        ordonnance.save()
        
        return Response({
            'status': 'Ordonnance annulée avec succès',
            'numero_ordonnance': ordonnance.numero_ordonnance
        })
    
    @action(detail=True, methods=['post'])
    def delivrer(self, request, pk=None):
        """Marquer une ordonnance comme délivrée (pour les pharmaciens)"""
        ordonnance = self.get_object()
        
        # Vérifier les permissions
        if request.user.role not in ['pharmacien', 'employe_pharmacie']:
            return Response(
                {'error': 'Seuls les pharmaciens peuvent marquer une ordonnance comme délivrée'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Vérifier que l'ordonnance peut être délivrée
        if not ordonnance.peut_etre_delivree:
            return Response(
                {'error': 'Cette ordonnance ne peut pas être délivrée (non validée ou expirée)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Déterminer la pharmacie
        pharmacie = None
        if request.user.role == 'pharmacien':
            try:
                pharmacie = Pharmacie.objects.get(user=request.user)
            except Pharmacie.DoesNotExist:
                pass
        elif request.user.role == 'employe_pharmacie':
            try:
                employe = EmployePharmacie.objects.get(user=request.user)
                pharmacie = employe.pharmacie
            except EmployePharmacie.DoesNotExist:
                pass
        
        # Marquer comme délivrée
        ordonnance.statut = 'delivree'
        ordonnance.date_delivrance = timezone.now()
        if pharmacie:
            ordonnance.pharmacie_delivrance = pharmacie
        ordonnance.save()
        
        return Response({
            'status': 'Ordonnance marquée comme délivrée',
            'numero_ordonnance': ordonnance.numero_ordonnance,
            'pharmacie': pharmacie.nom if pharmacie else None
        })
    
    @action(detail=False, methods=['get'])
    def mes_ordonnances(self, request):
        """Récupérer les ordonnances du spécialiste connecté"""
        if request.user.role != 'specialiste':
            return Response(
                {'error': 'Accès réservé aux spécialistes'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            specialiste = Specialiste.objects.get(user=request.user)
            ordonnances = self.get_queryset().filter(specialiste=specialiste)
            
            # Pagination
            page = self.paginate_queryset(ordonnances)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(ordonnances, many=True)
            return Response(serializer.data)
        except Specialiste.DoesNotExist:
            return Response(
                {'error': 'Profil spécialiste non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def par_registre(self, request):
        """Récupérer les ordonnances d'un registre spécifique"""
        registre_id = request.query_params.get('registre_id')
        if not registre_id:
            return Response(
                {'error': 'registre_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ordonnances = self.get_queryset().filter(registre_id=registre_id)
        serializer = self.get_serializer(ordonnances, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """Obtenir les statistiques des ordonnances"""
        queryset = self.get_queryset()
        
        stats = {
            'total_ordonnances': queryset.count(),
            'par_statut': {
                'brouillon': queryset.filter(statut='brouillon').count(),
                'validee': queryset.filter(statut='validee').count(),
                'delivree': queryset.filter(statut='delivree').count(),
                'annulee': queryset.filter(statut='annulee').count(),
            },
            'expirees': queryset.filter(
                date_expiration__lt=timezone.now().date(),
                statut__in=['brouillon', 'validee']
            ).count(),
            'ce_mois': queryset.filter(
                date_prescription__month=timezone.now().month,
                date_prescription__year=timezone.now().year
            ).count(),
        }
        
        # Statistiques par spécialiste (si admin hôpital)
        if request.user.role == 'admin_hopital':
            stats['par_specialiste'] = {}
            for specialiste in Specialiste.objects.filter(hopital__admin_hopital=request.user):
                count = queryset.filter(specialiste=specialiste).count()
                stats['par_specialiste'][f"{specialiste.user.nom}"] = count
        
        return Response(stats)
    
    @action(detail=True, methods=['get'])
    def generer_pdf(self, request, pk=None):
        """Générer et télécharger le PDF de l'ordonnance"""
        ordonnance = self.get_object()
        
        # Vérifier les permissions
        user = request.user
        if user.role == 'specialiste':
            try:
                specialiste = Specialiste.objects.get(user=user)
                if ordonnance.specialiste != specialiste:
                    return Response(
                        {'error': 'Vous ne pouvez accéder qu\'à vos propres ordonnances'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except Specialiste.DoesNotExist:
                return Response(
                    {'error': 'Profil spécialiste non trouvé'},
                    status=status.HTTP_404_NOT_FOUND
                )
        elif user.role == 'admin_hopital':
            try:
                hopital = Hopital.objects.get(admin_hopital=user)
                if ordonnance.hopital != hopital:
                    return Response(
                        {'error': 'Vous ne pouvez accéder qu\'aux ordonnances de votre hôpital'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except Hopital.DoesNotExist:
                return Response(
                    {'error': 'Hôpital non trouvé'},
                    status=status.HTTP_404_NOT_FOUND
                )
        elif user.role not in ['super_admin', 'pharmacien', 'employe_pharmacie']:
            return Response(
                {'error': 'Accès refusé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            from .pdf_utils import generer_pdf_ordonnance, generer_nom_fichier_pdf
            from django.http import HttpResponse
            
            # Générer le PDF
            pdf_buffer = generer_pdf_ordonnance(ordonnance)
            filename = generer_nom_fichier_pdf(ordonnance)
            
            # Créer la réponse HTTP
            response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['Content-Length'] = len(pdf_buffer.getvalue())
            
            return response
            
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de la génération du PDF: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def generer_qr_code(self, request, pk=None):
        """Générer le QR code pour l'ordonnance"""
        ordonnance = self.get_object()
        
        # Vérifier les permissions (même logique que pour le PDF)
        user = request.user
        if user.role == 'specialiste':
            try:
                specialiste = Specialiste.objects.get(user=user)
                if ordonnance.specialiste != specialiste:
                    return Response(
                        {'error': 'Vous ne pouvez accéder qu\'à vos propres ordonnances'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except Specialiste.DoesNotExist:
                return Response(
                    {'error': 'Profil spécialiste non trouvé'},
                    status=status.HTTP_404_NOT_FOUND
                )
        elif user.role == 'admin_hopital':
            try:
                hopital = Hopital.objects.get(admin_hopital=user)
                if ordonnance.hopital != hopital:
                    return Response(
                        {'error': 'Vous ne pouvez accéder qu\'aux ordonnances de votre hôpital'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except Hopital.DoesNotExist:
                return Response(
                    {'error': 'Hôpital non trouvé'},
                    status=status.HTTP_404_NOT_FOUND
                )
        elif user.role not in ['super_admin']:
            return Response(
                {'error': 'Accès refusé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            # Générer le QR code
            qr_url = ordonnance.generer_qr_code(request)
            
            if qr_url:
                return Response({
                    'qr_code_url': qr_url,
                    'pdf_url': ordonnance.qr_code_url,
                    'message': 'QR code généré avec succès'
                })
            else:
                return Response(
                    {'error': 'Erreur lors de la génération du QR code'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de la génération du QR code: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LigneOrdonnanceViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des lignes d'ordonnance"""
    queryset = LigneOrdonnance.objects.all()
    serializer_class = LigneOrdonnanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['ordonnance', 'produit']
    ordering_fields = ['ordre', 'created_at']
    ordering = ['ordre']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return LigneOrdonnanceCreateSerializer
        return LigneOrdonnanceSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = get_user_from_request(self.request)
        
        # Si pas de request (génération du schéma Swagger), retourner tous les objets
        if not user:
            return queryset
        
        # Filtrer selon les permissions des ordonnances
        if user.role == 'super_admin':
            return queryset
        elif user.role == 'admin_hopital':
            try:
                hopital = Hopital.objects.get(admin_hopital=user)
                return queryset.filter(ordonnance__hopital=hopital)
            except Hopital.DoesNotExist:
                return queryset.none()
        elif user.role == 'specialiste':
            try:
                specialiste = Specialiste.objects.get(user=user)
                return queryset.filter(ordonnance__specialiste=specialiste)
            except Specialiste.DoesNotExist:
                return queryset.none()
        elif user.role in ['pharmacien', 'employe_pharmacie']:
            return queryset.filter(ordonnance__statut__in=['validee', 'delivree'])
        
        return queryset.none()
    
    def perform_create(self, serializer):
        """Créer une ligne d'ordonnance"""
        # Vérifier que l'utilisateur peut modifier cette ordonnance
        ordonnance = serializer.validated_data['ordonnance']
        user = self.request.user
        
        if user.role == 'specialiste':
            try:
                specialiste = Specialiste.objects.get(user=user)
                if ordonnance.specialiste != specialiste:
                    raise ValidationError("Vous ne pouvez modifier que vos propres ordonnances")
            except Specialiste.DoesNotExist:
                raise ValidationError("Profil spécialiste non trouvé")
        elif user.role == 'admin_hopital':
            try:
                hopital = Hopital.objects.get(admin_hopital=user)
                if ordonnance.hopital != hopital:
                    raise ValidationError("Vous ne pouvez modifier que les ordonnances de votre hôpital")
            except Hopital.DoesNotExist:
                raise ValidationError("Hôpital non trouvé")
        else:
            raise ValidationError("Accès refusé")
        
        # Vérifier que l'ordonnance peut être modifiée
        if ordonnance.statut in ['delivree', 'annulee']:
            raise ValidationError("Cette ordonnance ne peut plus être modifiée")
        
        serializer.save()
    
    def perform_update(self, serializer):
        """Mettre à jour une ligne d'ordonnance"""
        # Même vérifications que pour la création
        self.perform_create(serializer)
    
    def perform_destroy(self, instance):
        """Supprimer une ligne d'ordonnance"""
        # Vérifier les permissions
        ordonnance = instance.ordonnance
        user = self.request.user
        
        if user.role == 'specialiste':
            try:
                specialiste = Specialiste.objects.get(user=user)
                if ordonnance.specialiste != specialiste:
                    raise ValidationError("Vous ne pouvez modifier que vos propres ordonnances")
            except Specialiste.DoesNotExist:
                raise ValidationError("Profil spécialiste non trouvé")
        elif user.role == 'admin_hopital':
            try:
                hopital = Hopital.objects.get(admin_hopital=user)
                if ordonnance.hopital != hopital:
                    raise ValidationError("Vous ne pouvez modifier que les ordonnances de votre hôpital")
            except Hopital.DoesNotExist:
                raise ValidationError("Hôpital non trouvé")
        else:
            raise ValidationError("Accès refusé")
        
        # Vérifier que l'ordonnance peut être modifiée
        if ordonnance.statut in ['delivree', 'annulee']:
            raise ValidationError("Cette ordonnance ne peut plus être modifiée")
        
        instance.delete()


class DossierMedicalViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des dossiers médicaux"""
    queryset = DossierMedical.objects.all()
    serializer_class = DossierMedicalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['registre', 'specialiste', 'hopital']
    search_fields = ['numero_dossier', 'patient_nom', 'patient_prenom', 'motif_consultation', 'diagnostic']
    ordering_fields = ['date_consultation', 'created_at']
    ordering = ['-date_consultation']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DossierMedicalCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return DossierMedicalUpdateSerializer
        elif self.action == 'list':
            return DossierMedicalListSerializer
        elif self.action == 'retrieve':
            return DossierMedicalDetailSerializer
        return DossierMedicalSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = get_user_from_request(self.request)
        
        # Si pas de request (génération du schéma Swagger), retourner tous les objets
        if not user:
            return queryset
        
        # Filtrer selon le rôle de l'utilisateur
        if user.role == 'super_admin':
            return queryset
        elif user.role == 'admin_hopital':
            try:
                hopital = Hopital.objects.get(admin_hopital=user)
                return queryset.filter(hopital=hopital)
            except Hopital.DoesNotExist:
                return queryset.none()
        elif user.role == 'specialiste':
            try:
                specialiste = Specialiste.objects.get(user=user)
                return queryset.filter(specialiste=specialiste)
            except Specialiste.DoesNotExist:
                return queryset.none()
        elif user.role == 'patient':
            # Les patients peuvent voir leurs propres dossiers
            try:
                patient = Patient.objects.get(email=user.email)
                return queryset.filter(
                    models.Q(registre__patient=patient) |
                    models.Q(patient_nom=patient.nom, patient_prenom=patient.prenom)
                )
            except Patient.DoesNotExist:
                return queryset.none()
        
        return queryset.none()
    
    def perform_create(self, serializer):
        """Créer un dossier médical"""
        user = self.request.user
        
        # Seuls les spécialistes peuvent créer des dossiers médicaux
        if user.role != 'specialiste':
            raise ValidationError("Seuls les spécialistes peuvent créer des dossiers médicaux")
        
        try:
            specialiste = Specialiste.objects.get(user=user)
            serializer.save(specialiste=specialiste, hopital=specialiste.hopital)
        except Specialiste.DoesNotExist:
            raise ValidationError("Profil spécialiste non trouvé")
    
    def perform_update(self, serializer):
        """Mettre à jour un dossier médical"""
        user = self.request.user
        dossier = self.get_object()
        
        # Vérifier les permissions
        if user.role == 'specialiste':
            try:
                specialiste = Specialiste.objects.get(user=user)
                if dossier.specialiste != specialiste:
                    raise ValidationError("Vous ne pouvez modifier que vos propres dossiers")
            except Specialiste.DoesNotExist:
                raise ValidationError("Profil spécialiste non trouvé")
        elif user.role == 'admin_hopital':
            try:
                hopital = Hopital.objects.get(admin_hopital=user)
                if dossier.hopital != hopital:
                    raise ValidationError("Vous ne pouvez modifier que les dossiers de votre hôpital")
            except Hopital.DoesNotExist:
                raise ValidationError("Hôpital non trouvé")
        else:
            raise ValidationError("Accès refusé")
        
        serializer.save()
    
    def perform_destroy(self, instance):
        """Supprimer un dossier médical"""
        user = self.request.user
        
        # Vérifier les permissions
        if user.role == 'specialiste':
            try:
                specialiste = Specialiste.objects.get(user=user)
                if instance.specialiste != specialiste:
                    raise ValidationError("Vous ne pouvez supprimer que vos propres dossiers")
            except Specialiste.DoesNotExist:
                raise ValidationError("Profil spécialiste non trouvé")
        elif user.role == 'admin_hopital':
            try:
                hopital = Hopital.objects.get(admin_hopital=user)
                if instance.hopital != hopital:
                    raise ValidationError("Vous ne pouvez supprimer que les dossiers de votre hôpital")
            except Hopital.DoesNotExist:
                raise ValidationError("Hôpital non trouvé")
        elif user.role != 'super_admin':
            raise ValidationError("Accès refusé")
        
        instance.delete()
    
    @action(detail=False, methods=['get'])
    def mes_dossiers(self, request):
        """Récupérer les dossiers de l'utilisateur connecté"""
        user = request.user
        
        if user.role == 'specialiste':
            try:
                specialiste = Specialiste.objects.get(user=user)
                dossiers = self.queryset.filter(specialiste=specialiste)
                serializer = DossierMedicalListSerializer(dossiers, many=True)
                return Response(serializer.data)
            except Specialiste.DoesNotExist:
                return Response({"error": "Profil spécialiste non trouvé"}, status=404)
        
        return Response({"error": "Accès refusé"}, status=403)
    
    @action(detail=True, methods=['post'])
    def upload_fichier(self, request, pk=None):
        """Ajouter un fichier joint au dossier médical"""
        dossier = self.get_object()
        
        # Vérifier les permissions
        user = request.user
        if user.role == 'specialiste':
            try:
                specialiste = Specialiste.objects.get(user=user)
                if dossier.specialiste != specialiste:
                    return Response({"error": "Accès refusé"}, status=403)
            except Specialiste.DoesNotExist:
                return Response({"error": "Profil spécialiste non trouvé"}, status=404)
        elif user.role == 'admin_hopital':
            try:
                hopital = Hopital.objects.get(admin_hopital=user)
                if dossier.hopital != hopital:
                    return Response({"error": "Accès refusé"}, status=403)
            except Hopital.DoesNotExist:
                return Response({"error": "Hôpital non trouvé"}, status=404)
        elif user.role != 'super_admin':
            return Response({"error": "Accès refusé"}, status=403)
        
        # Créer le fichier
        data = request.data.copy()
        data['dossier_medical'] = dossier.id
        
        serializer = FichierDossierMedicalCreateSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def export_pdf(self, request, pk=None):
        """Exporter le dossier médical en PDF"""
        dossier = self.get_object()
        
        # Vérifier les permissions
        user = request.user
        if user.role == 'specialiste':
            try:
                specialiste = Specialiste.objects.get(user=user)
                if dossier.specialiste != specialiste:
                    return Response({"error": "Accès refusé"}, status=403)
            except Specialiste.DoesNotExist:
                return Response({"error": "Profil spécialiste non trouvé"}, status=404)
        elif user.role == 'admin_hopital':
            try:
                hopital = Hopital.objects.get(admin_hopital=user)
                if dossier.hopital != hopital:
                    return Response({"error": "Accès refusé"}, status=403)
            except Hopital.DoesNotExist:
                return Response({"error": "Hôpital non trouvé"}, status=404)
        elif user.role != 'super_admin':
            return Response({"error": "Accès refusé"}, status=403)
        
        # TODO: Implémenter la génération PDF
        return Response({"message": "Fonctionnalité PDF à implémenter"}, status=501)



class FichierDossierMedicalViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des fichiers joints aux dossiers médicaux"""
    queryset = FichierDossierMedical.objects.all()
    serializer_class = FichierDossierMedicalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['dossier_medical', 'type_fichier']
    ordering_fields = ['created_at', 'nom_fichier']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return FichierDossierMedicalCreateSerializer
        return FichierDossierMedicalSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = get_user_from_request(self.request)
        
        # Si pas de request (génération du schéma Swagger), retourner tous les objets
        if not user:
            return queryset
        
        # Filtrer selon le rôle de l'utilisateur
        if user.role == 'super_admin':
            return queryset
        elif user.role == 'admin_hopital':
            try:
                hopital = Hopital.objects.get(admin_hopital=user)
                return queryset.filter(dossier_medical__hopital=hopital)
            except Hopital.DoesNotExist:
                return queryset.none()
        elif user.role == 'specialiste':
            try:
                specialiste = Specialiste.objects.get(user=user)
                return queryset.filter(dossier_medical__specialiste=specialiste)
            except Specialiste.DoesNotExist:
                return queryset.none()
        elif user.role == 'patient':
            # Les patients peuvent voir les fichiers de leurs propres dossiers
            try:
                patient = Patient.objects.get(email=user.email)
                return queryset.filter(
                    models.Q(dossier_medical__registre__patient=patient) |
                    models.Q(dossier_medical__patient_nom=patient.nom, dossier_medical__patient_prenom=patient.prenom)
                )
            except Patient.DoesNotExist:
                return queryset.none()
        
        return queryset.none()
    
    def perform_create(self, serializer):
        """Créer un fichier joint"""
        user = self.request.user
        dossier_medical_id = self.request.data.get('dossier_medical')
        
        # Vérifier que le dossier médical existe
        try:
            dossier = DossierMedical.objects.get(id=dossier_medical_id)
        except DossierMedical.DoesNotExist:
            raise ValidationError("Dossier médical non trouvé")
        
        # Vérifier les permissions
        if user.role == 'specialiste':
            try:
                specialiste = Specialiste.objects.get(user=user)
                if dossier.specialiste != specialiste:
                    raise ValidationError("Vous ne pouvez ajouter des fichiers qu'à vos propres dossiers")
            except Specialiste.DoesNotExist:
                raise ValidationError("Profil spécialiste non trouvé")
        elif user.role == 'admin_hopital':
            try:
                hopital = Hopital.objects.get(admin_hopital=user)
                if dossier.hopital != hopital:
                    raise ValidationError("Vous ne pouvez ajouter des fichiers qu'aux dossiers de votre hôpital")
            except Hopital.DoesNotExist:
                raise ValidationError("Hôpital non trouvé")
        elif user.role != 'super_admin':
            raise ValidationError("Accès refusé")
        
        serializer.save()
    
    def perform_destroy(self, instance):
        """Supprimer un fichier joint"""
        user = self.request.user
        dossier = instance.dossier_medical
        
        # Vérifier les permissions
        if user.role == 'specialiste':
            try:
                specialiste = Specialiste.objects.get(user=user)
                if dossier.specialiste != specialiste:
                    raise ValidationError("Vous ne pouvez supprimer que les fichiers de vos propres dossiers")
            except Specialiste.DoesNotExist:
                raise ValidationError("Profil spécialiste non trouvé")
        elif user.role == 'admin_hopital':
            try:
                hopital = Hopital.objects.get(admin_hopital=user)
                if dossier.hopital != hopital:
                    raise ValidationError("Vous ne pouvez supprimer que les fichiers des dossiers de votre hôpital")
            except Hopital.DoesNotExist:
                raise ValidationError("Hôpital non trouvé")
        elif user.role != 'super_admin':
            raise ValidationError("Accès refusé")
        
        instance.delete()
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Télécharger un fichier"""
        fichier = self.get_object()
        
        # Vérifier les permissions (déjà fait par get_queryset)
        from django.http import FileResponse
        
        try:
            response = FileResponse(fichier.fichier.open('rb'))
            response['Content-Type'] = fichier.type_mime or 'application/octet-stream'
            response['Content-Disposition'] = f'attachment; filename="{fichier.nom_fichier}"'
            return response
        except Exception as e:
            return Response(
                {'error': f'Erreur lors du téléchargement: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ============================================================================
# ViewSets pour les Factures Fournisseurs
# ============================================================================

class FournisseurViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des fournisseurs"""
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['actif', 'ville', 'pays']
    search_fields = ['nom', 'email', 'telephone']
    ordering_fields = ['nom', 'created_at']
    ordering = ['nom']
    
    def get_queryset(self):
        """Filtrer les fournisseurs selon le rôle"""
        # Pour la génération du schéma Swagger
        if getattr(self, 'swagger_fake_view', False):
            return Fournisseur.objects.none()
            
        queryset = super().get_queryset()
        user = self.request.user
        
        # Si l'utilisateur n'est pas authentifié
        if not user.is_authenticated:
            return Fournisseur.objects.none()
        
        # Les pharmaciens ne voient que les fournisseurs actifs
        if user.role == 'pharmacien':
            queryset = queryset.filter(actif=True)
        
        return queryset
    
    @action(detail=True, methods=['post'], url_path='activer')
    def activer(self, request, pk=None):
        """Activer un fournisseur"""
        fournisseur = self.get_object()
        fournisseur.actif = True
        fournisseur.save()
        
        return Response({
            'success': True,
            'message': f'Fournisseur {fournisseur.nom} activé avec succès'
        })
    
    @action(detail=True, methods=['post'], url_path='desactiver')
    def desactiver(self, request, pk=None):
        """Désactiver un fournisseur"""
        fournisseur = self.get_object()
        fournisseur.actif = False
        fournisseur.save()
        
        return Response({
            'success': True,
            'message': f'Fournisseur {fournisseur.nom} désactivé avec succès'
        })
    
    @action(detail=True, methods=['post'], url_path='creer-compte')
    def creer_compte(self, request, pk=None):
        """Créer un compte utilisateur pour le fournisseur"""
        from django.contrib.auth.hashers import make_password
        import secrets
        
        fournisseur = self.get_object()
        
        # Vérifier si le fournisseur a un email
        if not fournisseur.email:
            return Response({
                'success': False,
                'error': 'Le fournisseur doit avoir un email pour créer un compte'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Vérifier si un compte existe déjà
        if User.objects.filter(email=fournisseur.email).exists():
            return Response({
                'success': False,
                'error': 'Un compte existe déjà avec cet email'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Générer un mot de passe temporaire
        temp_password = secrets.token_urlsafe(12)
        
        # Créer l'utilisateur
        user = User.objects.create(
            email=fournisseur.email,
            nom=fournisseur.nom,
            role='fournisseur',  # Nouveau rôle à ajouter
            actif=True,
            password=make_password(temp_password)
        )
        
        return Response({
            'success': True,
            'message': f'Compte créé pour {fournisseur.nom}',
            'email': user.email,
            'temporary_password': temp_password,
            'user_id': user.id
        })


class FactureFournisseurViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des factures fournisseurs"""
    queryset = FactureFournisseur.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['pharmacie', 'fournisseur', 'statut', 'mode_paiement']
    search_fields = ['numero_facture', 'fournisseur__nom']
    ordering_fields = ['date_facture', 'montant_total', 'created_at']
    ordering = ['-date_facture', '-created_at']
    
    def get_serializer_class(self):
        """Retourner le serializer approprié selon l'action"""
        if self.action == 'create':
            return FactureFournisseurCreateSerializer
        return FactureFournisseurSerializer
    
    def get_queryset(self):
        """Filtrer les factures selon le rôle"""
        # Pour la génération du schéma Swagger
        if getattr(self, 'swagger_fake_view', False):
            return FactureFournisseur.objects.none()
            
        queryset = super().get_queryset()
        user = self.request.user
        
        # Si l'utilisateur n'est pas authentifié
        if not user.is_authenticated:
            return FactureFournisseur.objects.none()
        
        # Les pharmaciens ne voient que leurs factures
        if user.role == 'pharmacien':
            try:
                pharmacie = Pharmacie.objects.get(user=user)
                queryset = queryset.filter(pharmacie=pharmacie)
            except Pharmacie.DoesNotExist:
                queryset = queryset.none()
        
        # Les employés ne voient que les factures de leur pharmacie
        elif user.role == 'employe_pharmacie':
            try:
                employe = EmployePharmacie.objects.get(user=user)
                # Vérifier la permission
                if employe.peut_enregistrer_facture or employe.peut_gerer_stock:
                    queryset = queryset.filter(pharmacie=employe.pharmacie)
                else:
                    queryset = queryset.none()
            except EmployePharmacie.DoesNotExist:
                queryset = queryset.none()
        
        return queryset
    
    def perform_create(self, serializer):
        """Enregistrer la facture avec l'utilisateur connecté"""
        user = self.request.user
        
        # Vérifier les permissions
        if user.role == 'employe_pharmacie':
            try:
                employe = EmployePharmacie.objects.get(user=user)
                if not employe.peut_enregistrer_facture:
                    raise PermissionDenied("Vous n'avez pas la permission d'enregistrer des factures.")
            except EmployePharmacie.DoesNotExist:
                raise PermissionDenied("Employé non trouvé.")
        
        serializer.save(enregistre_par=user)
    
    @swagger_auto_schema(
        operation_description="Valider une facture et incrémenter le stock automatiquement",
        request_body=FactureFournisseurValidationSerializer,
        responses={
            200: openapi.Response(
                description="Facture validée et stock incrémenté",
                schema=FactureFournisseurSerializer
            ),
            400: "Erreur de validation",
            403: "Permission refusée",
            404: "Facture non trouvée"
        },
        tags=['Factures Fournisseurs']
    )
    @action(detail=True, methods=['post'])
    def valider(self, request, pk=None):
        """Valider une facture et incrémenter le stock"""
        facture = self.get_object()
        
        # Vérifier les permissions
        user = request.user
        if user.role == 'employe_pharmacie':
            try:
                employe = EmployePharmacie.objects.get(user=user)
                if not (employe.peut_enregistrer_facture or employe.peut_gerer_stock):
                    return Response(
                        {'error': "Vous n'avez pas la permission de valider des factures."},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except EmployePharmacie.DoesNotExist:
                return Response(
                    {'error': "Employé non trouvé."},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        # Valider les données
        serializer = FactureFournisseurValidationSerializer(
            data=request.data,
            context={'facture': facture}
        )
        serializer.is_valid(raise_exception=True)
        
        # Vérifier que la facture n'est pas déjà validée
        if facture.statut == 'validee':
            return Response(
                {'error': 'Cette facture est déjà validée.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if facture.stock_incremente:
            return Response(
                {'error': 'Le stock a déjà été incrémenté pour cette facture.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Incrémenter le stock pour chaque ligne
        from django.db import transaction
        
        try:
            with transaction.atomic():
                from decimal import Decimal
                
                for ligne in facture.lignes.all():
                    # Récupérer ou créer le stock
                    # Note: Le modèle StockProduit utilise 'quantite' et 'seuil_alerte'
                    stock, created = StockProduit.objects.get_or_create(
                        pharmacie=facture.pharmacie,
                        produit=ligne.produit,
                        numero_lot=ligne.numero_lot or '',
                        defaults={
                            'quantite': 0,
                            'seuil_alerte': 10,
                            'prix_vente': ligne.prix_unitaire_ht * Decimal('1.3'),  # Marge de 30%
                            'date_expiration': ligne.date_peremption
                        }
                    )
                    
                    # Incrémenter la quantité
                    stock.quantite += ligne.quantite
                    
                    # Mettre à jour la date d'expiration si fournie
                    if ligne.date_peremption:
                        stock.date_expiration = ligne.date_peremption
                    
                    # Mettre à jour le prix de vente si c'est un nouveau stock
                    if created:
                        stock.prix_vente = ligne.prix_unitaire_ht * Decimal('1.3')
                    
                    stock.save()
                
                # Marquer la facture comme validée
                facture.statut = 'validee'
                facture.stock_incremente = True
                facture.save()
        
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de l\'incrémentation du stock: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        serializer = FactureFournisseurSerializer(facture)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Annuler une facture",
        responses={
            200: openapi.Response(
                description="Facture annulée",
                schema=FactureFournisseurSerializer
            ),
            400: "Erreur de validation",
            403: "Permission refusée",
            404: "Facture non trouvée"
        },
        tags=['Factures Fournisseurs']
    )
    @action(detail=True, methods=['post'])
    def annuler(self, request, pk=None):
        """Annuler une facture"""
        facture = self.get_object()
        
        # Vérifier les permissions
        user = request.user
        if user.role == 'employe_pharmacie':
            try:
                employe = EmployePharmacie.objects.get(user=user)
                if not (employe.peut_enregistrer_facture or employe.peut_gerer_stock):
                    return Response(
                        {'error': "Vous n'avez pas la permission d'annuler des factures."},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except EmployePharmacie.DoesNotExist:
                return Response(
                    {'error': "Employé non trouvé."},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        # Vérifier que la facture peut être annulée
        if facture.statut == 'annulee':
            return Response(
                {'error': 'Cette facture est déjà annulée.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if facture.stock_incremente:
            return Response(
                {'error': 'Impossible d\'annuler une facture dont le stock a été incrémenté. Veuillez d\'abord décrémenter le stock manuellement.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Annuler la facture
        facture.statut = 'annulee'
        facture.save()
        
        serializer = FactureFournisseurSerializer(facture)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Obtenir les statistiques des factures fournisseurs",
        responses={
            200: openapi.Response(
                description="Statistiques des factures",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_factures': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'montant_total': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'montant_paye': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'montant_restant': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'factures_en_attente': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'factures_validees': openapi.Schema(type=openapi.TYPE_INTEGER),
                    }
                )
            )
        },
        tags=['Factures Fournisseurs']
    )
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """Obtenir les statistiques des factures"""
        from django.db.models import Sum, Count
        
        queryset = self.get_queryset()
        
        stats = queryset.aggregate(
            total_factures=Count('id'),
            montant_total=Sum('montant_total'),
            montant_paye=Sum('montant_paye'),
            factures_en_attente=Count('id', filter=models.Q(statut='en_attente')),
            factures_validees=Count('id', filter=models.Q(statut='validee')),
        )
        
        stats['montant_total'] = float(stats['montant_total'] or 0)
        stats['montant_paye'] = float(stats['montant_paye'] or 0)
        stats['montant_restant'] = stats['montant_total'] - stats['montant_paye']
        
        return Response(stats)
