# Generated manually for factures fournisseurs

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pf', '0009_remove_consultationpf_methode_prescite_and_more'),
    ]

    operations = [
        # Ajouter les nouvelles permissions aux employés
        migrations.AddField(
            model_name='employepharmacie',
            name='peut_annuler_vente',
            field=models.BooleanField(default=False, verbose_name='Peut annuler une vente'),
        ),
        migrations.AddField(
            model_name='employepharmacie',
            name='peut_enregistrer_facture',
            field=models.BooleanField(default=False, verbose_name='Peut enregistrer des factures fournisseurs'),
        ),
        
        # Créer le modèle Fournisseur
        migrations.CreateModel(
            name='Fournisseur',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=200, verbose_name='Nom du fournisseur')),
                ('adresse', models.TextField(verbose_name='Adresse')),
                ('ville', models.CharField(max_length=100, verbose_name='Ville')),
                ('pays', models.CharField(default='Sénégal', max_length=100, verbose_name='Pays')),
                ('telephone', models.CharField(max_length=20, verbose_name='Téléphone')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('numero_registre_commerce', models.CharField(blank=True, max_length=100, null=True, verbose_name='Numéro de registre de commerce')),
                ('numero_identification_fiscale', models.CharField(blank=True, max_length=100, null=True, verbose_name='NIF')),
                ('delai_paiement_jours', models.IntegerField(default=30, verbose_name='Délai de paiement (jours)')),
                ('remise_habituelle', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Remise habituelle (%)')),
                ('actif', models.BooleanField(default=True, verbose_name='Actif')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Fournisseur',
                'verbose_name_plural': 'Fournisseurs',
                'db_table': 'fournisseurs',
                'ordering': ['nom'],
            },
        ),
        
        # Créer le modèle FactureFournisseur
        migrations.CreateModel(
            name='FactureFournisseur',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('numero_facture', models.CharField(max_length=100, unique=True, verbose_name='Numéro de facture')),
                ('date_facture', models.DateField(verbose_name='Date de la facture')),
                ('date_enregistrement', models.DateTimeField(auto_now_add=True, verbose_name="Date d'enregistrement")),
                ('date_echeance', models.DateField(verbose_name="Date d'échéance")),
                ('montant_ht', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Montant HT')),
                ('montant_tva', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Montant TVA')),
                ('montant_remise', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Montant remise')),
                ('montant_total', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Montant total TTC')),
                ('mode_paiement', models.CharField(choices=[('especes', 'Espèces'), ('cheque', 'Chèque'), ('virement', 'Virement bancaire'), ('mobile_money', 'Mobile Money'), ('credit', 'À crédit')], default='credit', max_length=20, verbose_name='Mode de paiement')),
                ('montant_paye', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Montant payé')),
                ('statut', models.CharField(choices=[('en_attente', 'En attente de validation'), ('validee', 'Validée'), ('annulee', 'Annulée')], default='en_attente', max_length=20, verbose_name='Statut')),
                ('stock_incremente', models.BooleanField(default=False, verbose_name='Stock incrémenté')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('fichier_facture', models.FileField(blank=True, null=True, upload_to='factures_fournisseurs/', verbose_name='Fichier de la facture')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('enregistre_par', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factures_enregistrees', to=settings.AUTH_USER_MODEL, verbose_name='Enregistré par')),
                ('fournisseur', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='factures', to='pf.fournisseur', verbose_name='Fournisseur')),
                ('pharmacie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factures_fournisseurs', to='pf.pharmacie', verbose_name='Pharmacie')),
            ],
            options={
                'verbose_name': 'Facture Fournisseur',
                'verbose_name_plural': 'Factures Fournisseurs',
                'db_table': 'factures_fournisseurs',
                'ordering': ['-date_facture', '-created_at'],
            },
        ),
        
        # Créer le modèle LigneFactureFournisseur
        migrations.CreateModel(
            name='LigneFactureFournisseur',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nom_produit', models.CharField(max_length=200, verbose_name='Nom du produit')),
                ('quantite', models.IntegerField(verbose_name='Quantité')),
                ('prix_unitaire_ht', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Prix unitaire HT')),
                ('taux_tva', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Taux TVA (%)')),
                ('remise_ligne', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Remise ligne')),
                ('montant_ht', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Montant HT')),
                ('montant_tva', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Montant TVA')),
                ('montant_ttc', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Montant TTC')),
                ('numero_lot', models.CharField(blank=True, max_length=100, verbose_name='Numéro de lot')),
                ('date_peremption', models.DateField(blank=True, null=True, verbose_name='Date de péremption')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('facture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lignes', to='pf.facturefournisseur', verbose_name='Facture')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='lignes_factures_fournisseur', to='pf.produit', verbose_name='Produit')),
            ],
            options={
                'verbose_name': 'Ligne de Facture Fournisseur',
                'verbose_name_plural': 'Lignes de Factures Fournisseurs',
                'db_table': 'lignes_factures_fournisseurs',
                'ordering': ['id'],
            },
        ),
        
        # Ajouter les indexes
        migrations.AddIndex(
            model_name='fournisseur',
            index=models.Index(fields=['nom'], name='fournisseur_nom_idx'),
        ),
        migrations.AddIndex(
            model_name='fournisseur',
            index=models.Index(fields=['actif'], name='fournisseur_actif_idx'),
        ),
        migrations.AddIndex(
            model_name='facturefournisseur',
            index=models.Index(fields=['pharmacie', 'statut'], name='facture_pharmacie_statut_idx'),
        ),
        migrations.AddIndex(
            model_name='facturefournisseur',
            index=models.Index(fields=['fournisseur'], name='facture_fournisseur_idx'),
        ),
        migrations.AddIndex(
            model_name='facturefournisseur',
            index=models.Index(fields=['numero_facture'], name='facture_numero_idx'),
        ),
        migrations.AddIndex(
            model_name='facturefournisseur',
            index=models.Index(fields=['date_facture'], name='facture_date_idx'),
        ),
        migrations.AddIndex(
            model_name='facturefournisseur',
            index=models.Index(fields=['statut'], name='facture_statut_idx'),
        ),
        migrations.AddIndex(
            model_name='lignefacturefournisseur',
            index=models.Index(fields=['facture'], name='ligne_facture_idx'),
        ),
        migrations.AddIndex(
            model_name='lignefacturefournisseur',
            index=models.Index(fields=['produit'], name='ligne_produit_idx'),
        ),
    ]
