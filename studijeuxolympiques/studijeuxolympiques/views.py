from rest_framework import viewsets
from .models import Administration, ComplexeSportif, Hall, EpreuveSportive, CustomUser, Tarif, TokenTicket, AssociationToken, TokenUser, Ticket, Achat
from .serializers import (AdministrationSerializer, ComplexeSportifSerializer, HallSerializer, EpreuveSportiveSerializer, CustomUserSerializer, TarifSerializer, TokenTicketSerializer, AssociationTokenSerializer, TokenUserSerializer, TicketSerializer, AchatSerializer)
from rest_framework import generics
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Achat
from .serializers import AchatSerializer
from rest_framework.decorators import action
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from .serializers import TicketDetailSerializer  # Ma
from rest_framework import status

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

class TokenTicketViewSet(viewsets.ModelViewSet):
    queryset = TokenTicket.objects.all()
    serializer_class = TokenTicketSerializer

class AssociationTokenViewSet(viewsets.ModelViewSet):
    queryset = AssociationToken.objects.all()
    serializer_class = AssociationTokenSerializer

class TokenUserViewSet(viewsets.ModelViewSet):
    queryset = TokenUser.objects.all()
    serializer_class = TokenUserSerializer

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
        try:
            token_user = user.token_user
        except TokenUser.DoesNotExist:
            # Créez une instance de TokenTicket
            token_ticket = TokenTicket.objects.create(
                # Ajoutez les champs nécessaires pour TokenTicket ici
            )
            # Créez une instance d'AssociationToken
            association_token = AssociationToken.objects.create(token_ticket=token_ticket)
            # Créez une instance de TokenUser
            token_user = TokenUser.objects.create(user=user, association_token=association_token, numero_token='votre_numero_token')  # Remplacez 'votre_numero_token' par le token réel ou générez-le dynamiquement

        # Ensuite, continuez avec la création de l'achat
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
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

            # Create TokenTicket
            token_ticket = TokenTicket.objects.create(
                # Ajouter les champs nécessaires ici pour TokenTicket
            )

            # Create AssociationToken
            association_token = AssociationToken.objects.create(token_ticket=token_ticket)

            # Create TokenUser
            TokenUser.objects.create(user=user, association_token=association_token, numero_token='votre_numero_token')

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
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