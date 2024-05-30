from io import BytesIO
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import qrcode
from rest_framework import viewsets
import json
from .utils import generate_qr_code
from .models import Administration, ComplexeSportif, Hall, EpreuveSportive, CustomUser, Tarif, Ticket, Achat
from .serializers import (AdministrationSerializer, ComplexeSportifSerializer, HallSerializer, EpreuveSportiveSerializer, CustomUserSerializer, TarifSerializer,TicketSerializer, AchatSerializer)
from rest_framework import generics
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from .serializers import TicketDetailSerializer  # Ma
from rest_framework import status

from studijeuxolympiques import serializers

class AdministrationViewSet(viewsets.ModelViewSet):
    queryset = Administration.objects.all()
    serializer_class = AdministrationSerializer

class ComplexeSportifViewSet(viewsets.ModelViewSet):
    queryset = ComplexeSportif.objects.all()
    serializer_class = ComplexeSportifSerializer

class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer

class EpreuveSportiveViewSet(viewsets.ModelViewSet):
    queryset = EpreuveSportive.objects.all()
    serializer_class = EpreuveSportiveSerializer

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def categories(self, request):
        categories = EpreuveSportive.objects.values('type_epreuve_sportive', 'image_url').distinct()
        response_data = []
        for category in categories:
            first_epreuve = EpreuveSportive.objects.filter(type_epreuve_sportive=category['type_epreuve_sportive']).first()
            response_data.append({
                'type_epreuve_sportive': category['type_epreuve_sportive'],
                'image_url': first_epreuve.image_url if first_epreuve else 'https://example.com/default.jpg'
            })
        return Response(response_data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def by_level(self, request):
        niveau = request.query_params.get('niveau_epreuve')
        if not niveau:
            return Response({"detail": "Niveau d'épreuve non spécifié"}, status=400)
        
        # Supprimer les espaces de début et de fin et normaliser la casse
        niveau = niveau.strip().capitalize()
        
        epreuves = EpreuveSportive.objects.filter(niveau_epreuve__iexact=niveau)
        tickets = Ticket.objects.filter(epreuve_sportive__in=epreuves)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'categories', 'by_level']:
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class TarifViewSet(viewsets.ModelViewSet):
    queryset = Tarif.objects.all()
    serializer_class = TarifSerializer

# class TokenTicketViewSet(viewsets.ModelViewSet):
#     queryset = TokenTicket.objects.all()
#     serializer_class = TokenTicketSerializer

# class TokenUserViewSet(viewsets.ModelViewSet):
#     queryset = TokenUser.objects.all()
#     serializer_class = TokenUserSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def by_category(self, request, type_epreuve_sportive=None):
        type_epreuve_sportive = request.query_params.get('type_epreuve_sportive', None)
        if type_epreuve_sportive:
            tickets = Ticket.objects.filter(epreuve_sportive__type_epreuve_sportive=type_epreuve_sportive)
            serializer = self.get_serializer(tickets, many=True)
            return Response(serializer.data)
        return Response({"detail": "Type d'épreuve sportive non spécifié"}, status=400)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'by_category']:
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

class AchatViewSet(viewsets.ModelViewSet):
    queryset = Achat.objects.all()
    serializer_class = AchatSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        achat_data = serializer.validated_data

        # Vérification des places disponibles
        ticket = achat_data['ticket']
        if ticket.remaining_places < achat_data['nombre_tickets']:
            return Response({"error": "Not enough remaining places"}, status=status.HTTP_400_BAD_REQUEST)

        # Création de l'achat
        achat = Achat.objects.create(**achat_data)
        
        # Mise à jour des places restantes
        ticket.remaining_places -= achat_data['nombre_tickets']
        ticket.save()

        # Calcul du prix total
        achat.prix_total = achat.nombre_tickets * achat.prix_ticket
        
        # Génération du QR code
        qr_data = f"Achat ID: {achat.id}, Ticket ID: {achat.ticket.id}, User ID: {achat.user_acheteur.id}"
        qr_file = generate_qr_code(qr_data)
        achat.qr_code.save(qr_file.name, qr_file)

        achat.save()

        # Re-serialize the achat instance to include the new qr_code field
        serializer = self.get_serializer(achat)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)




class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        try:
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])  # Hacher le mot de passe
            user.is_active = True  # Assurez-vous que l'utilisateur est actif
            user.save()
        except KeyError as e:
            raise serializers.ValidationError({"error": f"Missing field: {str(e)}"})
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})
        
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    
class UserAchatListView(generics.ListAPIView):
    serializer_class = AchatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Achat.objects.filter(user_acheteur=user)  
    

@api_view(['GET'])
def ticket_details(request, ticket_ids):
    try:
        ids = ticket_ids.split(',')
        tickets = Ticket.objects.filter(id__in=ids)
        serializer = TicketDetailSerializer(tickets, many=True)
        return Response(serializer.data)
    except Ticket.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

# class AssociationTokenViewSet(viewsets.ModelViewSet):
#     queryset = AssociationToken.objects.all()
#     serializer_class = AssociationTokenSerializer
#     permission_classes = [IsAuthenticated]

# @csrf_exempt
# def verify_qr_code(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             ticket_id = data.get('ticketId')
#             user_id = data.get('userId')
#             purchase_id = data.get('purchaseId')

#             achat = Achat.objects.get(id=purchase_id, ticket__id=ticket_id, user_acheteur__id=user_id)
#             return JsonResponse({'status': 'success', 'message': 'QR code verified successfully'})
#         except Achat.DoesNotExist:
#             return HttpResponseBadRequest('Invalid QR code data')
#     return HttpResponseBadRequest('Invalid request method')