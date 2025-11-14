"""
Configuration Swagger personnalisée pour améliorer la documentation des APIs
"""
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Schémas de réponse personnalisés
patient_response = openapi.Response(
    description="Détails d'un patient",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'nom': openapi.Schema(type=openapi.TYPE_STRING),
            'prenom': openapi.Schema(type=openapi.TYPE_STRING),
            'dob': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            'sexe': openapi.Schema(type=openapi.TYPE_STRING, enum=['M', 'F']),
            'telephone': openapi.Schema(type=openapi.TYPE_STRING),
            'age': openapi.Schema(type=openapi.TYPE_INTEGER),
        }
    )
)

consultation_response = openapi.Response(
    description="Détails d'une consultation PF",
    schema=openapi.Schema(type=openapi.TYPE_OBJECT)
)

# Paramètres de requête communs
date_debut_param = openapi.Parameter(
    'date_debut',
    openapi.IN_QUERY,
    description="Date de début (format: YYYY-MM-DD)",
    type=openapi.TYPE_STRING,
    format=openapi.FORMAT_DATE
)

date_fin_param = openapi.Parameter(
    'date_fin',
    openapi.IN_QUERY,
    description="Date de fin (format: YYYY-MM-DD)",
    type=openapi.TYPE_STRING,
    format=openapi.FORMAT_DATE
)

# Schémas de requête pour l'authentification
login_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['email', 'password'],
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
        'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
    }
)

login_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'access': openapi.Schema(type=openapi.TYPE_STRING),
        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
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

