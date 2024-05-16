# Generated by Django 4.2.13 on 2024-05-15 15:41

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('tel', models.CharField(blank=True, max_length=20)),
                ('type', models.CharField(max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Administration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_administration', models.CharField(max_length=255)),
                ('adresse_administration', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='AssociationToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ComplexeSportif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_complexe', models.CharField(max_length=255)),
                ('adresse_complexe', models.CharField(max_length=255)),
                ('administration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complexes', to='studijeuxolympiques.administration')),
            ],
        ),
        migrations.CreateModel(
            name='EpreuveSportive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_epreuve_sportive', models.CharField(max_length=255)),
                ('type_epreuve_sportive', models.CharField(max_length=255)),
                ('duration_epreuve_sportive', models.DurationField()),
                ('niveau_epreuve', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('number_place', models.IntegerField()),
                ('complexe_sportif', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='halls', to='studijeuxolympiques.complexesportif')),
            ],
        ),
        migrations.CreateModel(
            name='Tarif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_tarif', models.CharField(max_length=255)),
                ('tarif', models.FloatField()),
                ('offre_tarif', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TokenTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_token', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TokenUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_token', models.CharField(max_length=255)),
                ('association_token', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='token_user', to='studijeuxolympiques.associationtoken')),
                ('user', models.OneToOneField(limit_choices_to={'type': 'acheteur'}, on_delete=django.db.models.deletion.CASCADE, related_name='token_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time_epreuve', models.DateTimeField()),
                ('remaining_places', models.IntegerField(default=0)),
                ('administration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='studijeuxolympiques.administration')),
                ('complexe_sportif', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='studijeuxolympiques.complexesportif')),
                ('epreuve_sportive', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='studijeuxolympiques.epreuvesportive')),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='studijeuxolympiques.hall')),
                ('tarifs', models.ManyToManyField(related_name='tickets', to='studijeuxolympiques.tarif')),
                ('token_ticket', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ticket', to='studijeuxolympiques.tokenticket')),
                ('user_admin', models.ForeignKey(limit_choices_to={'type': 'admin'}, on_delete=django.db.models.deletion.CASCADE, related_name='created_tickets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='epreuvesportive',
            name='hall',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='epreuves', to='studijeuxolympiques.hall'),
        ),
        migrations.AddField(
            model_name='associationtoken',
            name='token_ticket',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='association', to='studijeuxolympiques.tokenticket'),
        ),
        migrations.CreateModel(
            name='Achat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_tickets', models.IntegerField()),
                ('prix_ticket', models.DecimalField(decimal_places=2, max_digits=8)),
                ('prix_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_achat', models.DateTimeField(auto_now_add=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achats', to='studijeuxolympiques.ticket')),
                ('user_acheteur', models.ForeignKey(limit_choices_to={'type': 'acheteur'}, on_delete=django.db.models.deletion.CASCADE, related_name='achats', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
