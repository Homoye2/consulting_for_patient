"""
Vue pour l'authentification Google OAuth
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from google.auth.transport import requests
from google.oauth2 import id_token
from django.conf import settings
from .models import User
import os


@api_view(['POST'])
@permission_classes([AllowAny])
def google_auth(request):
    """
    Authentification via Google OAuth
    Accepte un token Google ID et retourne un JWT
    """
    token = request.data.get('token')
    
    if not token:
        return Response(
            {'error': 'Token Google requis'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Vérifier le token Google
        # En production, utilisez GOOGLE_CLIENT_ID depuis les variables d'environnement
        GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')
        
        try:
            if GOOGLE_CLIENT_ID:
                idinfo = id_token.verify_oauth2_token(
                    token,
                    requests.Request(),
                    GOOGLE_CLIENT_ID
                )
            else:
                # En développement, on accepte le token sans vérification stricte
                # En production, il faut absolument configurer GOOGLE_CLIENT_ID
                idinfo = id_token.verify_oauth2_token(
                    token,
                    requests.Request(),
                    skip_audience_check=True  # Seulement en développement
                )
        except ValueError as e:
            # Si la vérification échoue, essayer sans vérification d'audience (dev seulement)
            if not GOOGLE_CLIENT_ID:
                idinfo = id_token.verify_oauth2_token(
                    token,
                    requests.Request(),
                    skip_audience_check=True
                )
            else:
                raise
        
        # Extraire les informations utilisateur
        email = idinfo.get('email')
        nom = idinfo.get('name', '').split()[0] if idinfo.get('name') else email.split('@')[0]
        google_id = idinfo.get('sub')
        
        if not email:
            return Response(
                {'error': 'Email non disponible dans le token Google'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier ou créer l'utilisateur
        try:
            user = User.objects.get(email=email)
            # Mettre à jour le nom si nécessaire
            if not user.nom or user.nom == email.split('@')[0]:
                user.nom = nom
                user.save()
        except User.DoesNotExist:
            # Créer un nouvel utilisateur
            # Par défaut, rôle 'patient' pour les nouveaux utilisateurs Google
            user = User.objects.create_user(
                email=email,
                nom=nom,
                role='patient',  # Rôle par défaut
                actif=True
            )
        
        # Bloquer l'accès aux pharmaciens
        if user.role == 'pharmacien':
            return Response(
                {
                    'error': 'Les pharmaciens doivent utiliser l\'application dédiée aux pharmacies pour se connecter.',
                    'pharmacien_blocked': True
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Vérifier que l'utilisateur est actif
        if not user.actif or not user.is_active:
            return Response(
                {'error': 'Ce compte utilisateur est désactivé.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Générer les tokens JWT
        refresh = RefreshToken.for_user(user)
        refresh['email'] = user.email
        refresh['role'] = user.role
        refresh['nom'] = user.nom
        
        # Vérifier si l'utilisateur a un profil patient
        is_patient = hasattr(user, 'patient_profile')
        patient_id = None
        if is_patient:
            patient_id = user.patient_profile.id
        
        # Préparer la réponse
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'nom': user.nom,
                'role': user.role,
                'is_patient': is_patient,
                'patient_id': patient_id,
            }
        }
        
        return Response(data, status=status.HTTP_200_OK)
        
    except ValueError as e:
        # Token invalide
        return Response(
            {'error': f'Token Google invalide: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de l\'authentification Google: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

