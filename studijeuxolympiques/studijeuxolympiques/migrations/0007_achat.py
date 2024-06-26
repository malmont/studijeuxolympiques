# Generated by Django 4.2.13 on 2024-05-24 00:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studijeuxolympiques', '0006_delete_achat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_tickets', models.IntegerField()),
                ('prix_ticket', models.DecimalField(decimal_places=2, max_digits=8)),
                ('prix_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_achat', models.DateTimeField(auto_now_add=True)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='qr_codes')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achats', to='studijeuxolympiques.ticket')),
                ('user_acheteur', models.ForeignKey(limit_choices_to={'type': 'acheteur'}, on_delete=django.db.models.deletion.CASCADE, related_name='achats', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
