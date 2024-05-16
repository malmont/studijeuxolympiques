from rest_framework import serializers
from .models import Administration, ComplexeSportif, Hall, EpreuveSportive, CustomUser, Tarif, TokenTicket, AssociationToken, TokenUser, Ticket, Achat
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class AdministrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administration
        fields = '__all__'

class ComplexeSportifSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplexeSportif
        fields = ['name_complexe', 'adresse_complexe']

class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ['name', 'number_place']

class EpreuveSportiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = EpreuveSportive
        fields = ['name_epreuve_sportive', 'type_epreuve_sportive', 'duration_epreuve_sportive', 'niveau_epreuve']

class TarifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarif
        fields = ['name_tarif', 'tarif', 'offre_tarif']


class TokenTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenTicket
        fields = '__all__'

class AssociationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssociationToken
        fields = '__all__'

class TokenUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenUser
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    complexe_sportif = ComplexeSportifSerializer()
    epreuve_sportive = EpreuveSportiveSerializer()
    hall = HallSerializer()
    tarifs = TarifSerializer(many=True)

    class Meta:
        model = Ticket
        fields = ['id', 'start_time_epreuve', 'complexe_sportif', 'epreuve_sportive', 'hall', 'tarifs', 'remaining_places']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'tel']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])  # Hacher le mot de passe
        user.save()
        return user

class AchatSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer()
    user_acheteur_name = serializers.SerializerMethodField()

    class Meta:
        model = Achat
        fields = ['id', 'ticket', 'nombre_tickets', 'prix_ticket', 'prix_total', 'date_achat', 'user_acheteur', 'user_acheteur_name']

    def get_user_acheteur_name(self, obj):
        return obj.user_acheteur.username
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_id'] = user.id
        token['username'] = user.username

        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer    