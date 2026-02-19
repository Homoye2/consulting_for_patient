#!/usr/bin/env python
"""
Script pour créer des notifications de test
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth import get_user_model
from pf.models import Notification, CommandePharmacie, Pharmacie
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def create_test_notifications():
    """Créer des notifications de test pour les pharmaciens et employés"""
    
    # Trouver les utilisateurs pharmaciens et employés
    pharmaciens = User.objects.filter(role='pharmacien', actif=True)
    employes = User.objects.filter(role='employe_pharmacie', actif=True)
    
    users_to_notify = list(pharmaciens) + list(employes)
    
    if not users_to_notify:
        print("Aucun utilisateur pharmacien ou employé trouvé")
        return
    
    # Supprimer les anciennes notifications de test
    Notification.objects.filter(titre__contains='[TEST]').delete()
    
    notifications_created = 0
    
    for user in users_to_notify:
        # Notification de commande confirmée
        Notification.objects.create(
            user=user,
            type_notification='commande_confirmee',
            titre='[TEST] Nouvelle commande confirmée',
            message=f'Une commande a été confirmée et nécessite votre attention. Veuillez préparer les produits demandés.',
            data={'test': True, 'priority': 'high'}
        )
        notifications_created += 1
        
        # Notification de stock faible
        Notification.objects.create(
            user=user,
            type_notification='stock_alerte',
            titre='[TEST] Alerte stock faible',
            message='Le stock de Paracétamol 500mg est en dessous du seuil d\'alerte (5 unités restantes). Veuillez réapprovisionner rapidement.',
            data={'test': True, 'produit': 'Paracétamol 500mg', 'stock_restant': 5}
        )
        notifications_created += 1
        
        # Notification de commande prête
        Notification.objects.create(
            user=user,
            type_notification='commande_prete',
            titre='[TEST] Commande prête pour récupération',
            message='La commande CMD123456 est prête et peut être récupérée par le patient.',
            lu=True,  # Déjà lue
            date_lecture=timezone.now() - timedelta(hours=2),
            data={'test': True, 'commande_numero': 'CMD123456'}
        )
        notifications_created += 1
        
        # Notification système
        Notification.objects.create(
            user=user,
            type_notification='autre',
            titre='[TEST] Mise à jour système',
            message='Le système a été mis à jour avec de nouvelles fonctionnalités. Consultez la documentation pour plus d\'informations.',
            data={'test': True, 'version': '2.1.0'}
        )
        notifications_created += 1
    
    print(f"✅ {notifications_created} notifications de test créées pour {len(users_to_notify)} utilisateurs")
    
    # Afficher un résumé
    total_notifications = Notification.objects.count()
    unread_notifications = Notification.objects.filter(lu=False).count()
    
    print(f"📊 Résumé:")
    print(f"   - Total notifications: {total_notifications}")
    print(f"   - Non lues: {unread_notifications}")
    print(f"   - Lues: {total_notifications - unread_notifications}")

if __name__ == '__main__':
    create_test_notifications()