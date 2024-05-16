from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import F

class CustomUser(AbstractUser):
    tel = models.CharField(max_length=20, blank=True)
    type = models.CharField(max_length=20)  # 'admin' ou 'acheteur'

    def __str__(self):
        return self.username

class Administration(models.Model):
    name_administration = models.CharField(max_length=255)
    adresse_administration = models.CharField(max_length=255)

    def __str__(self):
        return self.name_administration

class ComplexeSportif(models.Model):
    name_complexe = models.CharField(max_length=255)
    adresse_complexe = models.CharField(max_length=255)
    administration = models.ForeignKey(Administration, on_delete=models.CASCADE, related_name='complexes')

    def __str__(self):
        return self.name_complexe

class Hall(models.Model):
    name = models.CharField(max_length=255)
    number_place = models.IntegerField()
    complexe_sportif = models.ForeignKey(ComplexeSportif, on_delete=models.CASCADE, related_name='halls')

    def __str__(self):
        return self.name

class EpreuveSportive(models.Model):
    name_epreuve_sportive = models.CharField(max_length=255)
    type_epreuve_sportive = models.CharField(max_length=255)
    duration_epreuve_sportive = models.DurationField()
    niveau_epreuve = models.CharField(max_length=255)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='epreuves')

    def __str__(self):
        return self.name_epreuve_sportive

class Tarif(models.Model):
    name_tarif = models.CharField(max_length=255)
    tarif = models.FloatField()
    offre_tarif = models.CharField(max_length=255)

    def __str__(self):
        return self.name_tarif

class TokenTicket(models.Model):
    numero_token = models.CharField(max_length=255)

    def __str__(self):
        return self.numero_token

class AssociationToken(models.Model):
    token_ticket = models.OneToOneField(TokenTicket, on_delete=models.CASCADE, related_name='association')

    def __str__(self):
        return f"Association for {self.token_ticket.numero_token}"

class TokenUser(models.Model):
    numero_token = models.CharField(max_length=255)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='token_user', limit_choices_to={'type': 'acheteur'})
    association_token = models.OneToOneField(AssociationToken, on_delete=models.CASCADE, related_name='token_user')

    def __str__(self):
        return self.numero_token

class Ticket(models.Model):
    start_time_epreuve = models.DateTimeField()
    administration = models.ForeignKey(Administration, on_delete=models.CASCADE, related_name='tickets')
    complexe_sportif = models.ForeignKey(ComplexeSportif, on_delete=models.CASCADE, related_name='tickets')
    epreuve_sportive = models.ForeignKey(EpreuveSportive, on_delete=models.CASCADE, related_name='tickets')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='tickets')
    tarifs = models.ManyToManyField(Tarif, related_name='tickets')
    token_ticket = models.OneToOneField(TokenTicket, on_delete=models.CASCADE, related_name='ticket', null=True, blank=True)
    remaining_places = models.IntegerField(default=0)

    def __str__(self):
        return f"Ticket for {self.epreuve_sportive.name_epreuve_sportive} at {self.start_time_epreuve}"

class Achat(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='achats')
    nombre_tickets = models.IntegerField()
    prix_ticket = models.DecimalField(max_digits=8, decimal_places=2)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2)
    date_achat = models.DateTimeField(auto_now_add=True)
    user_acheteur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='achats', limit_choices_to={'type': 'acheteur'})

    def save(self, *args, **kwargs):
        if not self.pk:  # Vérifie si c'est un nouvel objet
            if self.ticket.remaining_places >= self.nombre_tickets:
                self.ticket.remaining_places = F('remaining_places') - self.nombre_tickets
                self.ticket.save()
                self.prix_total = self.nombre_tickets * self.prix_ticket
                super().save(*args, **kwargs)
            else:
                raise ValueError("Not enough remaining places")

    def __str__(self):
        return f"{self.nombre_tickets} tickets bought for {self.ticket.epreuve_sportive.name_epreuve_sportive} on {self.date_achat}"
