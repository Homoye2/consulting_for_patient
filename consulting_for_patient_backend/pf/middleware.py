from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import SessionUtilisateur, HistoriqueConnexion
import re

User = get_user_model()


class SecurityTrackingMiddleware(MiddlewareMixin):
    """Middleware pour tracker les sessions et l'historique de connexion"""
    
    def process_request(self, request):
        # Mettre à jour la dernière activité pour les utilisateurs authentifiés
        if request.user.is_authenticated:
            self.update_session_activity(request)
    
    def update_session_activity(self, request):
        """Met à jour l'activité de la session utilisateur"""
        try:
            session_key = request.session.session_key
            if session_key:
                session_obj, created = SessionUtilisateur.objects.get_or_create(
                    session_key=session_key,
                    defaults={
                        'user': request.user,
                        'ip_address': self.get_client_ip(request),
                        'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                        'device_info': self.parse_device_info(request.META.get('HTTP_USER_AGENT', '')),
                        'location': '',  # Peut être étendu avec une API de géolocalisation
                        'active': True
                    }
                )
                
                if not created:
                    # Mettre à jour la dernière activité
                    session_obj.derniere_activite = timezone.now()
                    session_obj.active = True
                    session_obj.save(update_fields=['derniere_activite', 'active'])
        except Exception as e:
            # Log l'erreur mais ne pas interrompre la requête
            print(f"Erreur lors de la mise à jour de la session: {e}")
    
    def get_client_ip(self, request):
        """Récupère l'adresse IP du client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def parse_device_info(self, user_agent):
        """Parse les informations de l'appareil depuis le User-Agent"""
        if not user_agent:
            return 'Inconnu'
        
        # Détection simple du navigateur
        browsers = {
            'Chrome': r'Chrome/[\d.]+',
            'Firefox': r'Firefox/[\d.]+',
            'Safari': r'Safari/[\d.]+',
            'Edge': r'Edge/[\d.]+',
            'Opera': r'Opera/[\d.]+'
        }
        
        # Détection de l'OS
        os_patterns = {
            'Windows': r'Windows NT',
            'macOS': r'Mac OS X',
            'Linux': r'Linux',
            'iOS': r'iPhone|iPad',
            'Android': r'Android'
        }
        
        browser = 'Inconnu'
        os = 'Inconnu'
        
        for name, pattern in browsers.items():
            if re.search(pattern, user_agent):
                browser = name
                break
        
        for name, pattern in os_patterns.items():
            if re.search(pattern, user_agent):
                os = name
                break
        
        return f"{browser} sur {os}"


def log_login_attempt(user, request, status, details=''):
    """Fonction utilitaire pour enregistrer les tentatives de connexion"""
    try:
        HistoriqueConnexion.objects.create(
            user=user,
            statut=status,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            device_info=parse_device_info(request.META.get('HTTP_USER_AGENT', '')),
            location='',  # Peut être étendu
            details=details
        )
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de l'historique: {e}")


def get_client_ip(request):
    """Récupère l'adresse IP du client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def parse_device_info(user_agent):
    """Parse les informations de l'appareil depuis le User-Agent"""
    if not user_agent:
        return 'Inconnu'
    
    # Détection simple du navigateur
    browsers = {
        'Chrome': r'Chrome/[\d.]+',
        'Firefox': r'Firefox/[\d.]+',
        'Safari': r'Safari/[\d.]+',
        'Edge': r'Edge/[\d.]+',
        'Opera': r'Opera/[\d.]+'
    }
    
    # Détection de l'OS
    os_patterns = {
        'Windows': r'Windows NT',
        'macOS': r'Mac OS X',
        'Linux': r'Linux',
        'iOS': r'iPhone|iPad',
        'Android': r'Android'
    }
    
    browser = 'Inconnu'
    os = 'Inconnu'
    
    for name, pattern in browsers.items():
        if re.search(pattern, user_agent):
            browser = name
            break
    
    for name, pattern in os_patterns.items():
        if re.search(pattern, user_agent):
            os = name
            break
    
    return f"{browser} sur {os}"