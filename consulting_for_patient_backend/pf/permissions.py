from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    """Permission pour le Super Administrateur"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'super_admin'


class IsAdminHopital(permissions.BasePermission):
    """Permission pour les Administrateurs d'Hôpital"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['super_admin', 'admin_hopital']
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'super_admin':
            return True
        if request.user.role == 'admin_hopital':
            # Vérifier que l'admin gère cet hôpital
            if hasattr(obj, 'hopital'):
                return obj.hopital.admin_hopital == request.user
            elif hasattr(obj, 'admin_hopital'):
                return obj.admin_hopital == request.user
        return False


class IsSpecialiste(permissions.BasePermission):
    """Permission pour les Spécialistes"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'specialiste'


class IsSpecialisteOfHopital(permissions.BasePermission):
    """Permission pour vérifier que le spécialiste appartient à l'hôpital"""
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'super_admin':
            return True
        if request.user.role == 'specialiste':
            try:
                specialiste = request.user.specialiste_profile
                if hasattr(obj, 'hopital'):
                    return obj.hopital == specialiste.hopital
                elif hasattr(obj, 'specialiste'):
                    return obj.specialiste.hopital == specialiste.hopital
                return obj == specialiste.hopital
            except:
                return False
        return False


class CanManagePharmacieCommandes(permissions.BasePermission):
    """Permission pour gérer les commandes de pharmacie"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['super_admin', 'pharmacien']
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'super_admin':
            return True
        if request.user.role == 'pharmacien':
            # Vérifier que le pharmacien gère cette pharmacie
            pharmacies = request.user.pharmacies.filter(actif=True)
            if hasattr(obj, 'pharmacie'):
                return obj.pharmacie in pharmacies
            return obj in pharmacies
        return False


class IsPatientOwner(permissions.BasePermission):
    """Permission pour que le patient accède à ses propres données"""
    
    def has_object_permission(self, request, view, obj):
        if request.user.role in ['super_admin', 'admin_hopital', 'specialiste']:
            return True
        if request.user.role == 'patient':
            try:
                if hasattr(obj, 'patient'):
                    return obj.patient == request.user.patient_profile
                return obj == request.user.patient_profile
            except:
                return False
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """Permission pour permettre la lecture à tous et l'écriture aux administrateurs"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role in ['super_admin', 'admin_hopital']


class IsAdminOrMedicalStaff(permissions.BasePermission):
    """Permission pour les administrateurs et le personnel médical"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        medical_roles = ['super_admin', 'admin_hopital', 'specialiste']
        return request.user.role in medical_roles


class IsAdminOrPharmacist(permissions.BasePermission):
    """Permission pour les administrateurs, super admins et les pharmaciens"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return request.user.role in ['super_admin', 'administrateur', 'pharmacien'] or request.user.is_superuser


class IsAdminOrReception(permissions.BasePermission):
    """Permission pour les administrateurs, super admins et les agents d'enregistrement"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return request.user.role in ['super_admin', 'administrateur', 'agent_enregistrement'] or request.user.is_superuser


class CanManageUsers(permissions.BasePermission):
    """Permission pour gérer les utilisateurs (seulement super admin)"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role == 'super_admin' or request.user.is_superuser


class CanManageStock(permissions.BasePermission):
    """Permission pour gérer les stocks (administrateurs, super admins et pharmaciens)"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['super_admin', 'administrateur', 'pharmacien'] or request.user.is_superuser


class CanManageConsultations(permissions.BasePermission):
    """Permission pour gérer les consultations (spécialistes)"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        medical_roles = ['super_admin', 'admin_hopital', 'specialiste']
        return request.user.role in medical_roles


class CanManageAppointments(permissions.BasePermission):
    """Permission pour gérer les rendez-vous (spécialistes et agents)"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        allowed_roles = ['super_admin', 'admin_hopital', 'specialiste', 'agent_enregistrement']
        return request.user.role in allowed_roles


class IsPatientOrStaff(permissions.BasePermission):
    """Permission pour permettre aux patients d'accéder à leurs propres données"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Les admins et le personnel médical ont accès
        medical_roles = ['super_admin', 'admin_hopital', 'specialiste', 'agent_enregistrement']
        if request.user.role in medical_roles:
            return True
        
        # Les patients peuvent accéder à leurs propres données
        # On vérifie si l'utilisateur a un profil patient
        if hasattr(request.user, 'patient_profile'):
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        # Les admins et le personnel médical ont accès
        medical_roles = ['super_admin', 'admin_hopital', 'specialiste', 'agent_enregistrement']
        if request.user.role in medical_roles:
            return True
        
        # Les patients peuvent accéder uniquement à leurs propres données
        if hasattr(request.user, 'patient_profile'):
            patient = request.user.patient_profile
            # Vérifier si l'objet appartient au patient
            if hasattr(obj, 'patient'):
                return obj.patient == patient
            elif hasattr(obj, 'id'):
                # Pour les objets Patient, vérifier directement
                return obj == patient
        
        return False


class IsPatientOrAdmin(permissions.BasePermission):
    """Permission pour permettre aux patients de modifier leur propre profil"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Les admins ont accès complet
        if request.user.role in ['super_admin', 'admin_hopital']:
            return True
        
        # Les patients peuvent accéder à leur propre profil
        if hasattr(request.user, 'patient_profile'):
            # Permettre GET, PUT, PATCH pour leur propre profil
            # GET pour la liste (filtrée) et pour le détail
            if request.method in ['GET', 'PUT', 'PATCH']:
                return True
        
        # Les autres rôles médicaux ont accès complet
        medical_roles = ['specialiste', 'agent_enregistrement']
        if request.user.role in medical_roles:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        # Les admins ont accès complet
        if request.user.role in ['super_admin', 'admin_hopital']:
            return True
        
        # Les patients peuvent modifier uniquement leur propre profil
        if hasattr(request.user, 'patient_profile'):
            patient = request.user.patient_profile
            return obj == patient
        
        return False