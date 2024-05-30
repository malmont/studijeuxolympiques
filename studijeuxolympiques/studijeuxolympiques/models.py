from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import F

from .utils import generate_qr_code

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
    hall = models.ForeignKey('Hall', on_delete=models.CASCADE, related_name='epreuves')
    image_url = models.URLField(max_length=500, blank=True, null=True)  # Ajouter ce champ

    def __str__(self):
        return self.name_epreuve_sportive

class Tarif(models.Model):
    name_tarif = models.CharField(max_length=255)
    tarif = models.FloatField()
    offre_tarif = models.CharField(max_length=255)

    def __str__(self):
        return self.name_tarif

class Ticket(models.Model):
    start_time_epreuve = models.DateTimeField()
    administration = models.ForeignKey(Administration, on_delete=models.CASCADE, related_name='tickets')
    complexe_sportif = models.ForeignKey(ComplexeSportif, on_delete=models.CASCADE, related_name='tickets')
    epreuve_sportive = models.ForeignKey(EpreuveSportive, on_delete=models.CASCADE, related_name='tickets')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='tickets')
    tarifs = models.ManyToManyField(Tarif, related_name='tickets')
    remaining_places = models.IntegerField(default=0)

    def __str__(self):
        return f"Ticket for {self.epreuve_sportive.name_epreuve_sportive} at {self.start_time_epreuve}"

    @property
    def total_sales(self):
        return self.achats.aggregate(total_sales=models.Sum('nombre_tickets'))['total_sales'] or 0

    def sales_by_offer(self):
        offers = self.tarifs.all()
        sales_by_offer = {}
        for offer in offers:
            total_sales = self.achats.filter(ticket=self, ticket__tarifs=offer).aggregate(total_sales=models.Sum('nombre_tickets'))['total_sales'] or 0
            sales_by_offer[offer] = total_sales
        return sales_by_offer
    
    
class Achat(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='achats')
    nombre_tickets = models.IntegerField()
    prix_ticket = models.DecimalField(max_digits=8, decimal_places=2)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2)
    date_achat = models.DateTimeField(auto_now_add=True)
    user_acheteur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='achats', limit_choices_to={'type': 'acheteur'})
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_tickets} tickets bought for {self.ticket.epreuve_sportive.name_epreuve_sportive} on {self.date_achat}"
