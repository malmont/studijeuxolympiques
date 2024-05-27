# studijeuxolympiques/tests/test_models.py

import pytest
from django.contrib.auth import get_user_model
from studijeuxolympiques.models import (
    Administration, ComplexeSportif, Hall, EpreuveSportive, 
    Tarif, Ticket, Achat
)
from datetime import timedelta
from django.utils import timezone

@pytest.mark.django_db
def test_custom_user_creation():
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="password", tel="123456789", type="acheteur")
    assert user.username == "testuser"
    assert user.tel == "123456789"
    assert user.type == "acheteur"

@pytest.mark.django_db
def test_administration_creation():
    admin = Administration.objects.create(name_administration="Admin1", adresse_administration="123 Street")
    assert admin.name_administration == "Admin1"
    assert admin.adresse_administration == "123 Street"

@pytest.mark.django_db
def test_complexe_sportif_creation():
    admin = Administration.objects.create(name_administration="Admin1", adresse_administration="123 Street")
    complexe = ComplexeSportif.objects.create(name_complexe="Complexe1", adresse_complexe="456 Avenue", administration=admin)
    assert complexe.name_complexe == "Complexe1"
    assert complexe.adresse_complexe == "456 Avenue"
    assert complexe.administration == admin

@pytest.mark.django_db
def test_hall_creation():
    admin = Administration.objects.create(name_administration="Admin1", adresse_administration="123 Street")
    complexe = ComplexeSportif.objects.create(name_complexe="Complexe1", adresse_complexe="456 Avenue", administration=admin)
    hall = Hall.objects.create(name="Hall1", number_place=100, complexe_sportif=complexe)
    assert hall.name == "Hall1"
    assert hall.number_place == 100
    assert hall.complexe_sportif == complexe

@pytest.mark.django_db
def test_epreuve_sportive_creation():
    admin = Administration.objects.create(name_administration="Admin1", adresse_administration="123 Street")
    complexe = ComplexeSportif.objects.create(name_complexe="Complexe1", adresse_complexe="456 Avenue", administration=admin)
    hall = Hall.objects.create(name="Hall1", number_place=100, complexe_sportif=complexe)
    epreuve = EpreuveSportive.objects.create(
        name_epreuve_sportive="Epreuve1", 
        type_epreuve_sportive="Type1", 
        duration_epreuve_sportive=timedelta(hours=1),
        niveau_epreuve="Niveau1",
        hall=hall
    )
    assert epreuve.name_epreuve_sportive == "Epreuve1"
    assert epreuve.type_epreuve_sportive == "Type1"
    assert epreuve.duration_epreuve_sportive == timedelta(hours=1)
    assert epreuve.niveau_epreuve == "Niveau1"
    assert epreuve.hall == hall

@pytest.mark.django_db
def test_tarif_creation():
    tarif = Tarif.objects.create(name_tarif="Tarif1", tarif=100.0, offre_tarif="Offre1")
    assert tarif.name_tarif == "Tarif1"
    assert tarif.tarif == 100.0
    assert tarif.offre_tarif == "Offre1"

@pytest.mark.django_db
def test_ticket_creation():
    admin = Administration.objects.create(name_administration="Admin1", adresse_administration="123 Street")
    complexe = ComplexeSportif.objects.create(name_complexe="Complexe1", adresse_complexe="456 Avenue", administration=admin)
    hall = Hall.objects.create(name="Hall1", number_place=100, complexe_sportif=complexe)
    epreuve = EpreuveSportive.objects.create(
        name_epreuve_sportive="Epreuve1", 
        type_epreuve_sportive="Type1", 
        duration_epreuve_sportive=timedelta(hours=1),
        niveau_epreuve="Niveau1",
        hall=hall
    )
    ticket = Ticket.objects.create(
        start_time_epreuve=timezone.now(),
        administration=admin,
        complexe_sportif=complexe,
        epreuve_sportive=epreuve,
        hall=hall,
        remaining_places=50
    )
    assert ticket.epreuve_sportive == epreuve
    assert ticket.remaining_places == 50

@pytest.mark.django_db
def test_achat_creation():
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="password", tel="123456789", type="acheteur")
    admin = Administration.objects.create(name_administration="Admin1", adresse_administration="123 Street")
    complexe = ComplexeSportif.objects.create(name_complexe="Complexe1", adresse_complexe="456 Avenue", administration=admin)
    hall = Hall.objects.create(name="Hall1", number_place=100, complexe_sportif=complexe)
    epreuve = EpreuveSportive.objects.create(
        name_epreuve_sportive="Epreuve1", 
        type_epreuve_sportive="Type1", 
        duration_epreuve_sportive=timedelta(hours=1),
        niveau_epreuve="Niveau1",
        hall=hall
    )
    ticket = Ticket.objects.create(
        start_time_epreuve=timezone.now(),
        administration=admin,
        complexe_sportif=complexe,
        epreuve_sportive=epreuve,
        hall=hall,
        remaining_places=50
    )
    achat = Achat.objects.create(
        ticket=ticket,
        nombre_tickets=2,
        prix_ticket=50.00,
        prix_total=100.00,
        user_acheteur=user
    )
    assert achat.ticket == ticket
    assert achat.nombre_tickets == 2
    assert achat.prix_ticket == 50.00
    assert achat.prix_total == 100.00
    assert achat.user_acheteur == user
