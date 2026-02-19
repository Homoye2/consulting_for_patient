"""
Classe d'authentification personnalisée pour permettre l'accès public
même avec des tokens JWT invalides ou expirés.
"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class OptionalJWTAuthentication(JWTAuthentication):
    """
    Authentification JWT qui ne lève pas d'exception si le token est invalide.
    
    Au lieu de rejeter la requête avec 401, cette classe retourne None,
    permettant à Django REST Framework de vérifier les permissions de la vue.
    
    Si la vue a AllowAny, la requête passe.
    Si la vue a IsAuthenticated, la requête est rejetée avec 401.
    """
    
    def authenticate(self, request):
        """
        Tente d'authentifier la requête avec un token JWT.
        
        Si le token est valide, retourne (user, token).
        Si le token est invalide ou absent, retourne None au lieu de lever une exception.
        """
        try:
            return super().authenticate(request)
        except AuthenticationFailed:
            # Token invalide ou expiré - retourner None au lieu de lever une exception
            # Cela permet aux vues avec AllowAny de fonctionner
            return None
        except Exception:
            # Toute autre erreur - retourner None
            return None
