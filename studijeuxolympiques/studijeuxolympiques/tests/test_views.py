# studijeuxolympiques/tests/test_views.py

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from studijeuxolympiques.models import Administration, ComplexeSportif, Hall, EpreuveSportive, CustomUser, Tarif, Ticket, Achat
from django.utils import timezone
from datetime import timedelta

@pytest.fixture
def api_client():
    return APIClient()

# @pytest.mark.django_db
# def test_administration_viewset(api_client):
#     url = reverse('administration-list')
#     data = {"name_administration": "Admin1", "adresse_administration": "123 Street"}
#     response = api_client.post(url, data, format='json')
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.data['name_administration'] == "Admin1"
#     assert response.data['adresse_administration'] == "123 Street"

# @pytest.mark.django_db
# def test_complexe_sportif_viewset(api_client):
#     admin = Administration.objects.create(name_administration="Admin1", adresse_administration="123 Street")
#     url = reverse('complexesportif-list')
#     data = {"name_complexe": "Complexe1", "adresse_complexe": "456 Avenue", "administration": admin.id}
#     response = api_client.post(url, data, format='json')
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.data['name_complexe'] == "Complexe1"
#     assert response.data['adresse_complexe'] == "456 Avenue"
#     assert response.data['administration'] == admin.id

# @pytest.mark.django_db
# def test_hall_viewset(api_client):
#     admin = Administration.objects.create(name_administration="Admin1", adresse_administration="123 Street")
#     complexe = ComplexeSportif.objects.create(name_complexe="Complexe1", adresse_complexe="456 Avenue", administration=admin)
#     url = reverse('hall-list')
#     data = {"name": "Hall1", "number_place": 100, "complexe_sportif": complexe.id}
#     response = api_client.post(url, data, format='json')
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.data['name'] == "Hall1"
#     assert response.data['number_place'] == 100
#     assert response.data['complexe_sportif'] == complexe.id

# @pytest.mark.django_db
# def test_epreuve_sportive_viewset(api_client):
#     admin = Administration.objects.create(name_administration="Admin1", adresse_administration="123 Street")
#     complexe = ComplexeSportif.objects.create(name_complexe="Complexe1", adresse_complexe="456 Avenue", administration=admin)
#     hall = Hall.objects.create(name="Hall1", number_place=100, complexe_sportif=complexe)
#     url = reverse('epreuvesportive-list')
#     data = {
#         "name_epreuve_sportive": "Epreuve1", 
#         "type_epreuve_sportive": "Type1", 
#         "duration_epreuve_sportive": timedelta(hours=1),
#         "niveau_epreuve": "Niveau1",
#         "image_url": "",
#         "hall": hall.id
#     }
#     response = api_client.post(url, data, format='json')
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.data['name_epreuve_sportive'] == "Epreuve1"
#     assert response.data['type_epreuve_sportive'] == "Type1"
#     assert response.data['duration_epreuve_sportive'] == "01:00:00"
#     assert response.data['niveau_epreuve'] == "Niveau1"
#     assert response.data['hall'] == hall.id

# @pytest.mark.django_db
# def test_tarif_viewset(api_client):
#     url = reverse('tarif-list')
#     data = {"name_tarif": "Tarif1", "tarif": 100.0, "offre_tarif": "Offre1"}
#     response = api_client.post(url, data, format='json')
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.data['name_tarif'] == "Tarif1"
#     assert response.data['tarif'] == 100.0
#     assert response.data['offre_tarif'] == "Offre1"

# @pytest.mark.django_db
# def test_ticket_viewset(api_client):
#     admin = Administration.objects.create(name_administration="Admin1", adresse_administration="123 Street")
#     complexe = ComplexeSportif.objects.create(name_complexe="Complexe1", adresse_complexe="456 Avenue", administration=admin)
#     hall = Hall.objects.create(name="Hall1", number_place=100, complexe_sportif=complexe)
#     epreuve = EpreuveSportive.objects.create(
#         name_epreuve_sportive="Epreuve1", 
#         type_epreuve_sportive="Type1", 
#         duration_epreuve_sportive=timedelta(hours=1),
#         niveau_epreuve="Niveau1",
#         hall=hall
#     )
#     url = reverse('ticket-list')
#     data = {
#         "start_time_epreuve": timezone.now(),
#         "complexe_sportif": complexe.id,
#         "epreuve_sportive": epreuve.id,
#         "hall": hall.id,
#         "remaining_places": 50
#     }
#     response = api_client.post(url, data, format='json')
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.data['complexe_sportif'] == complexe.id
#     assert response.data['epreuve_sportive'] == epreuve.id
#     assert response.data['hall'] == hall.id
#     assert response.data['remaining_places'] == 50

@pytest.mark.django_db
def test_achat_viewset(api_client):
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
    api_client.force_authenticate(user=user)
    url = reverse('achat-list')
    data = {
        "ticket": ticket.id,
        "nombre_tickets": 2,
        "prix_ticket": 50.00,
        "prix_total": 100.00,
        "user_acheteur": user.id
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['ticket'] == ticket.id
    assert response.data['nombre_tickets'] == 2
    assert response.data['prix_ticket'] == "50.00"  # Decimal field
    assert response.data['prix_total'] == "100.00"  # Decimal field
    assert response.data['user_acheteur'] == user.id
