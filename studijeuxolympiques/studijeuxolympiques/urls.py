from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ticket_details
from studijeuxolympiques.serializers import CustomTokenObtainPairView
from .views import (
    AdministrationViewSet, ComplexeSportifViewSet, HallViewSet, EpreuveSportiveViewSet, CustomUserViewSet, TarifViewSet, 
    TokenTicketViewSet, AssociationTokenViewSet, TokenUserViewSet, TicketViewSet, AchatViewSet, RegisterUserView, UserAchatListView, UserProfileView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'administrations', AdministrationViewSet)
router.register(r'complexes', ComplexeSportifViewSet)
router.register(r'halls', HallViewSet)
router.register(r'epreuves', EpreuveSportiveViewSet)
router.register(r'users', CustomUserViewSet)
router.register(r'tarifs', TarifViewSet)
router.register(r'tokens_ticket', TokenTicketViewSet)
router.register(r'association_tokens', AssociationTokenViewSet)
router.register(r'tokens_user', TokenUserViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'achats', AchatViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),  # Ajoutez cette ligne pour inclure les URLs de l'administration
    path('', include(router.urls)),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user-profile/', UserProfileView.as_view(), name='user_profile'),
    path('api/user-achats/', UserAchatListView.as_view(), name='user_achats'),
    path('api/ticket-details/<str:ticket_ids>/', ticket_details, name='ticket-details'),
]
