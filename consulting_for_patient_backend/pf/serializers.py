from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
    User, Patient, MethodeContraceptive, RendezVous,
    ConsultationPF, StockItem, Prescription, MouvementStock,
    LandingPageContent, Service, Value
)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer personnalisé pour JWT avec informations utilisateur"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remplacer le champ username par email
        if 'username' in self.fields:
            email_field = self.fields.pop('username')
            email_field.label = 'Email'
            self.fields['email'] = email_field
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Ajouter des informations personnalisées au token
        token['email'] = user.email
        token['role'] = user.role
        token['nom'] = user.nom
        return token
    
    def validate(self, attrs):
        # Extraire email et password
        email = attrs.get('email')
        password = attrs.get('password')
        
        if not email or not password:
            raise serializers.ValidationError("L'email et le mot de passe sont requis.")
        
        # Authentifier l'utilisateur avec email au lieu de username
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Aucun compte trouvé avec cet email.")
        
        # Vérifier le mot de passe
        if not user.check_password(password):
            raise serializers.ValidationError("Mot de passe incorrect.")
        
        # Vérifier que l'utilisateur est actif
        if not user.actif:
            raise serializers.ValidationError("Ce compte utilisateur est désactivé.")
        
        # Vérifier que l'utilisateur peut s'authentifier
        if not user.is_active:
            raise serializers.ValidationError("Ce compte utilisateur est désactivé.")
        
        # Créer le token
        refresh = self.get_token(user)
        
        # Préparer la réponse
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        # Ajouter des informations utilisateur à la réponse
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'nom': user.nom,
            'role': user.role,
        }
        
        return data


class UserSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle User"""
    
    class Meta:
        model = User
        fields = ['id', 'nom', 'email', 'role', 'actif', 'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer un utilisateur avec mot de passe"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['id', 'nom', 'email', 'password', 'password_confirm', 'role', 'actif']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class PatientSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Patient"""
    age = serializers.ReadOnlyField()
    
    class Meta:
        model = Patient
        fields = [
            'id', 'nom', 'prenom', 'dob', 'sexe', 'telephone', 
            'adresse', 'antecedents', 'allergies', 'age', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PatientListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des patients"""
    age = serializers.ReadOnlyField()
    
    class Meta:
        model = Patient
        fields = ['id', 'nom', 'prenom', 'dob', 'sexe', 'telephone', 'age']


class MethodeContraceptiveSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle MethodeContraceptive"""
    
    class Meta:
        model = MethodeContraceptive
        fields = ['id', 'nom', 'categorie', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class RendezVousSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle RendezVous"""
    patient_nom = serializers.CharField(source='patient.nom', read_only=True)
    patient_prenom = serializers.CharField(source='patient.prenom', read_only=True)
    professionnel_nom = serializers.CharField(source='user.nom', read_only=True)
    
    class Meta:
        model = RendezVous
        fields = [
            'id', 'patient', 'patient_nom', 'patient_prenom', 'user', 
            'professionnel_nom', 'datetime', 'statut', 'notes', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ConsultationPFSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle ConsultationPF"""
    patient_nom = serializers.CharField(source='patient.nom', read_only=True)
    patient_prenom = serializers.CharField(source='patient.prenom', read_only=True)
    professionnel_nom = serializers.CharField(source='user.nom', read_only=True)
    methode_proposee_nom = serializers.CharField(source='methode_proposee.nom', read_only=True)
    methode_prescite_nom = serializers.CharField(source='methode_prescite.nom', read_only=True)
    
    class Meta:
        model = ConsultationPF
        fields = [
            'id', 'patient', 'patient_nom', 'patient_prenom', 'user', 
            'professionnel_nom', 'date', 'anamnese', 'examen', 
            'methode_proposee', 'methode_proposee_nom', 'methode_prescite', 
            'methode_prescite_nom', 'methode_posee', 'effets_secondaires', 
            'notes', 'observation', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ConsultationPFListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des consultations"""
    patient_nom_complet = serializers.SerializerMethodField()
    professionnel_nom = serializers.CharField(source='user.nom', read_only=True)
    methode_prescite_nom = serializers.CharField(source='methode_prescite.nom', read_only=True)
    
    class Meta:
        model = ConsultationPF
        fields = [
            'id', 'patient_nom_complet', 'professionnel_nom', 'date', 
            'methode_prescite_nom', 'methode_posee'
        ]
    
    def get_patient_nom_complet(self, obj):
        return f"{obj.patient.nom} {obj.patient.prenom}"


class StockItemSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle StockItem"""
    methode_nom = serializers.CharField(source='methode.nom', read_only=True)
    methode_categorie = serializers.CharField(source='methode.categorie', read_only=True)
    est_en_rupture = serializers.ReadOnlyField()
    est_sous_seuil = serializers.ReadOnlyField()
    
    class Meta:
        model = StockItem
        fields = [
            'id', 'methode', 'methode_nom', 'methode_categorie', 
            'quantite', 'seuil', 'est_en_rupture', 'est_sous_seuil',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PrescriptionSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Prescription"""
    consultation_patient = serializers.CharField(source='consultation.patient.nom', read_only=True)
    methode_nom = serializers.CharField(source='methode.nom', read_only=True)
    
    class Meta:
        model = Prescription
        fields = [
            'id', 'consultation', 'consultation_patient', 'methode', 
            'methode_nom', 'dosage', 'remarque', 'date_prescription'
        ]
        read_only_fields = ['id', 'date_prescription']


class MouvementStockSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle MouvementStock"""
    stock_item_methode = serializers.CharField(source='stock_item.methode.nom', read_only=True)
    user_nom = serializers.CharField(source='user.nom', read_only=True)
    
    class Meta:
        model = MouvementStock
        fields = [
            'id', 'stock_item', 'stock_item_methode', 'type_mouvement', 
            'quantite', 'motif', 'user', 'user_nom', 'date_mouvement'
        ]
        read_only_fields = ['id', 'date_mouvement']


class MouvementStockCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer un mouvement de stock"""
    
    class Meta:
        model = MouvementStock
        fields = ['id', 'stock_item', 'type_mouvement', 'quantite', 'motif']
    
    def validate(self, attrs):
        stock_item = attrs['stock_item']
        type_mouvement = attrs['type_mouvement']
        quantite = attrs['quantite']
        
        if type_mouvement == 'sortie' and quantite > stock_item.quantite:
            raise serializers.ValidationError(
                {"quantite": f"Stock insuffisant. Stock disponible: {stock_item.quantite}"}
            )
        
        return attrs
    
    def create(self, validated_data):
        mouvement = super().create(validated_data)
        stock_item = mouvement.stock_item
        
        # Mise à jour automatique du stock
        if mouvement.type_mouvement == 'entree':
            stock_item.quantite += mouvement.quantite
        elif mouvement.type_mouvement == 'sortie':
            stock_item.quantite -= mouvement.quantite
        elif mouvement.type_mouvement == 'inventaire':
            stock_item.quantite = mouvement.quantite
        elif mouvement.type_mouvement == 'perte':
            stock_item.quantite -= mouvement.quantite
        
        stock_item.save()
        return mouvement


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Service"""
    
    class Meta:
        model = Service
        fields = ['id', 'titre', 'description', 'icone', 'ordre']
        read_only_fields = ['id']


class ValueSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Value"""
    
    class Meta:
        model = Value
        fields = ['id', 'titre', 'description', 'icone', 'ordre']
        read_only_fields = ['id']


class LandingPageContentSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle LandingPageContent"""
    services = ServiceSerializer(many=True, read_only=True)
    values = ValueSerializer(many=True, read_only=True)
    
    class Meta:
        model = LandingPageContent
        fields = [
            'id', 'logo_text',
            'hero_title', 'hero_description', 'hero_button_primary', 'hero_button_secondary',
            'about_title', 'about_description_1', 'about_description_2',
            'about_stat_1_value', 'about_stat_1_label', 'about_stat_2_value', 'about_stat_2_label',
            'services_title', 'services_subtitle', 'services',
            'values_title', 'values_subtitle', 'values',
            'footer_about_text', 'footer_address', 'footer_phone', 'footer_email',
            'footer_facebook', 'footer_twitter', 'footer_instagram', 'footer_linkedin',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LandingPageContentUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour mettre à jour le contenu de la landing page"""
    
    class Meta:
        model = LandingPageContent
        fields = [
            'logo_text',
            'hero_title', 'hero_description', 'hero_button_primary', 'hero_button_secondary',
            'about_title', 'about_description_1', 'about_description_2',
            'about_stat_1_value', 'about_stat_1_label', 'about_stat_2_value', 'about_stat_2_label',
            'services_title', 'services_subtitle',
            'values_title', 'values_subtitle',
            'footer_about_text', 'footer_address', 'footer_phone', 'footer_email',
            'footer_facebook', 'footer_twitter', 'footer_instagram', 'footer_linkedin',
        ]
