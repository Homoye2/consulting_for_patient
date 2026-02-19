# Views pour le dashboard Super Admin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Count, Q, Avg
from datetime import timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import (
    User, RendezVous, ConsultationPF, Notification,
    HistoriqueConnexion, SessionUtilisateur
)
from .permissions import CanManageUsers


class SystemHealthView(APIView):
    """API pour la santé du système"""
    permission_classes = [IsAuthenticated, CanManageUsers]
    
    @swagger_auto_schema(
        operation_description="Récupère l'état de santé du système",
        responses={200: openapi.Response(description="État de santé du système")}
    )
    def get(self, request):
        import psutil
        import time
        
        # Test de la base de données
        db_start = time.time()
        try:
            User.objects.count()
            db_time = (time.time() - db_start) * 1000
            db_status = 'healthy' if db_time < 100 else 'warning' if db_time < 500 else 'error'
        except Exception:
            db_status = 'error'
            db_time = 0
        
        # Test de l'API (toujours healthy si on arrive ici)
        api_status = 'healthy'
        api_time = 50  # Temps estimé
        
        # Stockage
        try:
            disk = psutil.disk_usage('/')
            storage_usage = f"{disk.percent}%"
            storage_status = 'healthy' if disk.percent < 80 else 'warning' if disk.percent < 90 else 'error'
        except:
            storage_usage = 'N/A'
            storage_status = 'unknown'
        
        # Mémoire
        try:
            memory = psutil.virtual_memory()
            memory_usage = f"{memory.percent}%"
            memory_status = 'healthy' if memory.percent < 80 else 'warning' if memory.percent < 90 else 'error'
        except:
            memory_usage = 'N/A'
            memory_status = 'unknown'
        
        return Response({
            'database': {
                'status': db_status,
                'responseTime': f'{int(db_time)}ms'
            },
            'api': {
                'status': api_status,
                'responseTime': f'{api_time}ms'
            },
            'storage': {
                'status': storage_status,
                'usage': storage_usage
            },
            'memory': {
                'status': memory_status,
                'usage': memory_usage
            }
        })


class RecentActivityView(APIView):
    """API pour l'activité récente du système"""
    permission_classes = [IsAuthenticated, CanManageUsers]
    
    @swagger_auto_schema(
        operation_description="Récupère l'activité récente du système",
        manual_parameters=[
            openapi.Parameter('limit', openapi.IN_QUERY, description="Nombre d'activités à retourner", type=openapi.TYPE_INTEGER, default=10)
        ],
        responses={200: openapi.Response(description="Liste des activités récentes")}
    )
    def get(self, request):
        limit = int(request.query_params.get('limit', 10))
        activities = []
        
        # Derniers rendez-vous créés
        recent_rdv = RendezVous.objects.select_related('patient').order_by('-created_at')[:limit//2]
        for rdv in recent_rdv:
            activities.append({
                'id': f'rdv-{rdv.id}',
                'type': 'appointment',
                'description': f"Nouveau rendez-vous pour {rdv.patient.nom}",
                'timestamp': rdv.created_at.isoformat(),
                'icon': 'Calendar'
            })
        
        # Dernières consultations créées
        recent_consult = ConsultationPF.objects.select_related('patient').order_by('-created_at')[:limit//2]
        for consult in recent_consult:
            activities.append({
                'id': f'consult-{consult.id}',
                'type': 'consultation',
                'description': f"Consultation effectuée pour {consult.patient.nom}",
                'timestamp': consult.created_at.isoformat(),
                'icon': 'FileText'
            })
        
        # Trier par date
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return Response(activities[:limit])


class SystemAlertsView(APIView):
    """API pour les alertes système"""
    permission_classes = [IsAuthenticated, CanManageUsers]
    
    @swagger_auto_schema(
        operation_description="Récupère les alertes système actives",
        responses={200: openapi.Response(description="Liste des alertes")}
    )
    def get(self, request):
        alerts = []
        
        # Vérifier les RDV en attente
        rdv_en_attente = RendezVous.objects.filter(statut='en_attente').count()
        if rdv_en_attente > 5:
            alerts.append({
                'id': 'rdv-pending',
                'type': 'warning',
                'message': f"{rdv_en_attente} rendez-vous en attente de confirmation",
                'action': 'Voir les rendez-vous'
            })
        
        # Vérifier les consultations du jour
        today = timezone.now().date()
        consultations_today = ConsultationPF.objects.filter(date__date=today).count()
        if consultations_today > 20:
            alerts.append({
                'id': 'consult-high',
                'type': 'info',
                'message': f"{consultations_today} consultations prévues aujourd'hui",
                'action': 'Voir le planning'
            })
        
        # Vérifier les utilisateurs inactifs récents
        inactive_users = User.objects.filter(actif=False, date_joined__gte=timezone.now() - timedelta(days=7)).count()
        if inactive_users > 0:
            alerts.append({
                'id': 'users-inactive',
                'type': 'warning',
                'message': f"{inactive_users} nouveaux utilisateurs inactifs cette semaine",
                'action': 'Gérer les utilisateurs'
            })
        
        return Response(alerts)


class SecurityStatsView(APIView):
    """API pour les statistiques de sécurité"""
    permission_classes = [IsAuthenticated, CanManageUsers]
    
    @swagger_auto_schema(
        operation_description="Récupère les statistiques de sécurité",
        responses={200: openapi.Response(description="Statistiques de sécurité")}
    )
    def get(self, request):
        now = timezone.now()
        last_24h = now - timedelta(hours=24)
        
        # Tentatives de connexion
        total_attempts = HistoriqueConnexion.objects.filter(
            date_connexion__gte=last_24h
        ).count()
        
        successful_logins = HistoriqueConnexion.objects.filter(
            date_connexion__gte=last_24h,
            succes=True
        ).count()
        
        failed_attempts = HistoriqueConnexion.objects.filter(
            date_connexion__gte=last_24h,
            succes=False
        ).count()
        
        # IPs bloquées (simulé pour l'instant)
        blocked_ips = 0
        
        return Response({
            'totalAttempts': total_attempts,
            'successfulLogins': successful_logins,
            'failedAttempts': failed_attempts,
            'blockedIPs': blocked_ips
        })


class SecurityAlertsView(APIView):
    """API pour les alertes de sécurité"""
    permission_classes = [IsAuthenticated, CanManageUsers]
    
    @swagger_auto_schema(
        operation_description="Récupère les alertes de sécurité",
        responses={200: openapi.Response(description="Alertes de sécurité")}
    )
    def get(self, request):
        alerts = []
        now = timezone.now()
        last_hour = now - timedelta(hours=1)
        
        # Vérifier les tentatives de connexion échouées
        failed_attempts = HistoriqueConnexion.objects.filter(
            date_connexion__gte=last_hour,
            succes=False
        ).values('adresse_ip').annotate(count=Count('id')).filter(count__gte=3)
        
        for attempt in failed_attempts:
            alerts.append({
                'id': f"failed-{attempt['adresse_ip']}",
                'title': 'Tentatives de connexion suspectes',
                'description': f"Plusieurs tentatives de connexion échouées depuis l'IP {attempt['adresse_ip']}",
                'severity': 'high',
                'timestamp': now.isoformat()
            })
        
        # Vérifier les nouvelles connexions depuis des appareils inconnus
        new_devices = SessionUtilisateur.objects.filter(
            date_creation__gte=now - timedelta(hours=24)
        ).count()
        
        if new_devices > 10:
            alerts.append({
                'id': 'new-devices',
                'title': 'Nombreuses nouvelles connexions',
                'description': f"{new_devices} nouvelles connexions depuis de nouveaux appareils",
                'severity': 'medium',
                'timestamp': now.isoformat()
            })
        
        return Response(alerts)


class LoginAttemptsView(APIView):
    """API pour les tentatives de connexion récentes"""
    permission_classes = [IsAuthenticated, CanManageUsers]
    
    @swagger_auto_schema(
        operation_description="Récupère les tentatives de connexion récentes",
        manual_parameters=[
            openapi.Parameter('limit', openapi.IN_QUERY, description="Nombre de tentatives à retourner", type=openapi.TYPE_INTEGER, default=20)
        ],
        responses={200: openapi.Response(description="Liste des tentatives de connexion")}
    )
    def get(self, request):
        limit = int(request.query_params.get('limit', 20))
        
        attempts = HistoriqueConnexion.objects.select_related('user').order_by('-date_connexion')[:limit]
        
        result = []
        for attempt in attempts:
            result.append({
                'id': attempt.id,
                'email': attempt.user.email if attempt.user else 'Inconnu',
                'ip': attempt.adresse_ip or 'N/A',
                'userAgent': attempt.user_agent or 'N/A',
                'success': attempt.succes,
                'timestamp': attempt.date_connexion.isoformat()
            })
        
        return Response(result)


class BroadcastNotificationView(APIView):
    """API pour envoyer des notifications en masse"""
    permission_classes = [IsAuthenticated, CanManageUsers]
    
    @swagger_auto_schema(
        operation_description="Envoie une notification à un groupe d'utilisateurs",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'message', 'recipients'],
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Titre de la notification'),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Message de la notification'),
                'recipients': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Type de destinataires',
                    enum=['all', 'super_admin', 'admin_hopital', 'specialiste', 'pharmacien', 'employe_pharmacie', 'agent_enregistrement', 'patient']
                ),
                'type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Type de notification',
                    enum=['email', 'sms', 'push', 'all'],
                    default='email'
                )
            }
        ),
        responses={
            200: openapi.Response(description="Notification envoyée avec succès"),
            400: openapi.Response(description="Données invalides")
        }
    )
    def post(self, request):
        title = request.data.get('title')
        message = request.data.get('message')
        recipients = request.data.get('recipients')
        notification_type = request.data.get('type', 'email')
        
        if not title or not message or not recipients:
            return Response(
                {'error': 'Titre, message et destinataires sont requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Déterminer les utilisateurs cibles
        if recipients == 'all':
            users = User.objects.filter(actif=True)
        else:
            users = User.objects.filter(actif=True, role=recipients)
        
        # Créer les notifications
        notifications_created = 0
        for user in users:
            Notification.objects.create(
                user=user,
                type_notification='autre',
                titre=title,
                message=message,
                data={
                    'broadcast': True,
                    'notification_type': notification_type,
                    'sent_by': request.user.id
                }
            )
            notifications_created += 1
        
        return Response({
            'success': True,
            'message': f'Notification envoyée à {notifications_created} utilisateur(s)',
            'recipients_count': notifications_created
        })
