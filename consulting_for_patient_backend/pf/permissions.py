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

