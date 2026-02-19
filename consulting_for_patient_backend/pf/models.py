from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Manager personnalisé pour le modèle User"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'super_admin')
        extra_fields.setdefault('actif', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superuser doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superuser doit avoir is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Modèle utilisateur personnalisé avec rôles"""
    
    ROLE_CHOICES = [
        ('super_admin', 'Super Administrateur'),
        ('admin_hopital', 'Administrateur Hôpital'),
        ('specialiste', 'Spécialiste'),
        ('pharmacien', 'Pharmacien'),
        ('employe_pharmacie', 'Employé Pharmacie'),
        ('agent_enregistrement', 'Agent d\'enregistrement'),
        ('patient', 'Patient'),
        ('fournisseur', 'Fournisseur'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    actif = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
    
    def __str__(self):
        return f"{self.nom} ({self.email})"
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.is_superuser


class Patient(models.Model):
    """Modèle pour les patients"""
    
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    dob = models.DateField(verbose_name='Date de naissance')
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, unique=True, verbose_name='Email')
    adresse = models.TextField(blank=True, null=True)
    antecedents = models.TextField(blank=True, null=True, verbose_name='Antécédents')
    allergies = models.TextField(blank=True, null=True, verbose_name='Allergies')
    
    # Nouvelles informations
    ville_actuelle = models.CharField(max_length=100, blank=True, verbose_name='Ville actuelle')
    preferences_notification = models.JSONField(default=dict, blank=True, verbose_name='Préférences de notification')
    
    # Informations d'identité
    numero_cni = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name='Numéro CNI')
    numero_cne = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name='Numéro CNE')
    lieu_naissance = models.CharField(max_length=100, blank=True, null=True, verbose_name='Lieu de naissance')
    profession = models.CharField(max_length=100, blank=True, null=True, verbose_name='Profession')
    ethnie = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ethnie')
    
    user = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='patient_profile',
        verbose_name='Compte utilisateur'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'patients'
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        indexes = [
            models.Index(fields=['nom', 'prenom']),
            models.Index(fields=['telephone']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
    @property
    def age(self):
        """Calcule l'âge du patient"""
        today = timezone.now().date()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))


class Hopital(models.Model):
    """Modèle pour les hôpitaux"""
    
    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=200)
    code_hopital = models.CharField(max_length=50, unique=True)  # Ex: "CHAND001"
    adresse = models.TextField()
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100, default="Sénégal")
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    
    # Géolocalisation
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Configuration
    logo = models.ImageField(upload_to='hopitaux/logos/', null=True, blank=True)
    couleur_theme = models.CharField(max_length=7, default="#0066CC")  # Hex color
    description = models.TextField(blank=True)
    horaires_ouverture = models.JSONField(default=dict)  # {"lundi": "8h-17h", ...}
    
    # Administration
    admin_hopital = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='hopitaux_administres',
        limit_choices_to={'role': 'admin_hopital'}
    )
    
    # Statut
    actif = models.BooleanField(default=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hopitaux'
        ordering = ['nom']
        indexes = [
            models.Index(fields=['code_hopital']),
            models.Index(fields=['ville']),
            models.Index(fields=['actif']),
        ]
        verbose_name = 'Hôpital'
        verbose_name_plural = 'Hôpitaux'
    
    def __str__(self):
        return self.nom


class Specialite(models.Model):
    """Modèle pour les spécialités médicales"""
    
    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=200)  # Ex: "Cardiologie", "Pédiatrie"
    code = models.CharField(max_length=50, unique=True)  # Ex: "CARDIO", "PEDIATR"
    description = models.TextField(blank=True)
    icone = models.CharField(max_length=100, default="Stethoscope")
    
    actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'specialites'
        ordering = ['nom']
        verbose_name = 'Spécialité'
        verbose_name_plural = 'Spécialités'
    
    def __str__(self):
        return self.nom


class Specialiste(models.Model):
    """Modèle pour les spécialistes"""
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='specialiste_profile'
    )
    hopital = models.ForeignKey(
        Hopital, 
        on_delete=models.CASCADE, 
        related_name='specialistes'
    )
    specialite = models.ForeignKey(
        Specialite, 
        on_delete=models.PROTECT, 
        related_name='specialistes'
    )
    
    # Informations professionnelles
    numero_ordre = models.CharField(max_length=100, unique=True)  # Numéro d'ordre médical
    titre = models.CharField(max_length=100)  # Dr, Pr, etc.
    annees_experience = models.IntegerField(default=0)
    bio = models.TextField(blank=True)
    
    # Tarifs et consultations
    tarif_consultation = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duree_consultation = models.IntegerField(default=30)  # en minutes
    
    # Photo
    photo = models.ImageField(upload_to='specialistes/photos/', null=True, blank=True)
    
    # Disponibilité
    accepte_nouveaux_patients = models.BooleanField(default=True)
    consultation_en_ligne = models.BooleanField(default=False)
    
    # Statistiques
    note_moyenne = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    nombre_avis = models.IntegerField(default=0)
    
    actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'specialistes'
        unique_together = ['user', 'hopital']
        indexes = [
            models.Index(fields=['hopital', 'specialite']),
            models.Index(fields=['actif']),
        ]
        verbose_name = 'Spécialiste'
        verbose_name_plural = 'Spécialistes'
    
    def __str__(self):
        return f"{self.titre} {self.user.nom} - {self.specialite.nom}"


class DisponibiliteSpecialiste(models.Model):
    """Modèle pour les disponibilités des spécialistes"""
    
    JOURS_SEMAINE = [
        ('lundi', 'Lundi'),
        ('mardi', 'Mardi'),
        ('mercredi', 'Mercredi'),
        ('jeudi', 'Jeudi'),
        ('vendredi', 'Vendredi'),
        ('samedi', 'Samedi'),
        ('dimanche', 'Dimanche'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    specialiste = models.ForeignKey(
        Specialiste, 
        on_delete=models.CASCADE, 
        related_name='disponibilites'
    )
    jour_semaine = models.CharField(max_length=20, choices=JOURS_SEMAINE)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    
    # Exceptions (congés, absences)
    date_debut_exception = models.DateField(null=True, blank=True)
    date_fin_exception = models.DateField(null=True, blank=True)
    motif_exception = models.TextField(blank=True)
    
    actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'disponibilites_specialistes'
        unique_together = ['specialiste', 'jour_semaine', 'heure_debut']
        ordering = ['jour_semaine', 'heure_debut']
        verbose_name = 'Disponibilité Spécialiste'
        verbose_name_plural = 'Disponibilités Spécialistes'
    
    def __str__(self):
        return f"{self.specialiste.user.nom} - {self.jour_semaine} {self.heure_debut}-{self.heure_fin}"


class RendezVous(models.Model):
    """Modèle pour les rendez-vous"""
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('refuse', 'Refusé'),
        ('annule', 'Annulé'),
        ('termine', 'Terminé'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='rendez_vous')
    specialiste = models.ForeignKey(
        'Specialiste', 
        on_delete=models.CASCADE, 
        related_name='rendez_vous',
        null=True,
        blank=True
    )
    hopital = models.ForeignKey(
        'Hopital', 
        on_delete=models.CASCADE, 
        related_name='rendez_vous',
        null=True,
        blank=True
    )
    datetime = models.DateTimeField(verbose_name='Date et heure')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    motif = models.TextField(blank=True, verbose_name='Motif de consultation')
    
    # Gestion acceptation/refus
    confirme_par_specialiste = models.BooleanField(default=False)
    date_confirmation = models.DateTimeField(null=True, blank=True)
    date_refus = models.DateTimeField(null=True, blank=True)
    motif_refus = models.TextField(blank=True)
    
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'rendez_vous'
        verbose_name = 'Rendez-vous'
        verbose_name_plural = 'Rendez-vous'
        indexes = [
            models.Index(fields=['datetime']),
            models.Index(fields=['statut']),
            models.Index(fields=['patient', 'datetime']),
            models.Index(fields=['specialiste', 'datetime']),
            models.Index(fields=['hopital']),
        ]
        ordering = ['-datetime']
    
    def __str__(self):
        return f"RDV {self.patient} - {self.specialiste.user.nom} - {self.datetime.strftime('%d/%m/%Y %H:%M')}"


class ConsultationPF(models.Model):
    """Modèle pour les consultations de planification familiale"""
    
    id = models.BigAutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    specialiste = models.ForeignKey(
        'Specialiste', 
        on_delete=models.CASCADE, 
        related_name='consultations',
        null=True,
        blank=True
    )
    hopital = models.ForeignKey(
        'Hopital', 
        on_delete=models.CASCADE, 
        related_name='consultations',
        null=True,
        blank=True
    )
    rendez_vous = models.ForeignKey(
        'RendezVous',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consultations'
    )
    date = models.DateTimeField(default=timezone.now)
    anamnese = models.TextField(blank=True, null=True, verbose_name='Anamnèse')
    examen = models.TextField(blank=True, null=True, verbose_name='Examen clinique')
    methode_posee = models.BooleanField(default=False, verbose_name='Méthode posée')
    effets_secondaires = models.TextField(blank=True, null=True, verbose_name='Effets secondaires')
    notes = models.TextField(blank=True, null=True)
    observation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'consultations_pf'
        verbose_name = 'Consultation PF'
        verbose_name_plural = 'Consultations PF'
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['patient', 'date']),
            models.Index(fields=['specialiste', 'date']),
            models.Index(fields=['hopital']),
        ]
        ordering = ['-date']
    
    def __str__(self):
        return f"Consultation {self.patient} - {self.specialiste.user.nom} - {self.date.strftime('%d/%m/%Y')}"


class LandingPageContent(models.Model):
    """Modèle pour le contenu de la page d'accueil"""
    
    # Header
    logo_text = models.CharField(max_length=200, default="Hôpital Abass Ndao", verbose_name="Texte du logo")
    
    # Hero Section
    hero_title = models.CharField(max_length=200, default="Bienvenue à l'Hôpital Abass Ndao", verbose_name="Titre principal")
    hero_description = models.TextField(default="Votre partenaire de confiance pour la santé et le bien-être.", verbose_name="Description hero")
    hero_button_primary = models.CharField(max_length=100, default="Accéder à l'application", verbose_name="Bouton principal")
    hero_button_secondary = models.CharField(max_length=100, default="En savoir plus", verbose_name="Bouton secondaire")
    
    # About Section
    about_title = models.CharField(max_length=200, default="À propos de l'Hôpital Abass Ndao", verbose_name="Titre section à propos")
    about_description_1 = models.TextField(verbose_name="Description 1")
    about_description_2 = models.TextField(verbose_name="Description 2")
    about_stat_1_value = models.CharField(max_length=50, default="15+", verbose_name="Statistique 1 - Valeur")
    about_stat_1_label = models.CharField(max_length=100, default="Années d'expérience", verbose_name="Statistique 1 - Label")
    about_stat_2_value = models.CharField(max_length=50, default="50+", verbose_name="Statistique 2 - Valeur")
    about_stat_2_label = models.CharField(max_length=100, default="Professionnels", verbose_name="Statistique 2 - Label")
    
    # Services Section
    services_title = models.CharField(max_length=200, default="Nos Services", verbose_name="Titre section services")
    services_subtitle = models.TextField(default="Nous offrons une gamme complète de services médicaux", verbose_name="Sous-titre services")
    
    # Values Section
    values_title = models.CharField(max_length=200, default="Pourquoi nous choisir ?", verbose_name="Titre section valeurs")
    values_subtitle = models.TextField(default="Des valeurs qui font la différence dans nos soins", verbose_name="Sous-titre valeurs")
    
    # Footer
    footer_about_text = models.TextField(default="Votre partenaire de confiance pour la santé et le bien-être de la communauté.", verbose_name="Texte footer à propos")
    footer_address = models.CharField(max_length=200, default="Abass Ndao, Dakar, Sénégal", verbose_name="Adresse")
    footer_phone = models.CharField(max_length=50, default="+221 33 XXX XX XX", verbose_name="Téléphone")
    footer_email = models.EmailField(default="contact@abassndao.sn", verbose_name="Email")
    footer_facebook = models.URLField(blank=True, null=True, verbose_name="Facebook")
    footer_twitter = models.URLField(blank=True, null=True, verbose_name="Twitter")
    footer_instagram = models.URLField(blank=True, null=True, verbose_name="Instagram")
    footer_linkedin = models.URLField(blank=True, null=True, verbose_name="LinkedIn")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'landing_page_content'
        verbose_name = 'Contenu de la page d\'accueil'
        verbose_name_plural = 'Contenu de la page d\'accueil'
    
    def __str__(self):
        return "Contenu de la page d'accueil"
    
    @classmethod
    def get_content(cls):
        """Récupère ou crée le contenu de la landing page"""
        content, created = cls.objects.get_or_create(pk=1)
        return content


class Service(models.Model):
    """Modèle pour les services affichés sur la landing page"""
    
    landing_page = models.ForeignKey(LandingPageContent, on_delete=models.CASCADE, related_name='services')
    titre = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    contenu_detail = models.TextField(blank=True, null=True, verbose_name="Contenu détaillé - Comment fonctionne le service")
    icone = models.CharField(max_length=100, default="Heart", verbose_name="Nom de l'icône Lucide")
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    
    class Meta:
        db_table = 'services'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['ordre']
    
    def __str__(self):
        return self.titre


class Value(models.Model):
    """Modèle pour les valeurs affichées sur la landing page"""
    
    landing_page = models.ForeignKey(LandingPageContent, on_delete=models.CASCADE, related_name='values')
    titre = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    icone = models.CharField(max_length=100, default="Shield", verbose_name="Nom de l'icône Lucide")
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    
    class Meta:
        db_table = 'values'
        verbose_name = 'Valeur'
        verbose_name_plural = 'Valeurs'
        ordering = ['ordre']
    
    def __str__(self):
        return self.titre


class Produit(models.Model):
    """Modèle pour les produits pharmaceutiques"""
    
    CATEGORIES = [
        ('medicament', 'Médicament'),
        ('contraceptif', 'Contraceptif'),
        ('supplement', 'Supplément'),
        ('materiel_medical', 'Matériel Médical'),
        ('hygiene', 'Hygiène'),
        ('autre', 'Autre'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=200)
    code_barre = models.CharField(max_length=100, unique=True, null=True, blank=True)
    categorie = models.CharField(max_length=50, choices=CATEGORIES)
    
    # Description
    description = models.TextField(blank=True)
    composition = models.TextField(blank=True)
    posologie = models.TextField(blank=True)
    contre_indications = models.TextField(blank=True)
    
    # Informations commerciales
    fabricant = models.CharField(max_length=200, blank=True)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    unite = models.CharField(max_length=50, default="unité")  # unité, boîte, flacon, etc.
    
    # Réglementation
    prescription_requise = models.BooleanField(default=False)
    
    # Image
    image = models.ImageField(upload_to='produits/images/', null=True, blank=True)
    
    actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'produits'
        ordering = ['nom']
        indexes = [
            models.Index(fields=['categorie']),
            models.Index(fields=['code_barre']),
            models.Index(fields=['actif']),
        ]
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
    
    def __str__(self):
        return self.nom


class Pharmacie(models.Model):
    """Modèle pour les pharmacies"""
    
    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=200, verbose_name="Nom de la pharmacie")
    adresse = models.TextField(verbose_name="Adresse")
    ville = models.CharField(max_length=100, default="Dakar")
    pays = models.CharField(max_length=100, default="Sénégal")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    
    # Géolocalisation
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Configuration
    logo = models.ImageField(upload_to='pharmacies/logos/', null=True, blank=True)
    horaires_ouverture = models.JSONField(default=dict, blank=True)
    description = models.TextField(blank=True)
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='pharmacies',
        verbose_name="Pharmacien propriétaire",
        limit_choices_to={'role': 'pharmacien'}
    )
    actif = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pharmacies'
        verbose_name = 'Pharmacie'
        verbose_name_plural = 'Pharmacies'
        indexes = [
            models.Index(fields=['nom']),
            models.Index(fields=['user']),
            models.Index(fields=['actif']),
            models.Index(fields=['ville']),
        ]
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class EmployePharmacie(models.Model):
    """Modèle pour les employés des pharmacies"""
    
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='employe_pharmacie',
        verbose_name="Utilisateur",
        limit_choices_to={'role': 'employe_pharmacie'}
    )
    pharmacie = models.ForeignKey(
        Pharmacie,
        on_delete=models.CASCADE,
        related_name='employes',
        verbose_name="Pharmacie"
    )
    
    # Informations sur l'emploi
    poste = models.CharField(max_length=100, verbose_name="Poste", default="Employé")
    date_embauche = models.DateField(verbose_name="Date d'embauche", default=timezone.now)
    salaire = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name="Salaire"
    )
    
    # Permissions spécifiques
    peut_vendre = models.BooleanField(default=True, verbose_name="Peut effectuer des ventes")
    peut_gerer_stock = models.BooleanField(default=False, verbose_name="Peut gérer le stock")
    peut_voir_commandes = models.BooleanField(default=True, verbose_name="Peut voir les commandes")
    peut_traiter_commandes = models.BooleanField(default=False, verbose_name="Peut traiter les commandes")
    peut_annuler_vente = models.BooleanField(default=False, verbose_name="Peut annuler une vente")
    peut_enregistrer_facture = models.BooleanField(default=False, verbose_name="Peut enregistrer des factures fournisseurs")
    
    # Statut
    actif = models.BooleanField(default=True, verbose_name="Actif")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'employes_pharmacies'
        verbose_name = 'Employé Pharmacie'
        verbose_name_plural = 'Employés Pharmacies'
        unique_together = ['user', 'pharmacie']
        indexes = [
            models.Index(fields=['pharmacie']),
            models.Index(fields=['user']),
            models.Index(fields=['actif']),
        ]
        ordering = ['user__nom']
    
    def __str__(self):
        return f"{self.user.nom} - {self.pharmacie.nom}"
    
    @property
    def nom_complet(self):
        return self.user.nom
    
    @property
    def email(self):
        return self.user.email


class StockProduit(models.Model):
    """Modèle pour le stock des produits dans les pharmacies"""
    
    id = models.BigAutoField(primary_key=True)
    pharmacie = models.ForeignKey(Pharmacie, on_delete=models.CASCADE, related_name='stocks')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='stocks')
    
    quantite = models.IntegerField(default=0)
    seuil_alerte = models.IntegerField(default=10)
    
    # Lot et expiration
    numero_lot = models.CharField(max_length=100, blank=True)
    date_expiration = models.DateField(null=True, blank=True)
    
    # Prix spécifique à la pharmacie
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'stocks_produits'
        unique_together = ['pharmacie', 'produit', 'numero_lot']
        indexes = [
            models.Index(fields=['pharmacie', 'produit']),
            models.Index(fields=['date_expiration']),
        ]
        verbose_name = 'Stock Produit'
        verbose_name_plural = 'Stocks Produits'
    
    def __str__(self):
        return f"{self.produit.nom} - {self.pharmacie.nom}: {self.quantite}"
    
    @property
    def est_en_rupture(self):
        return self.quantite <= 0
    
    @property
    def est_sous_seuil(self):
        return 0 < self.quantite <= self.seuil_alerte
    
    @property
    def est_proche_expiration(self):
        if not self.date_expiration:
            return False
        from django.utils import timezone
        jours_restants = (self.date_expiration - timezone.now().date()).days
        return 0 < jours_restants <= 30


class CommandePharmacie(models.Model):
    """Modèle pour les commandes de produits en pharmacie"""
    
    STATUTS = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('preparee', 'Préparée'),
        ('prete', 'Prête à récupérer'),
        ('recuperee', 'Récupérée'),
        ('annulee', 'Annulée'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    numero_commande = models.CharField(max_length=50, unique=True)  # Auto-généré
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='commandes')
    pharmacie = models.ForeignKey(Pharmacie, on_delete=models.CASCADE, related_name='commandes')
    
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')
    
    # Montants
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Prescription si nécessaire (image uniquement)
    prescription_image = models.ImageField(upload_to='prescriptions/', null=True, blank=True)
    
    # Notes
    notes_patient = models.TextField(blank=True)
    notes_pharmacie = models.TextField(blank=True)
    
    # Dates
    date_commande = models.DateTimeField(auto_now_add=True)
    date_confirmation = models.DateTimeField(null=True, blank=True)
    date_preparation = models.DateTimeField(null=True, blank=True)
    date_prete = models.DateTimeField(null=True, blank=True)
    date_recuperation = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'commandes_pharmacies'
        ordering = ['-date_commande']
        indexes = [
            models.Index(fields=['numero_commande']),
            models.Index(fields=['patient', 'statut']),
            models.Index(fields=['pharmacie', 'statut']),
            models.Index(fields=['date_commande']),
        ]
        verbose_name = 'Commande Pharmacie'
        verbose_name_plural = 'Commandes Pharmacies'
    
    def __str__(self):
        return f"Commande {self.numero_commande} - {self.patient}"
    
    def save(self, *args, **kwargs):
        if not self.numero_commande:
            # Générer un numéro de commande unique
            import random
            import string
            self.numero_commande = f"CMD{''.join(random.choices(string.digits, k=8))}"
        super().save(*args, **kwargs)


class LigneCommande(models.Model):
    """Modèle pour les lignes de commande"""
    
    id = models.BigAutoField(primary_key=True)
    commande = models.ForeignKey(
        CommandePharmacie, 
        on_delete=models.CASCADE, 
        related_name='lignes'
    )
    produit = models.ForeignKey(
        Produit, 
        on_delete=models.PROTECT, 
        related_name='lignes_commandes'
    )
    
    quantite = models.IntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'lignes_commandes'
        unique_together = ['commande', 'produit']
        verbose_name = 'Ligne Commande'
        verbose_name_plural = 'Lignes Commandes'
    
    def save(self, *args, **kwargs):
        self.prix_total = self.quantite * self.prix_unitaire
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.produit.nom} x{self.quantite} - {self.commande.numero_commande}"


class Notification(models.Model):
    """Modèle pour les notifications"""
    
    TYPES = [
        ('rendez_vous_nouveau', 'Nouveau rendez-vous'),
        ('rendez_vous_confirme', 'Rendez-vous confirmé'),
        ('rendez_vous_refuse', 'Rendez-vous refusé'),
        ('rendez_vous_rappel', 'Rappel rendez-vous'),
        ('commande_confirmee', 'Commande confirmée'),
        ('commande_prete', 'Commande prête'),
        ('consultation_rapport', 'Rapport de consultation'),
        ('stock_alerte', 'Alerte stock'),
        ('autre', 'Autre'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type_notification = models.CharField(max_length=50, choices=TYPES)
    titre = models.CharField(max_length=200)
    message = models.TextField()
    
    # Liens optionnels
    rendez_vous = models.ForeignKey(
        'RendezVous', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='notifications'
    )
    commande = models.ForeignKey(
        CommandePharmacie, 
        on_delete=models.CASCADE,
        null=True, 
        blank=True, 
        related_name='notifications'
    )
    
    # Données JSON pour informations supplémentaires
    data = models.JSONField(default=dict, blank=True)
    
    # Statut
    lu = models.BooleanField(default=False)
    date_lecture = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'lu']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        return f"{self.titre} - {self.user.nom}"


class RapportConsultation(models.Model):
    """Modèle pour les rapports de consultation"""
    
    id = models.BigAutoField(primary_key=True)
    consultation = models.OneToOneField(
        ConsultationPF, 
        on_delete=models.CASCADE,
        related_name='rapport'
    )
    
    # Contenu du rapport
    diagnostic = models.TextField()
    traitement_prescrit = models.TextField()
    recommandations = models.TextField(blank=True)
    suivi_necessaire = models.BooleanField(default=False)
    date_prochain_rdv = models.DateField(null=True, blank=True)
    
    # Documents attachés
    documents = models.JSONField(default=list, blank=True)  # URLs des documents
    
    # Envoi au patient
    envoye_patient = models.BooleanField(default=False)
    date_envoi = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'rapports_consultations'
        verbose_name = 'Rapport Consultation'
        verbose_name_plural = 'Rapports Consultations'
    
    def __str__(self):
        return f"Rapport {self.consultation}"


class AvisSpecialiste(models.Model):
    """Modèle pour les avis sur les spécialistes"""
    
    id = models.BigAutoField(primary_key=True)
    specialiste = models.ForeignKey(
        Specialiste, 
        on_delete=models.CASCADE, 
        related_name='avis'
    )
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.CASCADE, 
        related_name='avis_donnes'
    )
    rendez_vous = models.OneToOneField(
        'RendezVous', 
        on_delete=models.CASCADE,
        related_name='avis'
    )
    
    note = models.IntegerField()  # 1-5 étoiles
    commentaire = models.TextField(blank=True)
    
    # Critères spécifiques
    ponctualite = models.IntegerField(null=True, blank=True)  # 1-5
    ecoute = models.IntegerField(null=True, blank=True)  # 1-5
    explication = models.IntegerField(null=True, blank=True)  # 1-5
    
    recommande = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'avis_specialistes'
        unique_together = ['specialiste', 'patient', 'rendez_vous']
        verbose_name = 'Avis Spécialiste'
        verbose_name_plural = 'Avis Spécialistes'
    
    def __str__(self):
        return f"Avis {self.specialiste.user.nom} - {self.note}/5"


class ContactMessage(models.Model):
    """Modèle pour les messages de contact des patients"""
    
    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=200, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    sujet = models.CharField(max_length=200, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='messages_contact',
        verbose_name="Patient"
    )
    lu = models.BooleanField(default=False, verbose_name="Lu")
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'contact_messages'
        verbose_name = 'Message de contact'
        verbose_name_plural = 'Messages de contact'
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Message de {self.nom} - {self.sujet}"


class SessionUtilisateur(models.Model):
    """Modèle pour tracker les sessions actives des utilisateurs"""
    
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sessions_actives',
        verbose_name="Utilisateur"
    )
    session_key = models.CharField(max_length=40, unique=True, verbose_name="Clé de session")
    ip_address = models.GenericIPAddressField(verbose_name="Adresse IP")
    user_agent = models.TextField(verbose_name="User Agent")
    device_info = models.CharField(max_length=200, blank=True, verbose_name="Info appareil")
    location = models.CharField(max_length=200, blank=True, verbose_name="Localisation")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    derniere_activite = models.DateTimeField(auto_now=True, verbose_name="Dernière activité")
    active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        db_table = 'sessions_utilisateurs'
        verbose_name = 'Session utilisateur'
        verbose_name_plural = 'Sessions utilisateurs'
        ordering = ['-derniere_activite']
        indexes = [
            models.Index(fields=['user', 'active']),
            models.Index(fields=['session_key']),
        ]
    
    def __str__(self):
        return f"Session {self.user.nom} - {self.ip_address}"
    
    @property
    def est_active(self):
        """Vérifie si la session est encore active (moins de 24h d'inactivité)"""
        from datetime import timedelta
        limite = timezone.now() - timedelta(hours=24)
        return self.active and self.derniere_activite > limite


class HistoriqueConnexion(models.Model):
    """Modèle pour l'historique des connexions des utilisateurs"""
    
    STATUT_CHOICES = [
        ('succes', 'Succès'),
        ('echec', 'Échec'),
        ('deconnexion', 'Déconnexion'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='historique_connexions',
        verbose_name="Utilisateur"
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        verbose_name="Statut"
    )
    ip_address = models.GenericIPAddressField(verbose_name="Adresse IP")
    user_agent = models.TextField(verbose_name="User Agent")
    device_info = models.CharField(max_length=200, blank=True, verbose_name="Info appareil")
    location = models.CharField(max_length=200, blank=True, verbose_name="Localisation")
    date_tentative = models.DateTimeField(auto_now_add=True, verbose_name="Date de tentative")
    details = models.TextField(blank=True, verbose_name="Détails")
    
    class Meta:
        db_table = 'historique_connexions'
        verbose_name = 'Historique de connexion'
        verbose_name_plural = 'Historiques de connexions'
        ordering = ['-date_tentative']
        indexes = [
            models.Index(fields=['user', 'date_tentative']),
            models.Index(fields=['statut']),
            models.Index(fields=['ip_address']),
        ]
    
    def __str__(self):
        return f"{self.user.nom} - {self.statut} - {self.date_tentative.strftime('%d/%m/%Y %H:%M')}"


class VentePharmacie(models.Model):
    """Modèle pour les ventes manuelles en pharmacie"""
    
    MODES_PAIEMENT = [
        ('especes', 'Espèces'),
        ('carte', 'Carte bancaire'),
        ('mobile', 'Paiement mobile'),
        ('cheque', 'Chèque'),
        ('credit', 'Crédit'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    numero_vente = models.CharField(max_length=50, unique=True)  # Auto-généré
    pharmacie = models.ForeignKey(Pharmacie, on_delete=models.CASCADE, related_name='ventes')
    
    # Client (optionnel pour vente anonyme)
    nom_client = models.CharField(max_length=200, blank=True, verbose_name="Nom du client")
    telephone_client = models.CharField(max_length=20, blank=True, verbose_name="Téléphone du client")
    
    # Montants
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_rendu = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Paiement
    mode_paiement = models.CharField(max_length=20, choices=MODES_PAIEMENT, default='especes')
    reference_paiement = models.CharField(max_length=100, blank=True, verbose_name="Référence de paiement")
    
    # Prescription si nécessaire
    prescription_image = models.ImageField(upload_to='ventes/prescriptions/', null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True, verbose_name="Notes de vente")
    
    # Vendeur
    vendeur = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name='ventes_effectuees',
        verbose_name="Vendeur"
    )
    
    # Annulation
    annulee = models.BooleanField(default=False, verbose_name="Vente annulée")
    motif_annulation = models.TextField(blank=True, verbose_name="Motif d'annulation")
    date_annulation = models.DateTimeField(null=True, blank=True, verbose_name="Date d'annulation")
    annulee_par = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='ventes_annulees',
        verbose_name="Annulée par"
    )
    
    # Dates
    date_vente = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ventes_pharmacies'
        ordering = ['-date_vente']
        indexes = [
            models.Index(fields=['numero_vente']),
            models.Index(fields=['pharmacie', 'date_vente']),
            models.Index(fields=['vendeur', 'date_vente']),
            models.Index(fields=['mode_paiement']),
        ]
        verbose_name = 'Vente Pharmacie'
        verbose_name_plural = 'Ventes Pharmacies'
    
    def __str__(self):
        return f"Vente {self.numero_vente} - {self.montant_total}€"
    
    def save(self, *args, **kwargs):
        if not self.numero_vente:
            # Générer un numéro de vente unique
            import random
            import string
            self.numero_vente = f"VTE{''.join(random.choices(string.digits, k=8))}"
        
        # Calculer le montant rendu - s'assurer que tous les types sont Decimal
        from decimal import Decimal
        montant_paye = Decimal(str(self.montant_paye))
        montant_total = Decimal(str(self.montant_total))
        self.montant_rendu = max(Decimal('0'), montant_paye - montant_total)
        
        super().save(*args, **kwargs)


class LigneVente(models.Model):
    """Modèle pour les lignes de vente"""
    
    id = models.BigAutoField(primary_key=True)
    vente = models.ForeignKey(
        VentePharmacie, 
        on_delete=models.CASCADE, 
        related_name='lignes'
    )
    produit = models.ForeignKey(
        Produit, 
        on_delete=models.PROTECT, 
        related_name='lignes_ventes'
    )
    stock_produit = models.ForeignKey(
        StockProduit,
        on_delete=models.PROTECT,
        related_name='lignes_ventes',
        verbose_name="Stock utilisé"
    )
    
    quantite = models.IntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Remise éventuelle
    remise_pourcentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    remise_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'lignes_ventes'
        unique_together = ['vente', 'produit']
        verbose_name = 'Ligne Vente'
        verbose_name_plural = 'Lignes Ventes'
    
    def save(self, *args, **kwargs):
        # Calculer la remise en montant si pourcentage donné - s'assurer que tous les types sont Decimal
        from decimal import Decimal
        
        quantite = Decimal(str(self.quantite))
        prix_unitaire = Decimal(str(self.prix_unitaire))
        remise_pourcentage = Decimal(str(self.remise_pourcentage))
        
        if remise_pourcentage > 0:
            self.remise_montant = (quantite * prix_unitaire * remise_pourcentage) / Decimal('100')
        
        # Calculer le prix total avec remise
        prix_brut = quantite * prix_unitaire
        self.prix_total = prix_brut - Decimal(str(self.remise_montant))
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.produit.nom} x{self.quantite} - {self.vente.numero_vente}"


class Registre(models.Model):
    """Modèle pour la gestion des registres hospitaliers"""
    
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    
    CONSULTATION_NC_CHOICES = [
        ('oui', 'Oui'),
        ('non', 'Non'),
    ]
    
    CONSULTATION_AC_CHOICES = [
        ('oui', 'Oui'),
        ('non', 'Non'),
    ]
    
    CONSULTATION_REFERE_ASC_CHOICES = [
        ('oui', 'Oui'),
        ('non', 'Non'),
    ]
    
    EXAMEN_LABO_TYPES = [
        ('negatif', 'Négatif'),
        ('positif', 'Positif'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    
    # Informations du patient
    nom = models.CharField(max_length=100, verbose_name='Nom du patient')
    prenom = models.CharField(max_length=100, verbose_name='Prénom du patient')
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, verbose_name='Sexe')
    age = models.IntegerField(verbose_name='Âge')
    residence = models.CharField(max_length=200, verbose_name='Résidence')
    ethnie = models.CharField(max_length=100, verbose_name='Ethnie')
    profession = models.CharField(max_length=100, verbose_name='Profession')
    
    # Informations d'identité pour liaison avec compte patient
    numero_cni = models.CharField(max_length=50, blank=True, null=True, verbose_name='Numéro CNI')
    numero_cne = models.CharField(max_length=50, blank=True, null=True, verbose_name='Numéro CNE')
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Téléphone')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    
    # Consultation
    consultation_nc = models.CharField(max_length=10, choices=CONSULTATION_NC_CHOICES, verbose_name='NC')
    consultation_ac = models.CharField(max_length=10, choices=CONSULTATION_AC_CHOICES, verbose_name='AC')
    consultation_refere_asc = models.CharField(max_length=10, choices=CONSULTATION_REFERE_ASC_CHOICES, verbose_name='REFERE ASC')
    
    # Mesures physiques
    poids_kg = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Poids (kg)')
    taille_cm = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Taille (cm)')
    poids_taille = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Poids/Taille')
    taille_age = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Taille/Âge')
    imc = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='IMC')
    
    # Motif et symptômes
    motif_symptomes = models.TextField(verbose_name='Motif ou symptômes')
    
    # Examen laboratoire
    examen_labo_type = models.CharField(max_length=20, choices=EXAMEN_LABO_TYPES, verbose_name='Type examen labo')
    
    # Diagnostic
    diagnostic = models.TextField(verbose_name='Diagnostic')
    
    # Liaison avec les modèles existants
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='registres',
        verbose_name='Patient lié'
    )
    specialiste = models.ForeignKey(
        Specialiste, 
        on_delete=models.CASCADE, 
        related_name='registres',
        verbose_name='Spécialiste'
    )
    hopital = models.ForeignKey(
        Hopital, 
        on_delete=models.CASCADE, 
        related_name='registres',
        verbose_name='Hôpital'
    )
    
    # Dates et statut
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    date_modification = models.DateTimeField(auto_now=True, verbose_name='Date de modification')
    actif = models.BooleanField(default=True, verbose_name='Actif')
    
    class Meta:
        db_table = 'registres'
        verbose_name = 'Registre'
        verbose_name_plural = 'Registres'
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['hopital', 'specialiste']),
            models.Index(fields=['patient']),
            models.Index(fields=['date_creation']),
            models.Index(fields=['numero_cni']),
            models.Index(fields=['numero_cne']),
            models.Index(fields=['actif']),
        ]
    
    def __str__(self):
        return f"Registre {self.nom} {self.prenom} - {self.date_creation.strftime('%d/%m/%Y')}"
    
    def save(self, *args, **kwargs):
        # Calculer automatiquement les ratios si les données sont disponibles
        if self.poids_kg and self.taille_cm:
            # Calculer l'IMC
            taille_m = float(self.taille_cm) / 100
            self.imc = float(self.poids_kg) / (taille_m * taille_m)
            
            # Calculer poids/taille (ratio simple)
            self.poids_taille = float(self.poids_kg) / float(self.taille_cm) * 100
        
        if self.taille_cm and self.age:
            # Calculer taille/âge (ratio simple)
            self.taille_age = float(self.taille_cm) / float(self.age)
        
        super().save(*args, **kwargs)
    
    def creer_ou_lier_patient(self):
        """Crée un nouveau patient ou lie à un patient existant basé sur CNI/CNE"""
        patient_existant = None
        
        # Chercher un patient existant par CNI ou CNE
        if self.numero_cni:
            try:
                patient_existant = Patient.objects.get(numero_cni=self.numero_cni)
            except Patient.DoesNotExist:
                pass
        
        if not patient_existant and self.numero_cne:
            try:
                patient_existant = Patient.objects.get(numero_cne=self.numero_cne)
            except Patient.DoesNotExist:
                pass
        
        if patient_existant:
            # Lier au patient existant
            self.patient = patient_existant
            self.save()
            return patient_existant, False  # False = pas créé, juste lié
        else:
            # Créer un nouveau patient
            from django.utils import timezone
            from datetime import date
            
            # Calculer la date de naissance approximative basée sur l'âge
            today = date.today()
            dob_approximative = date(today.year - self.age, today.month, today.day)
            
            nouveau_patient = Patient.objects.create(
                nom=self.nom,
                prenom=self.prenom,
                dob=dob_approximative,
                sexe=self.sexe,
                telephone=self.telephone,
                email=self.email,
                adresse=self.residence,
                numero_cni=self.numero_cni,
                numero_cne=self.numero_cne,
                profession=self.profession,
                ethnie=self.ethnie,
                ville_actuelle=self.residence
            )
            
            # Lier le registre au nouveau patient
            self.patient = nouveau_patient
            self.save()
            
            return nouveau_patient, True  # True = créé

class Ordonnance(models.Model):
    """Modèle pour les ordonnances médicales"""
    
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('validee', 'Validée'),
        ('delivree', 'Délivrée'),
        ('annulee', 'Annulée'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    numero_ordonnance = models.CharField(max_length=50, unique=True)  # Auto-généré
    
    # Liaison avec le registre
    registre = models.ForeignKey(
        'Registre',
        on_delete=models.CASCADE,
        related_name='ordonnances',
        verbose_name='Registre'
    )
    
    # Informations du prescripteur
    specialiste = models.ForeignKey(
        Specialiste,
        on_delete=models.CASCADE,
        related_name='ordonnances',
        verbose_name='Spécialiste prescripteur'
    )
    
    hopital = models.ForeignKey(
        Hopital,
        on_delete=models.CASCADE,
        related_name='ordonnances',
        verbose_name='Hôpital'
    )
    
    # Informations patient (dénormalisées pour l'historique)
    patient_nom = models.CharField(max_length=100, verbose_name='Nom du patient')
    patient_prenom = models.CharField(max_length=100, verbose_name='Prénom du patient')
    patient_age = models.IntegerField(verbose_name='Âge du patient')
    patient_sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')])
    
    # Diagnostic et observations
    diagnostic = models.TextField(verbose_name='Diagnostic')
    observations = models.TextField(blank=True, null=True, verbose_name='Observations')
    recommandations = models.TextField(blank=True, null=True, verbose_name='Recommandations')
    
    # Statut et dates
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')
    date_prescription = models.DateTimeField(auto_now_add=True, verbose_name='Date de prescription')
    date_validation = models.DateTimeField(null=True, blank=True, verbose_name='Date de validation')
    date_delivrance = models.DateTimeField(null=True, blank=True, verbose_name='Date de délivrance')
    
    # Validité
    duree_validite_jours = models.IntegerField(default=30, verbose_name='Durée de validité (jours)')
    date_expiration = models.DateField(null=True, blank=True, verbose_name='Date d\'expiration')
    
    # Informations de délivrance
    pharmacie_delivrance = models.ForeignKey(
        Pharmacie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ordonnances_delivrees',
        verbose_name='Pharmacie de délivrance'
    )
    
    # QR Code pour téléchargement PDF
    qr_code = models.ImageField(
        upload_to='ordonnances/qr_codes/',
        null=True,
        blank=True,
        verbose_name='QR Code'
    )
    qr_code_url = models.URLField(
        null=True,
        blank=True,
        verbose_name='URL du QR Code'
    )
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ordonnances'
        verbose_name = 'Ordonnance'
        verbose_name_plural = 'Ordonnances'
        ordering = ['-date_prescription']
        indexes = [
            models.Index(fields=['numero_ordonnance']),
            models.Index(fields=['registre']),
            models.Index(fields=['specialiste', 'date_prescription']),
            models.Index(fields=['statut']),
            models.Index(fields=['date_expiration']),
        ]
    
    def __str__(self):
        return f"Ordonnance {self.numero_ordonnance} - {self.patient_nom} {self.patient_prenom}"
    
    def save(self, *args, **kwargs):
        # Générer un numéro d'ordonnance unique
        if not self.numero_ordonnance:
            import random
            import string
            from datetime import datetime
            date_str = datetime.now().strftime('%Y%m%d')
            random_str = ''.join(random.choices(string.digits, k=4))
            self.numero_ordonnance = f"ORD{date_str}{random_str}"
        
        # Calculer la date d'expiration
        if not self.date_expiration and self.date_prescription:
            from datetime import timedelta
            self.date_expiration = (self.date_prescription + timedelta(days=self.duree_validite_jours)).date()
        
        # Remplir les informations patient depuis le registre
        if self.registre and not self.patient_nom:
            self.patient_nom = self.registre.nom
            self.patient_prenom = self.registre.prenom
            self.patient_age = self.registre.age
            self.patient_sexe = self.registre.sexe
        
        super().save(*args, **kwargs)
    
    @property
    def est_expiree(self):
        """Vérifie si l'ordonnance est expirée"""
        if not self.date_expiration:
            return False
        from django.utils import timezone
        return timezone.now().date() > self.date_expiration
    
    @property
    def peut_etre_delivree(self):
        """Vérifie si l'ordonnance peut être délivrée"""
        return self.statut == 'validee' and not self.est_expiree
    
    def generer_qr_code(self, request=None):
        """Génère le QR code pour télécharger le PDF de l'ordonnance"""
        import qrcode
        from io import BytesIO
        from django.core.files.base import ContentFile
        from django.urls import reverse
        
        if not self.pk:
            return None
        
        # URL pour télécharger le PDF
        if request:
            base_url = request.build_absolute_uri('/')
        else:
            from django.conf import settings
            base_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000/')
        
        pdf_url = f"{base_url}api/ordonnances/{self.pk}/pdf/"
        
        # Générer le QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=15,  # Increased from 10 to 15 for larger QR code
            border=4,
        )
        qr.add_data(pdf_url)
        qr.make(fit=True)
        
        # Créer l'image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Sauvegarder dans un buffer
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Sauvegarder le fichier
        filename = f"qr_ordonnance_{self.numero_ordonnance}.png"
        self.qr_code.save(
            filename,
            ContentFile(buffer.getvalue()),
            save=False
        )
        self.qr_code_url = pdf_url
        self.save(update_fields=['qr_code', 'qr_code_url'])
        
        return self.qr_code.url if self.qr_code else None


class LigneOrdonnance(models.Model):
    """Modèle pour les lignes d'ordonnance (médicaments prescrits)"""
    
    UNITE_CHOICES = [
        ('comprime', 'Comprimé(s)'),
        ('gelule', 'Gélule(s)'),
        ('ml', 'ml'),
        ('mg', 'mg'),
        ('g', 'g'),
        ('sachet', 'Sachet(s)'),
        ('ampoule', 'Ampoule(s)'),
        ('suppositoire', 'Suppositoire(s)'),
        ('application', 'Application(s)'),
        ('goutte', 'Goutte(s)'),
        ('autre', 'Autre'),
    ]
    
    FREQUENCE_CHOICES = [
        ('1_fois_jour', '1 fois par jour'),
        ('2_fois_jour', '2 fois par jour'),
        ('3_fois_jour', '3 fois par jour'),
        ('4_fois_jour', '4 fois par jour'),
        ('matin', 'Le matin'),
        ('midi', 'À midi'),
        ('soir', 'Le soir'),
        ('coucher', 'Au coucher'),
        ('si_besoin', 'Si besoin'),
        ('autre', 'Autre'),
    ]
    
    MOMENT_PRISE_CHOICES = [
        ('avant_repas', 'Avant les repas'),
        ('pendant_repas', 'Pendant les repas'),
        ('apres_repas', 'Après les repas'),
        ('jeun', 'À jeun'),
        ('coucher', 'Au coucher'),
        ('si_besoin', 'Si besoin'),
        ('autre', 'Autre'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    ordonnance = models.ForeignKey(
        Ordonnance,
        on_delete=models.CASCADE,
        related_name='lignes',
        verbose_name='Ordonnance'
    )
    
    # Médicament/Produit
    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
        related_name='lignes_ordonnances',
        verbose_name='Médicament/Produit',
        null=True,
        blank=True
    )
    
    # Si le produit n'existe pas dans la base, on peut saisir manuellement
    nom_medicament = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Nom du médicament (si non référencé)'
    )
    
    # Posologie
    dosage = models.CharField(max_length=100, verbose_name='Dosage')  # Ex: "500mg", "5ml"
    quantite = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Quantité')
    unite = models.CharField(max_length=20, choices=UNITE_CHOICES, verbose_name='Unité')
    
    # Fréquence et durée
    frequence = models.CharField(max_length=20, choices=FREQUENCE_CHOICES, verbose_name='Fréquence')
    frequence_detail = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Détail fréquence'
    )  # Pour "autre" ou précisions
    
    moment_prise = models.CharField(
        max_length=20,
        choices=MOMENT_PRISE_CHOICES,
        verbose_name='Moment de prise'
    )
    
    duree_traitement = models.IntegerField(verbose_name='Durée du traitement (jours)')
    
    # Instructions spéciales
    instructions = models.TextField(
        blank=True,
        verbose_name='Instructions spéciales'
    )
    
    # Quantité totale à délivrer (calculée)
    quantite_totale = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Quantité totale à délivrer'
    )
    
    # Ordre d'affichage
    ordre = models.IntegerField(default=0, verbose_name='Ordre')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'lignes_ordonnances'
        verbose_name = 'Ligne d\'ordonnance'
        verbose_name_plural = 'Lignes d\'ordonnances'
        ordering = ['ordre', 'id']
        indexes = [
            models.Index(fields=['ordonnance', 'ordre']),
        ]
    
    def __str__(self):
        nom = self.produit.nom if self.produit else self.nom_medicament
        return f"{nom} - {self.dosage} - {self.get_frequence_display()}"
    
    def save(self, *args, **kwargs):
        # Calculer la quantité totale approximative
        if self.quantite and self.duree_traitement:
            # Estimation basée sur la fréquence
            multiplicateur_freq = {
                '1_fois_jour': 1,
                '2_fois_jour': 2,
                '3_fois_jour': 3,
                '4_fois_jour': 4,
                'matin': 1,
                'midi': 1,
                'soir': 1,
                'coucher': 1,
                'si_besoin': 1,
                'autre': 1,
            }
            
            freq_mult = multiplicateur_freq.get(self.frequence, 1)
            self.quantite_totale = self.quantite * freq_mult * self.duree_traitement
        
        super().save(*args, **kwargs)
    
    @property
    def nom_complet(self):
        """Retourne le nom complet du médicament"""
        return self.produit.nom if self.produit else self.nom_medicament


class DossierMedical(models.Model):
    """Modèle pour les dossiers médicaux"""
    
    id = models.BigAutoField(primary_key=True)
    numero_dossier = models.CharField(max_length=50, unique=True)  # Auto-généré
    
    # Liaison avec le registre
    registre = models.ForeignKey(
        'Registre',
        on_delete=models.CASCADE,
        related_name='dossiers_medicaux',
        verbose_name='Registre'
    )
    
    # Informations du médecin
    specialiste = models.ForeignKey(
        Specialiste,
        on_delete=models.CASCADE,
        related_name='dossiers_medicaux',
        verbose_name='Spécialiste'
    )
    
    hopital = models.ForeignKey(
        Hopital,
        on_delete=models.CASCADE,
        related_name='dossiers_medicaux',
        verbose_name='Hôpital'
    )
    
    # Informations patient (dénormalisées pour l'historique)
    patient_nom = models.CharField(max_length=100, verbose_name='Nom du patient')
    patient_prenom = models.CharField(max_length=100, verbose_name='Prénom du patient')
    patient_age = models.IntegerField(verbose_name='Âge du patient')
    patient_sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')])
    
    # Consultation
    motif_consultation = models.TextField(verbose_name='Motif de consultation')
    histoire_maladie = models.TextField(verbose_name='Histoire de la maladie')
    
    # Antécédents
    antecedents = models.TextField(blank=True, null=True, verbose_name='Antécédents')
    antecedents_familiaux = models.TextField(blank=True, null=True, verbose_name='Antécédents familiaux')
    gyneco_obstetricaux = models.TextField(blank=True, null=True, verbose_name='Gynéco-Obstétricaux')
    chirurgicaux = models.TextField(blank=True, null=True, verbose_name='Chirurgicaux')
    
    # Examens
    examen_general = models.TextField(blank=True, null=True, verbose_name='Examen général')
    examen_physique = models.TextField(blank=True, null=True, verbose_name='Examen physique')
    
    # Diagnostic
    hypothese_diagnostic = models.TextField(blank=True, null=True, verbose_name='Hypothèse diagnostic')
    diagnostic = models.TextField(blank=True, null=True, verbose_name='Diagnostic')
    
    # Bilan
    bilan_biologie = models.TextField(blank=True, null=True, verbose_name='Bilan - Biologie')
    bilan_imagerie = models.TextField(blank=True, null=True, verbose_name='Bilan - Imagerie')
    
    # Métadonnées
    date_consultation = models.DateTimeField(auto_now_add=True, verbose_name='Date de consultation')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'dossiers_medicaux'
        verbose_name = 'Dossier médical'
        verbose_name_plural = 'Dossiers médicaux'
        ordering = ['-date_consultation']
        indexes = [
            models.Index(fields=['numero_dossier']),
            models.Index(fields=['registre']),
            models.Index(fields=['specialiste', 'date_consultation']),
        ]
    
    def __str__(self):
        return f"Dossier {self.numero_dossier} - {self.patient_nom} {self.patient_prenom}"
    
    def save(self, *args, **kwargs):
        # Générer un numéro de dossier unique
        if not self.numero_dossier:
            import random
            import string
            from datetime import datetime
            date_str = datetime.now().strftime('%Y%m%d')
            random_str = ''.join(random.choices(string.digits, k=4))
            self.numero_dossier = f"DOS{date_str}{random_str}"
        
        # Remplir les informations patient depuis le registre
        if self.registre and not self.patient_nom:
            self.patient_nom = self.registre.nom
            self.patient_prenom = self.registre.prenom
            self.patient_age = self.registre.age
            self.patient_sexe = self.registre.sexe
        
        super().save(*args, **kwargs)


# ============================================================================
# SIGNALS - Gestion automatique des états
# ============================================================================

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=Pharmacie)
def pharmacie_status_changed(sender, instance, **kwargs):
    """
    Signal déclenché avant la sauvegarde d'une pharmacie.
    Si la pharmacie est désactivée, désactive automatiquement l'utilisateur associé et tous les employés.
    Si la pharmacie est activée, active automatiquement l'utilisateur associé et tous les employés.
    """
    if instance.pk:  # Si la pharmacie existe déjà (mise à jour)
        try:
            old_instance = Pharmacie.objects.get(pk=instance.pk)
            
            # Si le statut actif a changé
            if old_instance.actif != instance.actif:
                action = "activé" if instance.actif else "désactivé"
                
                # 1. Synchroniser le statut du pharmacien propriétaire
                if instance.user:
                    instance.user.actif = instance.actif
                    instance.user.is_active = instance.actif
                    instance.user.save()
                    print(f"✅ Pharmacien {instance.user.email} {action} automatiquement")
                
                # 2. Synchroniser le statut de tous les employés de la pharmacie
                employes = EmployePharmacie.objects.filter(pharmacie=instance)
                employes_count = 0
                for employe in employes:
                    employe.actif = instance.actif
                    employe.user.actif = instance.actif
                    employe.user.is_active = instance.actif
                    employe.user.save()
                    employe.save()
                    employes_count += 1
                
                if employes_count > 0:
                    print(f"✅ {employes_count} employé(s) {action}(s) automatiquement")
                
        except Pharmacie.DoesNotExist:
            pass

@receiver(pre_save, sender=Hopital)
def hopital_status_changed(sender, instance, **kwargs):
    """
    Signal déclenché avant la sauvegarde d'un hôpital.
    Si l'hôpital est désactivé, désactive automatiquement l'utilisateur associé.
    Si l'hôpital est activé, active automatiquement l'utilisateur associé.
    """
    if instance.pk:  # Si l'hôpital existe déjà (mise à jour)
        try:
            old_instance = Hopital.objects.get(pk=instance.pk)
            
            # Si le statut actif a changé
            if old_instance.actif != instance.actif:
                if instance.user:
                    # Synchroniser le statut de l'utilisateur avec celui de l'hôpital
                    instance.user.actif = instance.actif
                    instance.user.is_active = instance.actif
                    instance.user.save()
                    
                    action = "activé" if instance.actif else "désactivé"
                    print(f"✅ Utilisateur {instance.user.email} {action} automatiquement (hôpital {action})")
        except Hopital.DoesNotExist:
            pass


# ============================================================================
# FICHIERS JOINTS AUX DOSSIERS MÉDICAUX
# ============================================================================

class FichierDossierMedical(models.Model):
    """Modèle pour les fichiers joints aux dossiers médicaux"""
    
    TYPE_FICHIER_CHOICES = [
        ('gyneco_obstetricaux', 'Gynéco-Obstétricaux'),
        ('chirurgicaux', 'Chirurgicaux'),
        ('examen_general', 'Examen général'),
        ('examen_physique', 'Examen physique'),
        ('hypothese_diagnostic', 'Hypothèse diagnostic'),
        ('diagnostic', 'Diagnostic'),
        ('biologie', 'Biologie'),
        ('imagerie', 'Imagerie'),
        ('autre', 'Autre'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    
    # Liaison avec le dossier médical
    dossier_medical = models.ForeignKey(
        DossierMedical,
        on_delete=models.CASCADE,
        related_name='fichiers',
        verbose_name='Dossier médical'
    )
    
    # Type de fichier
    type_fichier = models.CharField(
        max_length=50,
        choices=TYPE_FICHIER_CHOICES,
        verbose_name='Type de fichier'
    )
    
    # Fichier
    fichier = models.FileField(
        upload_to='dossiers_medicaux/%Y/%m/%d/',
        verbose_name='Fichier'
    )
    
    # Nom original du fichier
    nom_fichier = models.CharField(
        max_length=255,
        verbose_name='Nom du fichier'
    )
    
    # Description optionnelle
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description'
    )
    
    # Métadonnées
    taille_fichier = models.IntegerField(
        verbose_name='Taille du fichier (octets)',
        null=True,
        blank=True
    )
    
    type_mime = models.CharField(
        max_length=100,
        verbose_name='Type MIME',
        blank=True,
        null=True
    )
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'fichiers_dossiers_medicaux'
        verbose_name = 'Fichier de dossier médical'
        verbose_name_plural = 'Fichiers de dossiers médicaux'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['dossier_medical', 'type_fichier']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.nom_fichier} ({self.get_type_fichier_display()})"
    
    def save(self, *args, **kwargs):
        # Extraire le nom du fichier si pas fourni
        if not self.nom_fichier and self.fichier:
            self.nom_fichier = self.fichier.name
        
        # Extraire la taille du fichier
        if self.fichier and not self.taille_fichier:
            self.taille_fichier = self.fichier.size
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Supprimer le fichier physique
        if self.fichier:
            self.fichier.delete(save=False)
        super().delete(*args, **kwargs)


# ============================================================================
# GESTION DES FACTURES FOURNISSEURS
# ============================================================================

class Fournisseur(models.Model):
    """Modèle pour les fournisseurs de produits pharmaceutiques"""
    
    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=200, verbose_name="Nom du fournisseur")
    adresse = models.TextField(verbose_name="Adresse")
    ville = models.CharField(max_length=100, verbose_name="Ville")
    pays = models.CharField(max_length=100, default="Sénégal", verbose_name="Pays")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    
    # Informations commerciales
    numero_registre_commerce = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="Numéro de registre de commerce"
    )
    numero_identification_fiscale = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="NIF"
    )
    
    # Conditions commerciales
    delai_paiement_jours = models.IntegerField(
        default=30, 
        verbose_name="Délai de paiement (jours)"
    )
    remise_habituelle = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0, 
        verbose_name="Remise habituelle (%)"
    )
    
    # Statut
    actif = models.BooleanField(default=True, verbose_name="Actif")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'fournisseurs'
        verbose_name = 'Fournisseur'
        verbose_name_plural = 'Fournisseurs'
        ordering = ['nom']
        indexes = [
            models.Index(fields=['nom']),
            models.Index(fields=['actif']),
        ]
    
    def __str__(self):
        return self.nom


class FactureFournisseur(models.Model):
    """Modèle pour les factures des fournisseurs"""
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente de validation'),
        ('validee', 'Validée'),
        ('annulee', 'Annulée'),
    ]
    
    MODE_PAIEMENT_CHOICES = [
        ('especes', 'Espèces'),
        ('cheque', 'Chèque'),
        ('virement', 'Virement bancaire'),
        ('mobile_money', 'Mobile Money'),
        ('credit', 'À crédit'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    numero_facture = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="Numéro de facture"
    )
    
    # Relations
    pharmacie = models.ForeignKey(
        Pharmacie,
        on_delete=models.CASCADE,
        related_name='factures_fournisseurs',
        verbose_name="Pharmacie"
    )
    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.PROTECT,
        related_name='factures',
        verbose_name="Fournisseur"
    )
    enregistre_par = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='factures_enregistrees',
        verbose_name="Enregistré par"
    )
    
    # Dates
    date_facture = models.DateField(verbose_name="Date de la facture")
    date_enregistrement = models.DateTimeField(auto_now_add=True, verbose_name="Date d'enregistrement")
    date_echeance = models.DateField(verbose_name="Date d'échéance")
    
    # Montants
    montant_ht = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Montant HT"
    )
    montant_tva = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0, 
        verbose_name="Montant TVA"
    )
    montant_remise = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0, 
        verbose_name="Montant remise"
    )
    montant_total = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Montant total TTC"
    )
    
    # Paiement
    mode_paiement = models.CharField(
        max_length=20, 
        choices=MODE_PAIEMENT_CHOICES, 
        default='credit',
        verbose_name="Mode de paiement"
    )
    montant_paye = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0, 
        verbose_name="Montant payé"
    )
    
    # Statut
    statut = models.CharField(
        max_length=20, 
        choices=STATUT_CHOICES, 
        default='en_attente',
        verbose_name="Statut"
    )
    stock_incremente = models.BooleanField(
        default=False, 
        verbose_name="Stock incrémenté"
    )
    
    # Informations complémentaires
    notes = models.TextField(blank=True, verbose_name="Notes")
    fichier_facture = models.FileField(
        upload_to='factures_fournisseurs/', 
        blank=True, 
        null=True,
        verbose_name="Fichier de la facture"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'factures_fournisseurs'
        verbose_name = 'Facture Fournisseur'
        verbose_name_plural = 'Factures Fournisseurs'
        ordering = ['-date_facture', '-created_at']
        indexes = [
            models.Index(fields=['pharmacie', 'statut']),
            models.Index(fields=['fournisseur']),
            models.Index(fields=['numero_facture']),
            models.Index(fields=['date_facture']),
            models.Index(fields=['statut']),
        ]
    
    def __str__(self):
        return f"Facture {self.numero_facture} - {self.fournisseur.nom}"
    
    @property
    def montant_restant(self):
        """Calcule le montant restant à payer"""
        return self.montant_total - self.montant_paye
    
    @property
    def est_payee(self):
        """Vérifie si la facture est entièrement payée"""
        return self.montant_paye >= self.montant_total
    
    def save(self, *args, **kwargs):
        # Calculer le montant total si non fourni
        if not self.montant_total:
            self.montant_total = (self.montant_ht + self.montant_tva) - self.montant_remise
        
        # Calculer la date d'échéance si non fournie
        if not self.date_echeance and self.fournisseur:
            from datetime import timedelta
            self.date_echeance = self.date_facture + timedelta(days=self.fournisseur.delai_paiement_jours)
        
        super().save(*args, **kwargs)


class LigneFactureFournisseur(models.Model):
    """Modèle pour les lignes de facture fournisseur"""
    
    id = models.BigAutoField(primary_key=True)
    facture = models.ForeignKey(
        FactureFournisseur,
        on_delete=models.CASCADE,
        related_name='lignes',
        verbose_name="Facture"
    )
    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
        related_name='lignes_factures_fournisseur',
        verbose_name="Produit"
    )
    
    # Informations produit (snapshot au moment de la facture)
    nom_produit = models.CharField(max_length=200, verbose_name="Nom du produit")
    
    # Quantités et prix
    quantite = models.IntegerField(verbose_name="Quantité")
    prix_unitaire_ht = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Prix unitaire HT"
    )
    taux_tva = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0, 
        verbose_name="Taux TVA (%)"
    )
    remise_ligne = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        verbose_name="Remise ligne"
    )
    
    # Montants calculés
    montant_ht = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Montant HT"
    )
    montant_tva = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Montant TVA"
    )
    montant_ttc = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Montant TTC"
    )
    
    # Informations complémentaires
    numero_lot = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Numéro de lot"
    )
    date_peremption = models.DateField(
        blank=True, 
        null=True, 
        verbose_name="Date de péremption"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lignes_factures_fournisseurs'
        verbose_name = 'Ligne de Facture Fournisseur'
        verbose_name_plural = 'Lignes de Factures Fournisseurs'
        ordering = ['id']
        indexes = [
            models.Index(fields=['facture']),
            models.Index(fields=['produit']),
        ]
    
    def __str__(self):
        return f"{self.nom_produit} x {self.quantite}"
    
    def save(self, *args, **kwargs):
        # Sauvegarder le nom du produit
        if not self.nom_produit and self.produit:
            self.nom_produit = self.produit.nom
        
        # Calculer les montants
        self.montant_ht = (self.quantite * self.prix_unitaire_ht) - self.remise_ligne
        self.montant_tva = self.montant_ht * (self.taux_tva / 100)
        self.montant_ttc = self.montant_ht + self.montant_tva
        
        super().save(*args, **kwargs)
