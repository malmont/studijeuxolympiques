# Generated by Django 4.2.13 on 2024-05-18 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studijeuxolympiques', '0002_remove_ticket_user_admin_alter_ticket_token_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='epreuvesportive',
            name='image_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]