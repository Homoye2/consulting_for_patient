from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
    User, Patient, RendezVous,
    ConsultationPF, LandingPageContent, Service, Value, ContactMessage, Pharmacie,
    Hopital, Specialite, Specialiste, DisponibiliteSpecialiste,
    Produit, StockProduit, CommandePharmacie, LigneCommande,
    Notification, RapportConsultation, AvisSpecialiste,
    SessionUtilisateur, HistoriqueConnexion, VentePharmacie, LigneVente,
    EmployePharmacie, Registre, Ordonnance, LigneOrdonnance, DossierMedical,
    FichierDossierMedical, Fournisseur, FactureFournisseur, LigneFactureFournisseur
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
        
        # Bloquer l'accès aux pharmaciens - ils doivent utiliser l'application dédiée
        if user.role == 'pharmacien':
            raise serializers.ValidationError(
                'Les pharmaciens doivent utiliser l\'application dédiée aux pharmacies pour se connecter. Veuillez utiliser l\'application réservée aux pharmacies.',
                code='pharmacien_blocked'
            )
        
        # Créer le token
        refresh = self.get_token(user)
        
        # Vérifier si l'utilisateur a un profil patient
        is_patient = hasattr(user, 'patient_profile')
        patient_id = None
        if is_patient:
            patient_id = user.patient_profile.id
        
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
            'is_patient': is_patient,
            'patient_id': patient_id,
        }
        
        return data


class PharmacyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer spécialement conçu pour l'authentification des pharmaciens et employés"""
    
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
            raise serializers.ValidationError("Ce compte utilisateur est désactivé. Contactez votre administrateur.")
        
        # Vérifier que l'utilisateur peut s'authentifier
        if not user.is_active:
            raise serializers.ValidationError("Ce compte utilisateur est désactivé. Contactez votre administrateur.")
        
        # Vérifier que c'est bien un pharmacien ou un employé de pharmacie
        if user.role not in ['pharmacien', 'employe_pharmacie']:
            raise serializers.ValidationError(
                'Cette application est réservée aux pharmaciens et employés de pharmacie uniquement.',
                code='not_pharmacy_user'
            )
        
        # Vérifier que la pharmacie associée est active
        try:
            from .models import Pharmacie, EmployePharmacie
            
            # Pour les pharmaciens propriétaires
            if user.role == 'pharmacien':
                pharmacie = Pharmacie.objects.get(user=user)
                if not pharmacie.actif:
                    raise serializers.ValidationError(
                        "La pharmacie associée à ce compte est désactivée. Contactez l'administrateur système.",
                        code='pharmacy_disabled'
                    )
            
            # Pour les employés de pharmacie
            elif user.role == 'employe_pharmacie':
                try:
                    employe = EmployePharmacie.objects.select_related('pharmacie').get(user=user)
                    if not employe.actif:
                        raise serializers.ValidationError(
                            "Votre compte employé est désactivé. Contactez l'administrateur de la pharmacie.",
                            code='employee_disabled'
                        )
                    if not employe.pharmacie.actif:
                        raise serializers.ValidationError(
                            "La pharmacie associée à ce compte est désactivée. Contactez l'administrateur système.",
                            code='pharmacy_disabled'
                        )
                except EmployePharmacie.DoesNotExist:
                    raise serializers.ValidationError(
                        "Aucune pharmacie n'est associée à ce compte employé. Contactez l'administrateur système.",
                        code='no_pharmacy'
                    )
                    
        except Pharmacie.DoesNotExist:
            raise serializers.ValidationError(
                "Aucune pharmacie n'est associée à ce compte. Contactez l'administrateur système.",
                code='no_pharmacy'
            )
        
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


class HospitalTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer spécialement conçu pour l'authentification des admins hôpitaux et spécialistes"""
    
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
            raise serializers.ValidationError("Ce compte utilisateur est désactivé. Contactez votre administrateur.")
        
        # Vérifier que l'utilisateur peut s'authentifier
        if not user.is_active:
            raise serializers.ValidationError("Ce compte utilisateur est désactivé. Contactez votre administrateur.")
        
        # Vérifier que c'est bien un admin hôpital ou un spécialiste
        if user.role not in ['admin_hopital', 'specialiste']:
            raise serializers.ValidationError(
                'Cette application est réservée aux administrateurs d\'hôpital et aux spécialistes uniquement.',
                code='not_hospital_user'
            )
        
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
            'id', 'nom', 'prenom', 'dob', 'sexe', 'telephone', 'email',
            'adresse', 'antecedents', 'allergies', 'age', 'user',
            'ville_actuelle', 'preferences_notification',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PatientListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des patients"""
    age = serializers.ReadOnlyField()
    
    class Meta:
        model = Patient
        fields = ['id', 'nom', 'prenom', 'dob', 'sexe', 'telephone', 'age']


class RendezVousSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle RendezVous"""
    patient_nom = serializers.CharField(source='patient.nom', read_only=True)
    patient_prenom = serializers.CharField(source='patient.prenom', read_only=True)
    specialiste_nom = serializers.CharField(source='specialiste.user.nom', read_only=True)
    hopital_nom = serializers.CharField(source='hopital.nom', read_only=True)
    specialite_nom = serializers.CharField(source='specialiste.specialite.nom', read_only=True)
    
    class Meta:
        model = RendezVous
        fields = [
            'id', 'patient', 'patient_nom', 'patient_prenom', 'specialiste', 
            'specialiste_nom', 'hopital', 'hopital_nom', 'specialite_nom',
            'datetime', 'statut', 'motif', 'confirme_par_specialiste',
            'date_confirmation', 'date_refus', 'motif_refus', 'notes', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'date_confirmation', 'date_refus']


class ConsultationPFSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle ConsultationPF"""
    patient_nom = serializers.CharField(source='patient.nom', read_only=True)
    patient_prenom = serializers.CharField(source='patient.prenom', read_only=True)
    specialiste_nom = serializers.CharField(source='specialiste.user.nom', read_only=True)
    specialiste_specialite = serializers.CharField(source='specialiste.specialite.nom', read_only=True)
    hopital_nom = serializers.CharField(source='hopital.nom', read_only=True)
    hopital_adresse = serializers.CharField(source='hopital.adresse', read_only=True)
    hopital_telephone = serializers.CharField(source='hopital.telephone', read_only=True)
    specialite_nom = serializers.CharField(source='specialiste.specialite.nom', read_only=True)
    
    class Meta:
        model = ConsultationPF
        fields = [
            'id', 'patient', 'patient_nom', 'patient_prenom', 'specialiste', 
            'specialiste_nom', 'specialiste_specialite', 'hopital', 'hopital_nom', 
            'hopital_adresse', 'hopital_telephone', 'specialite_nom',
            'rendez_vous', 'date', 'anamnese', 'examen', 
            'methode_posee', 'effets_secondaires', 
            'notes', 'observation', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ConsultationPFListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des consultations"""
    patient_nom_complet = serializers.SerializerMethodField()
    professionnel_nom = serializers.SerializerMethodField()
    
    class Meta:
        model = ConsultationPF
        fields = [
            'id', 'patient_nom_complet', 'professionnel_nom', 'date', 
            'methode_posee', 'anamnese', 'examen',
            'effets_secondaires', 'notes', 'observation'
        ]
    
    def get_patient_nom_complet(self, obj):
        return f"{obj.patient.nom} {obj.patient.prenom}"
    
    def get_professionnel_nom(self, obj):
        return obj.specialiste.user.nom if obj.specialiste else ''


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Service"""
    
    class Meta:
        model = Service
        fields = ['id', 'titre', 'description', 'contenu_detail', 'icone', 'ordre']
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


class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer pour les messages de contact"""
    
    class Meta:
        model = ContactMessage
        fields = ['id', 'nom', 'email', 'sujet', 'message', 'patient', 'lu', 'date_creation']
        read_only_fields = ['id', 'lu', 'date_creation']


# Nouveaux Serializers pour la nouvelle architecture

class HopitalSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Hopital"""
    admin_hopital_nom = serializers.CharField(source='admin_hopital.nom', read_only=True)
    admin_hopital_email = serializers.CharField(source='admin_hopital.email', read_only=True)
    
    class Meta:
        model = Hopital
        fields = [
            'id', 'nom', 'code_hopital', 'adresse', 'ville', 'pays',
            'telephone', 'email', 'latitude', 'longitude', 'logo',
            'couleur_theme', 'description', 'horaires_ouverture',
            'admin_hopital', 'admin_hopital_nom', 'admin_hopital_email',
            'actif', 'date_inscription', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'date_inscription', 'created_at', 'updated_at']


class HopitalListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des hôpitaux"""
    
    class Meta:
        model = Hopital
        fields = ['id', 'nom', 'code_hopital', 'ville', 'telephone', 'email', 'actif']


class SpecialiteSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Specialite"""
    
    class Meta:
        model = Specialite
        fields = ['id', 'nom', 'code', 'description', 'icone', 'actif', 'created_at']
        read_only_fields = ['id', 'created_at']


class SpecialisteSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Specialiste"""
    user_nom = serializers.CharField(source='user.nom', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    hopital_nom = serializers.CharField(source='hopital.nom', read_only=True)
    specialite_nom = serializers.CharField(source='specialite.nom', read_only=True)
    
    class Meta:
        model = Specialiste
        fields = [
            'id', 'user', 'user_nom', 'user_email', 'hopital', 'hopital_nom',
            'specialite', 'specialite_nom', 'numero_ordre', 'titre',
            'annees_experience', 'bio', 'tarif_consultation', 'duree_consultation',
            'photo', 'accepte_nouveaux_patients', 'consultation_en_ligne',
            'note_moyenne', 'nombre_avis', 'actif', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'note_moyenne', 'nombre_avis', 'created_at', 'updated_at']


class DisponibiliteSpecialisteSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle DisponibiliteSpecialiste"""
    specialiste_nom = serializers.CharField(source='specialiste.user.nom', read_only=True)
    
    class Meta:
        model = DisponibiliteSpecialiste
        fields = [
            'id', 'specialiste', 'specialiste_nom', 'jour_semaine',
            'heure_debut', 'heure_fin', 'date_debut_exception',
            'date_fin_exception', 'motif_exception', 'actif', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ProduitSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Produit"""
    
    class Meta:
        model = Produit
        fields = [
            'id', 'nom', 'code_barre', 'categorie', 'description', 'composition',
            'posologie', 'contre_indications', 'fabricant', 'prix_unitaire',
            'unite', 'prescription_requise', 'image', 'actif', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StockProduitSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle StockProduit"""
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)
    pharmacie_nom = serializers.CharField(source='pharmacie.nom', read_only=True)
    est_en_rupture = serializers.ReadOnlyField()
    est_sous_seuil = serializers.ReadOnlyField()
    est_proche_expiration = serializers.ReadOnlyField()
    
    class Meta:
        model = StockProduit
        fields = [
            'id', 'pharmacie', 'pharmacie_nom', 'produit', 'produit_nom',
            'quantite', 'seuil_alerte', 'numero_lot', 'date_expiration',
            'prix_vente', 'est_en_rupture', 'est_sous_seuil',
            'est_proche_expiration', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'est_en_rupture', 'est_sous_seuil',
                           'est_proche_expiration', 'created_at', 'updated_at']


class LigneCommandeSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle LigneCommande"""
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)
    
    class Meta:
        model = LigneCommande
        fields = [
            'id', 'commande', 'produit', 'produit_nom', 'quantite',
            'prix_unitaire', 'prix_total', 'created_at'
        ]
        read_only_fields = ['id', 'prix_total', 'created_at']


class CommandePharmacieSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle CommandePharmacie"""
    patient_nom = serializers.CharField(source='patient.nom', read_only=True)
    patient_prenom = serializers.CharField(source='patient.prenom', read_only=True)
    patient_telephone = serializers.CharField(source='patient.telephone', read_only=True)
    pharmacie_nom = serializers.CharField(source='pharmacie.nom', read_only=True)
    lignes = LigneCommandeSerializer(many=True, read_only=True)
    
    class Meta:
        model = CommandePharmacie
        fields = [
            'id', 'numero_commande', 'patient', 'patient_nom', 'patient_prenom', 'patient_telephone',
            'pharmacie', 'pharmacie_nom', 'statut', 'montant_total',
            'prescription_image', 'notes_patient', 'notes_pharmacie',
            'date_commande', 'date_confirmation', 'date_preparation',
            'date_prete', 'date_recuperation', 'lignes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'numero_commande', 'date_commande', 'created_at', 'updated_at']


class CommandePharmacieCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer une commande avec ses lignes"""
    lignes = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        help_text="Liste des lignes de commande avec produit, quantite, prix_unitaire"
    )
    
    class Meta:
        model = CommandePharmacie
        fields = [
            'pharmacie', 'notes_patient', 'prescription_image', 'lignes'
        ]
    
    def validate_lignes(self, value):
        """Valider les lignes de commande"""
        if not value:
            raise serializers.ValidationError("Au moins une ligne de commande est requise.")
        
        for ligne in value:
            if 'produit' not in ligne:
                raise serializers.ValidationError("produit est requis pour chaque ligne.")
            if 'quantite' not in ligne or ligne['quantite'] <= 0:
                raise serializers.ValidationError("quantite doit être supérieure à 0.")
            if 'prix_unitaire' not in ligne or ligne['prix_unitaire'] <= 0:
                raise serializers.ValidationError("prix_unitaire doit être supérieur à 0.")
        
        return value
    
    def create(self, validated_data):
        from django.db import transaction
        
        lignes_data = validated_data.pop('lignes')
        
        # Récupérer le patient depuis le contexte (request.user)
        request = self.context.get('request')
        if not request or not hasattr(request.user, 'patient_profile'):
            raise serializers.ValidationError("Utilisateur non authentifié ou n'est pas un patient.")
        
        patient = request.user.patient_profile
        
        with transaction.atomic():
            # Créer la commande
            commande = CommandePharmacie.objects.create(
                patient=patient,
                **validated_data
            )
            
            from decimal import Decimal
            montant_total = Decimal('0')
            
            # Créer les lignes de commande
            for ligne_data in lignes_data:
                produit_id = ligne_data['produit']
                quantite = ligne_data['quantite']
                prix_unitaire = ligne_data['prix_unitaire']
                
                # Vérifier que le produit existe
                try:
                    produit = Produit.objects.get(id=produit_id)
                except Produit.DoesNotExist:
                    raise serializers.ValidationError(f"Produit avec ID {produit_id} non trouvé.")
                
                # Créer la ligne de commande
                ligne_commande = LigneCommande.objects.create(
                    commande=commande,
                    produit=produit,
                    quantite=quantite,
                    prix_unitaire=Decimal(str(prix_unitaire))
                )
                
                montant_total += ligne_commande.prix_total
            
            # Mettre à jour le montant total de la commande
            commande.montant_total = montant_total
            commande.save()
            
            # Créer une notification pour la pharmacie
            try:
                pharmacie_user = commande.pharmacie.user
                Notification.objects.create(
                    user=pharmacie_user,
                    type_notification='commande_confirmee',
                    titre='Nouvelle commande',
                    message=f'Nouvelle commande {commande.numero_commande} de {patient.nom} {patient.prenom}.',
                    commande=commande
                )
            except Exception as e:
                # Ne pas bloquer la création de la commande si la notification échoue
                print(f"Erreur lors de la création de la notification: {e}")
            
            return commande


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Notification"""
    user_nom = serializers.CharField(source='user.nom', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'user_nom', 'type_notification', 'titre', 'message',
            'rendez_vous', 'commande', 'data', 'lu', 'date_lecture', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'date_lecture']


class RapportConsultationSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle RapportConsultation"""
    consultation_patient = serializers.CharField(source='consultation.patient.nom', read_only=True)
    consultation_date = serializers.DateTimeField(source='consultation.date', read_only=True)
    
    class Meta:
        model = RapportConsultation
        fields = [
            'id', 'consultation', 'consultation_patient', 'consultation_date',
            'diagnostic', 'traitement_prescrit', 'recommandations',
            'suivi_necessaire', 'date_prochain_rdv', 'documents',
            'envoye_patient', 'date_envoi', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'date_envoi']


class AvisSpecialisteSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle AvisSpecialiste"""
    specialiste_nom = serializers.CharField(source='specialiste.user.nom', read_only=True)
    patient_nom = serializers.CharField(source='patient.nom', read_only=True)
    
    class Meta:
        model = AvisSpecialiste
        fields = [
            'id', 'specialiste', 'specialiste_nom', 'patient', 'patient_nom',
            'rendez_vous', 'note', 'commentaire', 'ponctualite', 'ecoute',
            'explication', 'recommande', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class PharmacieSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Pharmacie - Mise à jour"""
    user_nom = serializers.CharField(source='user.nom', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Pharmacie
        fields = [
            'id', 'nom', 'adresse', 'ville', 'pays', 'telephone', 'email',
            'latitude', 'longitude', 'logo', 'horaires_ouverture', 'description',
            'user', 'user_nom', 'user_email', 'actif',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SessionUtilisateurSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle SessionUtilisateur"""
    user_nom = serializers.CharField(source='user.nom', read_only=True)
    est_active = serializers.ReadOnlyField()
    duree_session = serializers.SerializerMethodField()
    
    class Meta:
        model = SessionUtilisateur
        fields = [
            'id', 'user', 'user_nom', 'session_key', 'ip_address', 
            'user_agent', 'device_info', 'location', 'date_creation',
            'derniere_activite', 'active', 'est_active', 'duree_session'
        ]
        read_only_fields = ['id', 'date_creation', 'derniere_activite']
    
    def get_duree_session(self, obj):
        """Calcule la durée de la session"""
        from datetime import datetime
        duree = obj.derniere_activite - obj.date_creation
        heures = int(duree.total_seconds() // 3600)
        minutes = int((duree.total_seconds() % 3600) // 60)
        if heures > 0:
            return f"{heures}h {minutes}min"
        return f"{minutes}min"


class HistoriqueConnexionSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle HistoriqueConnexion"""
    user_nom = serializers.CharField(source='user.nom', read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    
    class Meta:
        model = HistoriqueConnexion
        fields = [
            'id', 'user', 'user_nom', 'statut', 'statut_display',
            'ip_address', 'user_agent', 'device_info', 'location',
            'date_tentative', 'details'
        ]
        read_only_fields = ['id', 'date_tentative']


class LigneVenteSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle LigneVente"""
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)
    produit_unite = serializers.CharField(source='produit.unite', read_only=True)
    
    class Meta:
        model = LigneVente
        fields = [
            'id', 'vente', 'produit', 'produit_nom', 'produit_unite',
            'stock_produit', 'quantite', 'prix_unitaire', 'prix_total',
            'remise_pourcentage', 'remise_montant', 'created_at'
        ]
        read_only_fields = ['id', 'prix_total', 'remise_montant', 'created_at']


class VentePharmacieSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle VentePharmacie"""
    pharmacie_nom = serializers.CharField(source='pharmacie.nom', read_only=True)
    vendeur_nom = serializers.CharField(source='vendeur.nom', read_only=True)
    annulee_par_nom = serializers.CharField(source='annulee_par.nom', read_only=True)
    mode_paiement_display = serializers.CharField(source='get_mode_paiement_display', read_only=True)
    lignes = LigneVenteSerializer(many=True, read_only=True)
    
    class Meta:
        model = VentePharmacie
        fields = [
            'id', 'numero_vente', 'pharmacie', 'pharmacie_nom',
            'nom_client', 'telephone_client', 'montant_total',
            'montant_paye', 'montant_rendu', 'mode_paiement',
            'mode_paiement_display', 'reference_paiement',
            'prescription_image', 'notes', 'vendeur', 'vendeur_nom',
            'annulee', 'motif_annulation', 'date_annulation', 'annulee_par', 'annulee_par_nom',
            'date_vente', 'lignes', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'numero_vente', 'montant_rendu', 'date_vente',
            'annulee', 'motif_annulation', 'date_annulation', 'annulee_par',
            'created_at', 'updated_at'
        ]


class VentePharmacieCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer une vente avec ses lignes"""
    lignes = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        help_text="Liste des lignes de vente avec produit_id, quantite, prix_unitaire, remise_pourcentage"
    )
    
    class Meta:
        model = VentePharmacie
        fields = [
            'pharmacie', 'nom_client', 'telephone_client',
            'montant_paye', 'mode_paiement', 'reference_paiement',
            'prescription_image', 'notes', 'lignes'
        ]
    
    def validate_lignes(self, value):
        """Valider les lignes de vente"""
        if not value:
            raise serializers.ValidationError("Au moins une ligne de vente est requise.")
        
        for ligne in value:
            if 'produit_id' not in ligne:
                raise serializers.ValidationError("produit_id est requis pour chaque ligne.")
            if 'quantite' not in ligne or ligne['quantite'] <= 0:
                raise serializers.ValidationError("quantite doit être supérieure à 0.")
            if 'prix_unitaire' not in ligne or ligne['prix_unitaire'] <= 0:
                raise serializers.ValidationError("prix_unitaire doit être supérieur à 0.")
        
        return value
    
    def create(self, validated_data):
        from django.db import transaction
        
        lignes_data = validated_data.pop('lignes')
        
        with transaction.atomic():
            # Créer la vente (le vendeur sera ajouté par perform_create dans le ViewSet)
            vente = VentePharmacie.objects.create(**validated_data)
            
            from decimal import Decimal
            montant_total = Decimal('0')
            
            # Créer les lignes de vente
            for ligne_data in lignes_data:
                produit_id = ligne_data['produit_id']
                quantite = ligne_data['quantite']
                prix_unitaire = ligne_data['prix_unitaire']
                remise_pourcentage = ligne_data.get('remise_pourcentage', 0)
                
                # Vérifier que le produit existe
                try:
                    produit = Produit.objects.get(id=produit_id)
                except Produit.DoesNotExist:
                    raise serializers.ValidationError(f"Produit avec ID {produit_id} non trouvé.")
                
                # Trouver le stock correspondant
                try:
                    stock_produit = StockProduit.objects.get(
                        pharmacie=vente.pharmacie,
                        produit=produit
                    )
                except StockProduit.DoesNotExist:
                    raise serializers.ValidationError(f"Stock non trouvé pour le produit {produit.nom}.")
                
                # Vérifier la disponibilité
                if stock_produit.quantite < quantite:
                    raise serializers.ValidationError(
                        f"Stock insuffisant pour {produit.nom}. "
                        f"Disponible: {stock_produit.quantite}, Demandé: {quantite}"
                    )
                
                # Créer la ligne de vente
                ligne_vente = LigneVente.objects.create(
                    vente=vente,
                    produit=produit,
                    stock_produit=stock_produit,
                    quantite=quantite,
                    prix_unitaire=prix_unitaire,
                    remise_pourcentage=remise_pourcentage
                )
                
                # Utiliser Decimal pour les calculs
                from decimal import Decimal
                montant_total += Decimal(str(ligne_vente.prix_total))
                
                # Décrémenter le stock
                stock_produit.quantite -= quantite
                stock_produit.save()
            
            # Mettre à jour le montant total de la vente
            vente.montant_total = montant_total
            vente.save()
            
            return vente

# Serializers pour EmployePharmacie
class EmployePharmacieSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle EmployePharmacie"""
    user_nom = serializers.CharField(source='user.nom', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    pharmacie_nom = serializers.CharField(source='pharmacie.nom', read_only=True)
    
    class Meta:
        model = EmployePharmacie
        fields = [
            'id', 'user', 'user_nom', 'user_email', 'pharmacie', 'pharmacie_nom',
            'poste', 'date_embauche', 'salaire', 'peut_vendre', 'peut_gerer_stock',
            'peut_voir_commandes', 'peut_traiter_commandes', 'peut_annuler_vente',
            'peut_enregistrer_facture', 'actif', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class EmployePharmacieCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer un employé avec son utilisateur"""
    # Champs pour créer l'utilisateur
    nom = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    
    class Meta:
        model = EmployePharmacie
        fields = [
            'nom', 'email', 'password', 'pharmacie', 'poste', 'date_embauche',
            'salaire', 'peut_vendre', 'peut_gerer_stock', 'peut_voir_commandes',
            'peut_traiter_commandes', 'peut_annuler_vente', 'peut_enregistrer_facture', 'notes'
        ]
    
    def validate_email(self, value):
        """Vérifier que l'email n'existe pas déjà"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Un utilisateur avec cet email existe déjà.")
        return value
    
    def create(self, validated_data):
        """Créer l'utilisateur et l'employé"""
        # Extraire les données utilisateur
        nom = validated_data.pop('nom')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        
        # Créer l'utilisateur
        user = User.objects.create_user(
            nom=nom,
            email=email,
            password=password,
            role='employe_pharmacie',
            actif=True
        )
        
        # Créer l'employé
        employe = EmployePharmacie.objects.create(
            user=user,
            **validated_data
        )
        
        return employe


class EmployePharmacieUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour mettre à jour un employé"""
    user_nom = serializers.CharField(source='user.nom', required=False)
    user_email = serializers.CharField(source='user.email', required=False)
    
    class Meta:
        model = EmployePharmacie
        fields = [
            'user_nom', 'user_email', 'poste', 'date_embauche', 'salaire',
            'peut_vendre', 'peut_gerer_stock', 'peut_voir_commandes',
            'peut_traiter_commandes', 'peut_annuler_vente', 'peut_enregistrer_facture',
            'actif', 'notes'
        ]
    
    def validate_user_email(self, value):
        """Vérifier que l'email n'existe pas déjà (sauf pour l'utilisateur actuel)"""
        if User.objects.filter(email=value).exclude(id=self.instance.user.id).exists():
            raise serializers.ValidationError("Un utilisateur avec cet email existe déjà.")
        return value
    
    def update(self, instance, validated_data):
        """Mettre à jour l'employé et son utilisateur"""
        # Extraire les données utilisateur
        user_data = {}
        if 'user' in validated_data:
            user_data = validated_data.pop('user')
        
        # Mettre à jour l'utilisateur si nécessaire
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()
        
        # Mettre à jour l'employé
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance


# Serializers pour Registre
class RegistreSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Registre"""
    patient_nom_complet = serializers.SerializerMethodField()
    specialiste_nom = serializers.CharField(source='specialiste.user.nom', read_only=True)
    hopital_nom = serializers.CharField(source='hopital.nom', read_only=True)
    specialite_nom = serializers.CharField(source='specialiste.specialite.nom', read_only=True)
    
    class Meta:
        model = Registre
        fields = [
            'id', 'nom', 'prenom', 'sexe', 'age', 'residence', 'ethnie', 'profession',
            'numero_cni', 'numero_cne', 'telephone', 'email',
            'consultation_nc', 'consultation_ac', 'consultation_refere_asc',
            'poids_kg', 'taille_cm', 'poids_taille', 'taille_age', 'imc',
            'motif_symptomes', 'examen_labo_type', 'diagnostic',
            'patient', 'patient_nom_complet', 'specialiste', 'specialiste_nom',
            'hopital', 'hopital_nom', 'specialite_nom',
            'date_creation', 'date_modification', 'actif'
        ]
        read_only_fields = ['id', 'patient_nom_complet', 'specialiste_nom', 'hopital_nom', 
                           'specialite_nom', 'date_creation', 'date_modification', 
                           'poids_taille', 'taille_age', 'imc']
    
    def get_patient_nom_complet(self, obj):
        """Retourner le nom complet du patient lié s'il existe"""
        if obj.patient:
            return f"{obj.patient.nom} {obj.patient.prenom}"
        return None


class RegistreCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer un registre"""
    
    class Meta:
        model = Registre
        fields = [
            'nom', 'prenom', 'sexe', 'age', 'residence', 'ethnie', 'profession',
            'numero_cni', 'numero_cne', 'telephone', 'email',
            'consultation_nc', 'consultation_ac', 'consultation_refere_asc',
            'poids_kg', 'taille_cm', 'motif_symptomes', 'examen_labo_type', 'diagnostic'
        ]
    
    def validate(self, data):
        """Validation des données du registre"""
        # Nettoyer les champs CNI/CNE (supprimer les chaînes vides)
        numero_cni = data.get('numero_cni', '').strip()
        numero_cne = data.get('numero_cne', '').strip()
        
        # Convertir les chaînes vides en None
        if not numero_cni:
            data['numero_cni'] = None
        if not numero_cne:
            data['numero_cne'] = None
        
        # Vérifier qu'au moins un numéro d'identité est fourni
        if not numero_cni and not numero_cne:
            raise serializers.ValidationError(
                "Au moins un numéro d'identité (CNI ou CNE) est requis."
            )
        
        # Vérifier que l'âge est cohérent
        if data.get('age') and (data['age'] < 0 or data['age'] > 150):
            raise serializers.ValidationError("L'âge doit être entre 0 et 150 ans.")
        
        # Vérifier les mesures physiques
        if data.get('poids_kg') and data['poids_kg'] <= 0:
            raise serializers.ValidationError("Le poids doit être positif.")
        
        if data.get('taille_cm') and data['taille_cm'] <= 0:
            raise serializers.ValidationError("La taille doit être positive.")
        
        return data


class RegistreUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour mettre à jour un registre"""
    
    class Meta:
        model = Registre
        fields = [
            'nom', 'prenom', 'sexe', 'age', 'residence', 'ethnie', 'profession',
            'numero_cni', 'numero_cne', 'telephone', 'email',
            'consultation_nc', 'consultation_ac', 'consultation_refere_asc',
            'poids_kg', 'taille_cm', 'motif_symptomes', 'examen_labo_type', 'diagnostic',
            'actif'
        ]
    
    def validate(self, data):
        """Validation des données du registre"""
        # Vérifier que l'âge est cohérent
        if data.get('age') and (data['age'] < 0 or data['age'] > 150):
            raise serializers.ValidationError("L'âge doit être entre 0 et 150 ans.")
        
        # Vérifier les mesures physiques
        if data.get('poids_kg') and data['poids_kg'] <= 0:
            raise serializers.ValidationError("Le poids doit être positif.")
        
        if data.get('taille_cm') and data['taille_cm'] <= 0:
            raise serializers.ValidationError("La taille doit être positive.")
        
        return data


class RegistreListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des registres"""
    patient_nom_complet = serializers.SerializerMethodField()
    specialiste_nom = serializers.CharField(source='specialiste.user.nom', read_only=True)
    hopital_nom = serializers.CharField(source='hopital.nom', read_only=True)
    
    class Meta:
        model = Registre
        fields = [
            'id', 'nom', 'prenom', 'sexe', 'age', 'residence',
            'motif_symptomes', 'diagnostic', 'examen_labo_type',
            'patient_nom_complet', 'specialiste_nom', 'hopital_nom',
            'date_creation', 'actif'
        ]
    
    def get_patient_nom_complet(self, obj):
        """Retourner le nom complet du patient lié s'il existe"""
        if obj.patient:
            return f"{obj.patient.nom} {obj.patient.prenom}"
        return None

# Serializers pour Ordonnance et LigneOrdonnance
class LigneOrdonnanceSerializer(serializers.ModelSerializer):
    """Serializer pour les lignes d'ordonnance"""
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)
    nom_complet = serializers.ReadOnlyField()
    
    class Meta:
        model = LigneOrdonnance
        fields = [
            'id', 'produit', 'produit_nom', 'nom_medicament', 'nom_complet',
            'dosage', 'quantite', 'unite', 'frequence', 'frequence_detail',
            'moment_prise', 'duree_traitement', 'instructions', 'quantite_totale',
            'ordre', 'created_at'
        ]
        read_only_fields = ['id', 'produit_nom', 'nom_complet', 'quantite_totale', 'created_at']


class LigneOrdonnanceCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer une ligne d'ordonnance"""
    
    class Meta:
        model = LigneOrdonnance
        fields = [
            'produit', 'nom_medicament', 'dosage', 'quantite', 'unite',
            'frequence', 'frequence_detail', 'moment_prise', 'duree_traitement',
            'instructions', 'ordre'
        ]
    
    def validate(self, data):
        """Validation des données de la ligne d'ordonnance"""
        # Vérifier qu'au moins un produit ou nom de médicament est fourni
        if not data.get('produit') and not data.get('nom_medicament'):
            raise serializers.ValidationError(
                "Un produit ou un nom de médicament est requis."
            )
        
        # Vérifier que la quantité est positive
        if data.get('quantite') and data['quantite'] <= 0:
            raise serializers.ValidationError("La quantité doit être positive.")
        
        # Vérifier que la durée de traitement est positive
        if data.get('duree_traitement') and data['duree_traitement'] <= 0:
            raise serializers.ValidationError("La durée de traitement doit être positive.")
        
        return data


class OrdonnanceSerializer(serializers.ModelSerializer):
    """Serializer pour les ordonnances"""
    lignes = LigneOrdonnanceSerializer(many=True, read_only=True)
    specialiste_nom = serializers.CharField(source='specialiste.user.nom', read_only=True)
    hopital_nom = serializers.CharField(source='hopital.nom', read_only=True)
    registre_patient_nom = serializers.SerializerMethodField()
    est_expiree = serializers.ReadOnlyField()
    peut_etre_delivree = serializers.ReadOnlyField()
    qr_code_url_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Ordonnance
        fields = [
            'id', 'numero_ordonnance', 'registre', 'specialiste', 'specialiste_nom',
            'hopital', 'hopital_nom', 'patient_nom', 'patient_prenom', 'patient_age',
            'patient_sexe', 'registre_patient_nom', 'diagnostic', 'observations',
            'recommandations', 'statut', 'date_prescription', 'date_validation',
            'date_delivrance', 'duree_validite_jours', 'date_expiration',
            'pharmacie_delivrance', 'lignes', 'est_expiree', 'peut_etre_delivree',
            'qr_code', 'qr_code_url', 'qr_code_url_display', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'numero_ordonnance', 'specialiste_nom', 'hopital_nom',
            'registre_patient_nom', 'est_expiree', 'peut_etre_delivree',
            'qr_code', 'qr_code_url', 'qr_code_url_display', 'created_at', 'updated_at'
        ]
    
    def get_registre_patient_nom(self, obj):
        """Retourner le nom du patient depuis le registre"""
        if obj.registre:
            return f"{obj.registre.nom} {obj.registre.prenom}"
        return None
    
    def get_qr_code_url_display(self, obj):
        """Récupère l'URL complète du QR code"""
        if obj.qr_code:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.qr_code.url)
            return obj.qr_code.url
        return None


class OrdonnanceCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer une ordonnance avec ses lignes"""
    lignes = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False,
        help_text="Liste des médicaments à prescrire"
    )
    
    class Meta:
        model = Ordonnance
        fields = [
            'registre', 'diagnostic', 'observations', 'recommandations',
            'duree_validite_jours', 'lignes'
        ]
    
    def validate_lignes(self, value):
        """Valider les lignes d'ordonnance"""
        if not value:
            return value
        
        for i, ligne in enumerate(value):
            # Vérifier les champs requis
            required_fields = ['dosage', 'quantite', 'unite', 'frequence', 'moment_prise', 'duree_traitement']
            for field in required_fields:
                if field not in ligne or not ligne[field]:
                    raise serializers.ValidationError(
                        f"Ligne {i+1}: Le champ '{field}' est requis."
                    )
            
            # Vérifier qu'au moins un produit ou nom de médicament est fourni
            if not ligne.get('produit') and not ligne.get('nom_medicament'):
                raise serializers.ValidationError(
                    f"Ligne {i+1}: Un produit ou un nom de médicament est requis."
                )
        
        return value
    
    def create(self, validated_data):
        """Créer une ordonnance avec ses lignes"""
        lignes_data = validated_data.pop('lignes', [])
        
        # Créer l'ordonnance
        ordonnance = Ordonnance.objects.create(**validated_data)
        
        # Créer les lignes d'ordonnance
        for i, ligne_data in enumerate(lignes_data):
            ligne_data['ordre'] = i + 1
            LigneOrdonnance.objects.create(ordonnance=ordonnance, **ligne_data)
        
        return ordonnance


class OrdonnanceUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour mettre à jour une ordonnance"""
    
    class Meta:
        model = Ordonnance
        fields = [
            'diagnostic', 'observations', 'recommandations', 'statut',
            'duree_validite_jours', 'date_validation', 'date_delivrance',
            'pharmacie_delivrance'
        ]
    
    def validate_statut(self, value):
        """Valider le changement de statut"""
        if self.instance and self.instance.statut == 'delivree' and value != 'delivree':
            raise serializers.ValidationError(
                "Une ordonnance délivrée ne peut pas changer de statut."
            )
        return value


class OrdonnanceListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des ordonnances"""
    specialiste_nom = serializers.CharField(source='specialiste.user.nom', read_only=True)
    hopital_nom = serializers.CharField(source='hopital.nom', read_only=True)
    nombre_medicaments = serializers.SerializerMethodField()
    est_expiree = serializers.ReadOnlyField()
    
    class Meta:
        model = Ordonnance
        fields = [
            'id', 'numero_ordonnance', 'patient_nom', 'patient_prenom',
            'specialiste_nom', 'hopital_nom', 'diagnostic', 'statut',
            'date_prescription', 'date_expiration', 'nombre_medicaments',
            'est_expiree'
        ]
    
    def get_nombre_medicaments(self, obj):
        """Retourner le nombre de médicaments prescrits"""
        return obj.lignes.count()


# Serializers pour DossierMedical
class DossierMedicalSerializer(serializers.ModelSerializer):
    """Serializer pour les dossiers médicaux"""
    specialiste_nom = serializers.CharField(source='specialiste.user.nom', read_only=True)
    hopital_nom = serializers.CharField(source='hopital.nom', read_only=True)
    registre_patient_nom = serializers.SerializerMethodField()
    
    class Meta:
        model = DossierMedical
        fields = [
            'id', 'numero_dossier', 'registre', 'registre_patient_nom',
            'specialiste', 'specialiste_nom', 'hopital', 'hopital_nom',
            'patient_nom', 'patient_prenom', 'patient_age', 'patient_sexe',
            'motif_consultation', 'histoire_maladie',
            'antecedents', 'antecedents_familiaux', 'gyneco_obstetricaux', 'chirurgicaux',
            'examen_general', 'examen_physique',
            'hypothese_diagnostic', 'diagnostic',
            'bilan_biologie', 'bilan_imagerie',
            'date_consultation', 'created_at', 'updated_at'
        ]
    
    def get_registre_patient_nom(self, obj):
        """Retourner le nom complet du patient depuis le registre"""
        if obj.registre:
            return f"{obj.registre.nom} {obj.registre.prenom}"
        return f"{obj.patient_nom} {obj.patient_prenom}"


class DossierMedicalCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer un dossier médical"""
    
    class Meta:
        model = DossierMedical
        fields = [
            'id', 'registre', 'motif_consultation', 'histoire_maladie',
            'antecedents', 'antecedents_familiaux', 'gyneco_obstetricaux', 'chirurgicaux',
            'examen_general', 'examen_physique',
            'hypothese_diagnostic', 'diagnostic',
            'bilan_biologie', 'bilan_imagerie'
        ]
        read_only_fields = ['id']
    
    def create(self, validated_data):
        """Créer un dossier médical"""
        # Récupérer l'utilisateur connecté
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            
            # Vérifier que l'utilisateur est un spécialiste
            if user.role == 'specialiste':
                try:
                    specialiste = Specialiste.objects.get(user=user)
                    validated_data['specialiste'] = specialiste
                    validated_data['hopital'] = specialiste.hopital
                except Specialiste.DoesNotExist:
                    raise serializers.ValidationError("Utilisateur spécialiste non trouvé.")
            else:
                raise serializers.ValidationError("Seuls les spécialistes peuvent créer des dossiers médicaux.")
        
        return DossierMedical.objects.create(**validated_data)


class DossierMedicalUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour mettre à jour un dossier médical"""
    
    class Meta:
        model = DossierMedical
        fields = [
            'id', 'motif_consultation', 'histoire_maladie',
            'antecedents', 'antecedents_familiaux', 'gyneco_obstetricaux', 'chirurgicaux',
            'examen_general', 'examen_physique',
            'hypothese_diagnostic', 'diagnostic',
            'bilan_biologie', 'bilan_imagerie'
        ]
        read_only_fields = ['id']


class DossierMedicalListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des dossiers médicaux"""
    specialiste_nom = serializers.CharField(source='specialiste.user.nom', read_only=True)
    hopital_nom = serializers.CharField(source='hopital.nom', read_only=True)
    registre_patient_nom = serializers.SerializerMethodField()
    
    class Meta:
        model = DossierMedical
        fields = [
            'id', 'numero_dossier', 'registre_patient_nom',
            'patient_nom', 'patient_prenom', 'patient_age',
            'specialiste_nom', 'hopital_nom',
            'motif_consultation', 'diagnostic',
            'date_consultation'
        ]
    
    def get_registre_patient_nom(self, obj):
        """Retourner le nom complet du patient depuis le registre"""
        if obj.registre:
            return f"{obj.registre.nom} {obj.registre.prenom}"
        return f"{obj.patient_nom} {obj.patient_prenom}"



# ============================================================================
# Serializers pour FichierDossierMedical
# ============================================================================

class FichierDossierMedicalSerializer(serializers.ModelSerializer):
    """Serializer pour les fichiers joints aux dossiers médicaux"""
    fichier_url = serializers.SerializerMethodField()
    type_fichier_display = serializers.CharField(source='get_type_fichier_display', read_only=True)
    taille_fichier_display = serializers.SerializerMethodField()
    
    class Meta:
        model = FichierDossierMedical
        fields = [
            'id', 'dossier_medical', 'type_fichier', 'type_fichier_display',
            'fichier', 'fichier_url', 'nom_fichier', 'description',
            'taille_fichier', 'taille_fichier_display', 'type_mime',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['fichier_url', 'taille_fichier', 'type_mime']
    
    def get_fichier_url(self, obj):
        """Retourner l'URL complète du fichier"""
        if obj.fichier:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.fichier.url)
            return obj.fichier.url
        return None
    
    def get_taille_fichier_display(self, obj):
        """Retourner la taille du fichier formatée"""
        if obj.taille_fichier:
            size = obj.taille_fichier
            for unit in ['o', 'Ko', 'Mo', 'Go']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} To"
        return None


class FichierDossierMedicalCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer un fichier joint"""
    
    class Meta:
        model = FichierDossierMedical
        fields = [
            'dossier_medical', 'type_fichier', 'fichier',
            'nom_fichier', 'description'
        ]
    
    def create(self, validated_data):
        """Créer un fichier joint"""
        fichier = validated_data.get('fichier')
        
        # Extraire les métadonnées du fichier
        if fichier:
            validated_data['taille_fichier'] = fichier.size
            validated_data['type_mime'] = fichier.content_type
            
            # Utiliser le nom original si non fourni
            if not validated_data.get('nom_fichier'):
                validated_data['nom_fichier'] = fichier.name
        
        return FichierDossierMedical.objects.create(**validated_data)


# Mettre à jour DossierMedicalSerializer pour inclure les fichiers
class DossierMedicalDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour les dossiers médicaux avec fichiers"""
    specialiste_nom = serializers.CharField(source='specialiste.user.nom', read_only=True)
    hopital_nom = serializers.CharField(source='hopital.nom', read_only=True)
    registre_patient_nom = serializers.SerializerMethodField()
    fichiers = FichierDossierMedicalSerializer(many=True, read_only=True)
    fichiers_par_type = serializers.SerializerMethodField()
    
    class Meta:
        model = DossierMedical
        fields = [
            'id', 'numero_dossier', 'registre', 'registre_patient_nom',
            'specialiste', 'specialiste_nom', 'hopital', 'hopital_nom',
            'patient_nom', 'patient_prenom', 'patient_age', 'patient_sexe',
            'motif_consultation', 'histoire_maladie',
            'antecedents', 'antecedents_familiaux', 'gyneco_obstetricaux', 'chirurgicaux',
            'examen_general', 'examen_physique',
            'hypothese_diagnostic', 'diagnostic',
            'bilan_biologie', 'bilan_imagerie',
            'date_consultation', 'created_at', 'updated_at',
            'fichiers', 'fichiers_par_type'
        ]
    
    def get_registre_patient_nom(self, obj):
        """Retourner le nom complet du patient depuis le registre"""
        if obj.registre:
            return f"{obj.registre.nom} {obj.registre.prenom}"
        return f"{obj.patient_nom} {obj.patient_prenom}"
    
    def get_fichiers_par_type(self, obj):
        """Grouper les fichiers par type"""
        fichiers_groupes = {}
        for fichier in obj.fichiers.all():
            type_fichier = fichier.type_fichier
            if type_fichier not in fichiers_groupes:
                fichiers_groupes[type_fichier] = []
            fichiers_groupes[type_fichier].append(
                FichierDossierMedicalSerializer(fichier, context=self.context).data
            )
        return fichiers_groupes


# ============================================================================
# Serializers pour les Factures Fournisseurs
# ============================================================================

class FournisseurSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Fournisseur"""
    
    class Meta:
        model = Fournisseur
        fields = [
            'id', 'nom', 'adresse', 'ville', 'pays', 'telephone', 'email',
            'numero_registre_commerce', 'numero_identification_fiscale',
            'delai_paiement_jours', 'remise_habituelle', 'actif', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class LigneFactureFournisseurSerializer(serializers.ModelSerializer):
    """Serializer pour les lignes de facture fournisseur"""
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)
    
    class Meta:
        model = LigneFactureFournisseur
        fields = [
            'id', 'facture', 'produit', 'produit_nom', 'nom_produit',
            'quantite', 'prix_unitaire_ht', 'taux_tva', 'remise_ligne',
            'montant_ht', 'montant_tva', 'montant_ttc',
            'numero_lot', 'date_peremption',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['montant_ht', 'montant_tva', 'montant_ttc', 'created_at', 'updated_at']


class LigneFactureFournisseurCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer une ligne de facture"""
    
    class Meta:
        model = LigneFactureFournisseur
        fields = [
            'produit', 'quantite', 'prix_unitaire_ht', 'taux_tva',
            'remise_ligne', 'numero_lot', 'date_peremption'
        ]


class FactureFournisseurSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle FactureFournisseur"""
    fournisseur_nom = serializers.CharField(source='fournisseur.nom', read_only=True)
    pharmacie_nom = serializers.CharField(source='pharmacie.nom', read_only=True)
    enregistre_par_nom = serializers.CharField(source='enregistre_par.nom', read_only=True)
    lignes = LigneFactureFournisseurSerializer(many=True, read_only=True)
    montant_restant = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    est_payee = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = FactureFournisseur
        fields = [
            'id', 'numero_facture', 'pharmacie', 'pharmacie_nom',
            'fournisseur', 'fournisseur_nom', 'enregistre_par', 'enregistre_par_nom',
            'date_facture', 'date_enregistrement', 'date_echeance',
            'montant_ht', 'montant_tva', 'montant_remise', 'montant_total',
            'mode_paiement', 'montant_paye', 'montant_restant', 'est_payee',
            'statut', 'stock_incremente', 'notes', 'fichier_facture',
            'lignes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['date_enregistrement', 'enregistre_par', 'stock_incremente', 'created_at', 'updated_at']


class FactureFournisseurCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer une facture fournisseur avec ses lignes"""
    lignes = LigneFactureFournisseurCreateSerializer(many=True, write_only=True)
    
    class Meta:
        model = FactureFournisseur
        fields = [
            'numero_facture', 'pharmacie', 'fournisseur', 'date_facture',
            'date_echeance', 'montant_ht', 'montant_tva', 'montant_remise',
            'montant_total', 'mode_paiement', 'montant_paye', 'notes',
            'fichier_facture', 'lignes'
        ]
    
    def validate_numero_facture(self, value):
        """Vérifier que le numéro de facture n'existe pas déjà"""
        if FactureFournisseur.objects.filter(numero_facture=value).exists():
            raise serializers.ValidationError("Une facture avec ce numéro existe déjà.")
        return value
    
    def validate_lignes(self, value):
        """Vérifier qu'il y a au moins une ligne"""
        if not value:
            raise serializers.ValidationError("La facture doit contenir au moins une ligne.")
        return value
    
    def create(self, validated_data):
        """Créer la facture et ses lignes"""
        lignes_data = validated_data.pop('lignes')
        
        # Créer la facture
        facture = FactureFournisseur.objects.create(**validated_data)
        
        # Créer les lignes
        for ligne_data in lignes_data:
            LigneFactureFournisseur.objects.create(
                facture=facture,
                **ligne_data
            )
        
        return facture


class FactureFournisseurValidationSerializer(serializers.Serializer):
    """Serializer pour valider une facture et incrémenter le stock"""
    valider = serializers.BooleanField(default=True)
    
    def validate(self, data):
        facture = self.context.get('facture')
        
        if facture.statut == 'validee':
            raise serializers.ValidationError("Cette facture est déjà validée.")
        
        if facture.statut == 'annulee':
            raise serializers.ValidationError("Cette facture est annulée.")
        
        return data
