#!/usr/bin/env python
"""
Script pour créer des notifications de test pour l'utilisateur margot68@example.net
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth import get_user_model
from pf.models import Notification
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def create_notifications_for_margot():
    """Créer des notifications spécifiquement pour margot68@example.net"""
    
    # Trouver l'utilisateur margot68@example.net
    try:
        user = User.objects.get(email='margot68@example.net', role='patient', actif=True)
        print(f"✅ Utilisateur trouvé: {user.nom} ({user.email}) - ID: {user.id}")
    except User.DoesNotExist:
        print("❌ Utilisateur margot68@example.net non trouvé")
        return
    
    # Supprimer les anciennes notifications de test pour cet utilisateur
    old_notifications = Notification.objects.filter(
        user=user,
        titre__contains='[TEST]'
    )
    deleted_count = old_notifications.count()
    old_notifications.delete()
    print(f"🗑️ {deleted_count} anciennes notifications de test supprimées")
    
    # Créer de nouvelles notifications
    notifications_data = [
        {
            'type_notification': 'rendez_vous_confirme',
            'titre': '[TEST] Rendez-vous confirmé avec Dr. Martin',
            'message': 'Votre rendez-vous avec Dr. Martin le 15 février à 14h30 a été confirmé. Merci de vous présenter 15 minutes avant l\'heure.',
            'lu': False,
            'data': {'test': True, 'priority': 'high', 'doctor': 'Dr. Martin'}
        },
        {
            'type_notification': 'rendez_vous_rappel',
            'titre': '[TEST] Rappel: Rendez-vous demain',
            'message': 'N\'oubliez pas votre rendez-vous avec Dr. Sow demain à 10h00 au service de cardiologie.',
            'lu': False,
            'data': {'test': True, 'priority': 'medium', 'doctor': 'Dr. Sow'}
        },
        {
            'type_notification': 'commande_prete',
            'titre': '[TEST] Votre commande est prête',
            'message': 'Votre commande #CMD-2024-001 est prête à être récupérée à la Pharmacie du Centre. Horaires: 8h-18h.',
            'lu': False,
            'data': {'test': True, 'commande_numero': 'CMD-2024-001', 'pharmacie': 'Pharmacie du Centre'}
        },
        {
            'type_notification': 'consultation_rapport',
            'titre': '[TEST] Rapport de consultation disponible',
            'message': 'Le rapport de votre consultation du 28 janvier avec Dr. Diallo est maintenant disponible dans votre dossier médical.',
            'lu': True,
            'date_lecture': timezone.now() - timedelta(hours=2),
            'data': {'test': True, 'doctor': 'Dr. Diallo', 'date_consultation': '2024-01-28'}
        },
        {
            'type_notification': 'autre',
            'titre': '[TEST] Mise à jour importante',
            'message': 'Une nouvelle version de l\'application e-Sora est disponible avec des améliorations de sécurité et de nouvelles fonctionnalités.',
            'lu': True,
            'date_lecture': timezone.now() - timedelta(days=1),
            'data': {'test': True, 'version': '2.1.0', 'type': 'security_update'}
        }
    ]
    
    created_count = 0
    for notif_data in notifications_data:
        notification = Notification.objects.create(
            user=user,
            type_notification=notif_data['type_notification'],
            titre=notif_data['titre'],
            message=notif_data['message'],
            lu=notif_data['lu'],
            date_lecture=notif_data.get('date_lecture'),
            data=notif_data['data']
        )
        created_count += 1
        print(f"📝 Notification créée: {notification.titre} (ID: {notification.id})")
    
    print(f"\n✅ {created_count} nouvelles notifications créées pour {user.email}")
    
    # Vérifier le résultat
    total_notifications = Notification.objects.filter(user=user).count()
    unread_notifications = Notification.objects.filter(user=user, lu=False).count()
    
    print(f"\n📊 Résumé pour {user.email}:")
    print(f"   - Total notifications: {total_notifications}")
    print(f"   - Non lues: {unread_notifications}")
    print(f"   - Lues: {total_notifications - unread_notifications}")
    
    # Afficher les notifications non lues
    print(f"\n📬 Notifications non lues:")
    unread_notifs = Notification.objects.filter(user=user, lu=False).order_by('-created_at')
    for notif in unread_notifs:
        print(f"   - {notif.titre} ({notif.type_notification})")

if __name__ == '__main__':
    create_notifications_for_margot()