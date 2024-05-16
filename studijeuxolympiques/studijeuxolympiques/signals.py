from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, TokenUser, AssociationToken, Achat, TokenTicket

@receiver(post_save, sender=CustomUser)
def create_token_user(sender, instance, created, **kwargs):
    if created and instance.type == 'acheteur':
        association_token = AssociationToken.objects.create()
        TokenUser.objects.create(user=instance, association_token=association_token, numero_token="user_token_" + str(instance.id))

@receiver(post_save, sender=Achat)
def create_token_ticket(sender, instance, created, **kwargs):
    if created:
        token_ticket = TokenTicket.objects.create(numero_token="ticket_token_" + str(instance.id))
        
        # Associer le token_ticket au ticket et enregistrer
        instance.ticket.token_ticket = token_ticket
        instance.ticket.save()

        # Mettre à jour l'association des tokens
        token_user = instance.user_acheteur.token_user
        association_token = token_user.association_token
        association_token.token_ticket = token_ticket
        association_token.save()