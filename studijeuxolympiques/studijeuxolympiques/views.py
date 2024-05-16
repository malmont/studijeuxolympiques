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

class AchatViewSet(viewsets.ModelViewSet):
    queryset = Achat.objects.all()
    serializer_class = AchatSerializer
    permission_classes = [IsAuthenticated]

class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        user = serializer.save(commit=False)
        user.set_password(serializer.validated_data['password'])  # Hacher le mot de passe
        user.is_active = True  # Assurez-vous que l'utilisateur est actif
        user.save()

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