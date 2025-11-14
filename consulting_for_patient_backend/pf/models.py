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
        extra_fields.setdefault('role', 'administrateur')
        extra_fields.setdefault('actif', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superuser doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superuser doit avoir is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Modèle utilisateur personnalisé avec rôles"""
    
    ROLE_CHOICES = [
        ('administrateur', 'Administrateur'),
        ('medecin', 'Médecin'),
        ('sage_femme', 'Sage-femme'),
        ('infirmier', 'Infirmier(ère)'),
        ('pharmacien', 'Pharmacien'),
        ('agent_enregistrement', 'Agent d\'enregistrement'),
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
    adresse = models.TextField(blank=True, null=True)
    antecedents = models.TextField(blank=True, null=True, verbose_name='Antécédents')
    allergies = models.TextField(blank=True, null=True, verbose_name='Allergies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'patients'
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        indexes = [
            models.Index(fields=['nom', 'prenom']),
            models.Index(fields=['telephone']),
        ]
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
    @property
    def age(self):
        """Calcule l'âge du patient"""
        today = timezone.now().date()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))


class MethodeContraceptive(models.Model):
    """Modèle pour les méthodes contraceptives"""
    
    CATEGORIE_CHOICES = [
        ('hormonale', 'Hormonale'),
        ('barriere', 'Barrière'),
        ('iud', 'Dispositif intra-utérin (DIU)'),
        ('permanent', 'Permanent'),
        ('naturelle', 'Naturelle'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=200)
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'methodes_contraceptives'
        verbose_name = 'Méthode contraceptive'
        verbose_name_plural = 'Méthodes contraceptives'
        indexes = [
            models.Index(fields=['categorie']),
        ]
    
    def __str__(self):
        return self.nom


class RendezVous(models.Model):
    """Modèle pour les rendez-vous"""
    
    STATUT_CHOICES = [
        ('planifie', 'Planifié'),
        ('confirme', 'Confirmé'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
        ('absent', 'Absent'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='rendez_vous')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rendez_vous', verbose_name='Professionnel')
    datetime = models.DateTimeField(verbose_name='Date et heure')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='planifie')
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
            models.Index(fields=['user', 'datetime']),
        ]
        ordering = ['-datetime']
    
    def __str__(self):
        return f"RDV {self.patient} - {self.datetime.strftime('%d/%m/%Y %H:%M')}"


class ConsultationPF(models.Model):
    """Modèle pour les consultations de planification familiale"""
    
    id = models.BigAutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultations', verbose_name='Professionnel')
    date = models.DateTimeField(default=timezone.now)
    anamnese = models.TextField(blank=True, null=True, verbose_name='Anamnèse')
    examen = models.TextField(blank=True, null=True, verbose_name='Examen clinique')
    methode_proposee = models.ForeignKey(
        MethodeContraceptive, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='consultations_proposees',
        verbose_name='Méthode proposée'
    )
    methode_prescite = models.ForeignKey(
        MethodeContraceptive, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='consultations_prescrites',
        verbose_name='Méthode prescrite'
    )
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
            models.Index(fields=['user', 'date']),
        ]
        ordering = ['-date']
    
    def __str__(self):
        return f"Consultation {self.patient} - {self.date.strftime('%d/%m/%Y')}"


class StockItem(models.Model):
    """Modèle pour la gestion des stocks de méthodes contraceptives"""
    
    id = models.BigAutoField(primary_key=True)
    methode = models.ForeignKey(MethodeContraceptive, on_delete=models.CASCADE, related_name='stock_items')
    quantite = models.IntegerField(default=0, verbose_name='Quantité disponible')
    seuil = models.IntegerField(default=10, verbose_name='Seuil d\'alerte')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'stock_items'
        verbose_name = 'Article de stock'
        verbose_name_plural = 'Articles de stock'
        unique_together = ['methode']
        indexes = [
            models.Index(fields=['quantite']),
        ]
    
    def __str__(self):
        return f"{self.methode.nom} - Stock: {self.quantite}"
    
    @property
    def est_en_rupture(self):
        """Vérifie si le stock est en rupture"""
        return self.quantite <= 0
    
    @property
    def est_sous_seuil(self):
        """Vérifie si le stock est sous le seuil d'alerte"""
        return self.quantite <= self.seuil


class Prescription(models.Model):
    """Modèle pour les prescriptions de méthodes contraceptives"""
    
    id = models.BigAutoField(primary_key=True)
    consultation = models.ForeignKey(ConsultationPF, on_delete=models.CASCADE, related_name='prescriptions')
    methode = models.ForeignKey(MethodeContraceptive, on_delete=models.CASCADE, related_name='prescriptions')
    dosage = models.CharField(max_length=200, blank=True, null=True)
    remarque = models.TextField(blank=True, null=True)
    date_prescription = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'prescriptions'
        verbose_name = 'Prescription'
        verbose_name_plural = 'Prescriptions'
        indexes = [
            models.Index(fields=['consultation']),
            models.Index(fields=['date_prescription']),
        ]
    
    def __str__(self):
        return f"Prescription {self.methode.nom} - {self.consultation.patient}"


class MouvementStock(models.Model):
    """Modèle pour tracer les mouvements de stock (entrées/sorties)"""
    
    TYPE_MOUVEMENT_CHOICES = [
        ('entree', 'Entrée'),
        ('sortie', 'Sortie'),
        ('inventaire', 'Inventaire'),
        ('perte', 'Perte'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    stock_item = models.ForeignKey(StockItem, on_delete=models.CASCADE, related_name='mouvements')
    type_mouvement = models.CharField(max_length=20, choices=TYPE_MOUVEMENT_CHOICES)
    quantite = models.IntegerField()
    motif = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='mouvements_stock')
    date_mouvement = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'mouvements_stock'
        verbose_name = 'Mouvement de stock'
        verbose_name_plural = 'Mouvements de stock'
        indexes = [
            models.Index(fields=['date_mouvement']),
            models.Index(fields=['type_mouvement']),
        ]
        ordering = ['-date_mouvement']
    
    def __str__(self):
        return f"{self.type_mouvement} - {self.stock_item.methode.nom} - {self.quantite}"


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
