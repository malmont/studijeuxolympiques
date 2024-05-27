# studijeuxolympiques/tests/test_serializers.py

import pytest
from studijeuxolympiques.serializers import (
    AdministrationSerializer, ComplexeSportifSerializer, HallSerializer,
    EpreuveSportiveSerializer, TarifSerializer, CustomUserSerializer, AchatSerializer
)
from studijeuxolympiques.models import (
    Administration, ComplexeSportif, Hall, EpreuveSportive, CustomUser,
    Tarif, Ticket, Achat
)
from django.utils import timezone
from datetime import timedelta

@pytest.mark.django_db
def test_administration_serializer():
    admin_data = {"name_administration": "Admin1", "adresse_administration": "123 Street"}
    serializer = AdministrationSerializer(data=admin_data)
    assert serializer.is_valid()
    admin = serializer.save()
    assert admin.name_administration == "Admin1"
    assert admin.adresse_administration == "123 Street"

@pytest.mark.django_db
def test_complexe_sportif_serializer():
    admin = Administration.objects.create(name_administration="Admin1", adresse_administration="123 Street")
    complexe_data = {"name_complexe": "Complexe1", "adresse_complexe": "456 Avenue"}
    serializer = ComplexeSportifSerializer(data=complexe_data)
    assert serializer.is_valid()
    complexe = serializer.save(administration=admin)
    assert complexe.name_complexe == "Complexe1"
    assert complexe.adresse_complexe == "456 Avenue"
    assert complexe.administration == admin

@pytest.mark.django_db
def test_hall_serializer():
    admin = Administration.objects.create(name_administration="Admin1", adresse_administration="123 Street")
    complexe = ComplexeSportif.objects.create(name_complexe="Complexe1", adresse_complexe="456 Avenue", administration=admin)
    hall_data = {"name": "Hall1", "number_place": 100}
    serializer = HallSerializer(data=hall_data)
    assert serializer.is_valid()
    hall = serializer.save(complexe_sportif=complexe)
    assert hall.name == "Hall1"
    assert hall.number_place == 100
    assert hall.complexe_sportif == complexe

@pytest.mark.django_db
def test_epreuve_sportive_serializer():
    admin = Administration.objects.create(name_administration="Admin1", adresse_administration="123 Street")
    complexe = ComplexeSportif.objects.create(name_complexe="Complexe1", adresse_complexe="456 Avenue", administration=admin)
    hall = Hall.objects.create(name="Hall1", number_place=100, complexe_sportif=complexe)
    epreuve_data = {
        "name_epreuve_sportive": "Epreuve1", 
        "type_epreuve_sportive": "Type1", 
        "duration_epreuve_sportive": timedelta(hours=1),
        "niveau_epreuve": "Niveau1",
        "image_url": ""
    }
    serializer = EpreuveSportiveSerializer(data=epreuve_data)
    assert serializer.is_valid()
    epreuve = serializer.save(hall=hall)
    assert epreuve.name_epreuve_sportive == "Epreuve1"
    assert epreuve.type_epreuve_sportive == "Type1"
    assert epreuve.duration_epreuve_sportive == timedelta(hours=1)
    assert epreuve.niveau_epreuve == "Niveau1"
    assert epreuve.hall == hall

@pytest.mark.django_db
def test_tarif_serializer():
    tarif_data = {"name_tarif": "Tarif1", "tarif": 100.0, "offre_tarif": "Offre1"}
    serializer = TarifSerializer(data=tarif_data)
    assert serializer.is_valid()
    tarif = serializer.save()
    assert tarif.name_tarif == "Tarif1"
    assert tarif.tarif == 100.0
    assert tarif.offre_tarif == "Offre1"

@pytest.mark.django_db
def test_custom_user_serializer():
    user_data = {
        "username": "testuser", 
        "email": "testuser@example.com", 
        "tel": "123456789", 
        "password": "password", 
        "type": "acheteur"
    }
    serializer = CustomUserSerializer(data=user_data)
    assert serializer.is_valid()
    user = serializer.save()
    assert user.username == "testuser"
    assert user.check_password("password")
    assert user.type == "acheteur"

@pytest.mark.django_db
def test_achat_serializer():
    user = CustomUser.objects.create_user(username="testuser", password="password", tel="123456789", type="acheteur")
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
    achat_data = {
        "ticket": ticket.id,
        "nombre_tickets": 2,
        "prix_ticket": 50.00,
        "prix_total": 100.00,
        "user_acheteur": user.id
    }
    serializer = AchatSerializer(data=achat_data)
    assert serializer.is_valid()
    achat = serializer.save()
    assert achat.ticket == ticket
    assert achat.nombre_tickets == 2
    assert achat.prix_ticket == 50.00
    assert achat.prix_total == 100.00
    assert achat.user_acheteur == user
