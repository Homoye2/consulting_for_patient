#!/usr/bin/env python3
"""
Script pour générer un diagramme PNG à partir du fichier Mermaid
Utilise mermaid-cli si disponible, sinon génère un diagramme texte
"""

import subprocess
import sys
import os

def check_mermaid_cli():
    """Vérifie si mermaid-cli est installé"""
    try:
        result = subprocess.run(['mmdc', '--version'], 
                             capture_output=True, 
                             text=True, 
                             timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def generate_png_with_mermaid():
    """Génère le PNG avec mermaid-cli"""
    input_file = 'ARCHITECTURE_DIAGRAM.mmd'
    output_file = 'ARCHITECTURE_DIAGRAM.png'
    
    try:
        subprocess.run([
            'mmdc',
            '-i', input_file,
            '-o', output_file,
            '-w', '2400',
            '-H', '1800',
            '-b', 'white'
        ], check=True)
        print(f"✅ Diagramme généré avec succès: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la génération: {e}")
        return False
    except FileNotFoundError:
        print("❌ mermaid-cli (mmdc) n'est pas installé")
        return False

def generate_text_diagram():
    """Génère un diagramme texte alternatif"""
    print("\n" + "="*80)
    print("DIAGRAMME DE RELATIONS - ARCHITECTURE BACKEND")
    print("="*80)
    print("""
┌─────────────────────────────────────────────────────────────────────────┐
│                           MODÈLES PRINCIPAUX                             │
└─────────────────────────────────────────────────────────────────────────┘

User (Utilisateur)
├── OneToOne → Patient (profil patient)
├── ForeignKey → RendezVous (créateur)
├── ForeignKey → ConsultationPF (professionnel)
└── ForeignKey → MouvementStock (enregistreur)

Patient
├── OneToOne ← User (compte utilisateur)
├── ForeignKey → RendezVous (ses rendez-vous)
├── ForeignKey → ConsultationPF (ses consultations)
└── ForeignKey → ContactMessage (ses messages)

MethodeContraceptive
├── OneToOne → StockItem (stock associé)
├── ForeignKey → ConsultationPF (méthode proposée)
├── ForeignKey → ConsultationPF (méthode prescrite)
└── ForeignKey → Prescription (prescriptions)

ConsultationPF
├── ForeignKey ← Patient
├── ForeignKey ← User (professionnel)
├── ForeignKey ← MethodeContraceptive (proposée)
├── ForeignKey ← MethodeContraceptive (prescrite)
└── ForeignKey → Prescription

StockItem
├── OneToOne ← MethodeContraceptive
└── ForeignKey → MouvementStock

LandingPageContent
├── ForeignKey → Service (services affichés)
└── ForeignKey → Value (valeurs affichées)

┌─────────────────────────────────────────────────────────────────────────┐
│                         RELATIONS DÉTAILLÉES                             │
└─────────────────────────────────────────────────────────────────────────┘

1. User ↔ Patient (OneToOne)
   - Un utilisateur peut avoir un profil patient
   - Un patient peut avoir un compte utilisateur

2. User → RendezVous (ForeignKey)
   - Un utilisateur (professionnel) crée des rendez-vous
   - Plusieurs rendez-vous par utilisateur

3. Patient → RendezVous (ForeignKey)
   - Un patient a plusieurs rendez-vous
   - Relation obligatoire

4. Patient → ConsultationPF (ForeignKey)
   - Un patient a plusieurs consultations
   - Relation obligatoire

5. User → ConsultationPF (ForeignKey)
   - Un professionnel effectue plusieurs consultations
   - Relation obligatoire

6. MethodeContraceptive ↔ StockItem (OneToOne)
   - Chaque méthode a un stock unique
   - Relation 1:1

7. ConsultationPF → Prescription (ForeignKey)
   - Une consultation peut avoir plusieurs prescriptions
   - Relation obligatoire

8. StockItem → MouvementStock (ForeignKey)
   - Un stock a plusieurs mouvements
   - Historique des entrées/sorties

9. LandingPageContent → Service (ForeignKey)
   - La landing page a plusieurs services
   - Relation obligatoire

10. LandingPageContent → Value (ForeignKey)
    - La landing page a plusieurs valeurs
    - Relation obligatoire

┌─────────────────────────────────────────────────────────────────────────┐
│                         TABLES DE BASE DE DONNÉES                        │
└─────────────────────────────────────────────────────────────────────────┘

- users
- patients
- methodes_contraceptives
- rendez_vous
- consultations_pf
- stocks
- prescriptions
- mouvements_stock
- landing_page_content
- services
- values
- contact_messages

┌─────────────────────────────────────────────────────────────────────────┐
│                         INDEXES PRINCIPAUX                              │
└─────────────────────────────────────────────────────────────────────────┘

patients:
  - (nom, prenom)
  - telephone
  - email

rendez_vous:
  - datetime
  - statut
  - (patient, datetime)

consultations_pf:
  - date
  - (patient, date)
  - (user, date)

mouvements_stock:
  - date_mouvement
  - type_mouvement
""")
    print("\n" + "="*80)
    print("💡 Pour générer le PNG, installez mermaid-cli:")
    print("   npm install -g @mermaid-js/mermaid-cli")
    print("   Puis exécutez: mmdc -i ARCHITECTURE_DIAGRAM.mmd -o ARCHITECTURE_DIAGRAM.png")
    print("="*80 + "\n")

if __name__ == '__main__':
    print("🔍 Vérification de mermaid-cli...")
    
    if check_mermaid_cli():
        print("✅ mermaid-cli détecté, génération du PNG...")
        if generate_png_with_mermaid():
            sys.exit(0)
        else:
            print("⚠️  Échec de la génération PNG, affichage du diagramme texte...")
            generate_text_diagram()
    else:
        print("⚠️  mermaid-cli non disponible")
        generate_text_diagram()
        print("\n📝 Le fichier ARCHITECTURE_DIAGRAM.mmd a été créé.")
        print("   Vous pouvez le visualiser sur https://mermaid.live/")
        print("   ou installer mermaid-cli pour générer le PNG automatiquement.")

