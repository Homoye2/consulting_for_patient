from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Permission pour permettre la lecture à tous et l'écriture aux administrateurs"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == 'administrateur'


class IsAdminOrMedicalStaff(permissions.BasePermission):
    """Permission pour les administrateurs et le personnel médical"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        medical_roles = ['administrateur', 'medecin', 'sage_femme', 'infirmier']
        return request.user.role in medical_roles


class IsAdminOrPharmacist(permissions.BasePermission):
    """Permission pour les administrateurs et les pharmaciens"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return request.user.role in ['administrateur', 'pharmacien']


class IsAdminOrReception(permissions.BasePermission):
    """Permission pour les administrateurs et les agents d'enregistrement"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return request.user.role in ['administrateur', 'agent_enregistrement']


class CanManageUsers(permissions.BasePermission):
    """Permission pour gérer les utilisateurs (seulement administrateurs)"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role == 'administrateur' or request.user.is_superuser


class CanManageStock(permissions.BasePermission):
    """Permission pour gérer les stocks (administrateurs et pharmaciens)"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['administrateur', 'pharmacien']


class CanManageConsultations(permissions.BasePermission):
    """Permission pour gérer les consultations (personnel médical)"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        medical_roles = ['administrateur', 'medecin', 'sage_femme', 'infirmier']
        return request.user.role in medical_roles


class CanManageAppointments(permissions.BasePermission):
    """Permission pour gérer les rendez-vous (personnel médical et agents)"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        allowed_roles = ['administrateur', 'medecin', 'sage_femme', 'infirmier', 'agent_enregistrement']
        return request.user.role in allowed_roles


class IsPatientOrStaff(permissions.BasePermission):
    """Permission pour permettre aux patients d'accéder à leurs propres données"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Les admins et le personnel médical ont accès
        medical_roles = ['administrateur', 'medecin', 'sage_femme', 'infirmier', 'agent_enregistrement']
        if request.user.role in medical_roles:
            return True
        
        # Les patients peuvent accéder à leurs propres données
        # On vérifie si l'utilisateur a un profil patient
        if hasattr(request.user, 'patient_profile'):
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        # Les admins et le personnel médical ont accès
        medical_roles = ['administrateur', 'medecin', 'sage_femme', 'infirmier', 'agent_enregistrement']
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
        if request.user.role == 'administrateur':
            return True
        
        # Les patients peuvent accéder à leur propre profil
        if hasattr(request.user, 'patient_profile'):
            # Permettre GET, PUT, PATCH pour leur propre profil
            # GET pour la liste (filtrée) et pour le détail
            if request.method in ['GET', 'PUT', 'PATCH']:
                return True
        
        # Les autres rôles médicaux ont accès complet
        medical_roles = ['medecin', 'sage_femme', 'infirmier', 'agent_enregistrement']
        if request.user.role in medical_roles:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        # Les admins ont accès complet
        if request.user.role == 'administrateur':
            return True
        
        # Les patients peuvent modifier uniquement leur propre profil
        if hasattr(request.user, 'patient_profile'):
            patient = request.user.patient_profile
            return obj == patient
        
        return False