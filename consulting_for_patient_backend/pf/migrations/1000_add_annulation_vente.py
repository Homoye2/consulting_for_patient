# Migration pour ajouter les champs d'annulation de vente

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pf', '0999_add_factures_fournisseurs'),
    ]

    operations = [
        migrations.AddField(
            model_name='ventepharmacie',
            name='annulee',
            field=models.BooleanField(default=False, verbose_name='Vente annulée'),
        ),
        migrations.AddField(
            model_name='ventepharmacie',
            name='motif_annulation',
            field=models.TextField(blank=True, verbose_name='Motif d\'annulation'),
        ),
        migrations.AddField(
            model_name='ventepharmacie',
            name='date_annulation',
            field=models.DateTimeField(null=True, blank=True, verbose_name='Date d\'annulation'),
        ),
        migrations.AddField(
            model_name='ventepharmacie',
            name='annulee_par',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=models.SET_NULL,
                related_name='ventes_annulees',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Annulée par'
            ),
        ),
    ]
