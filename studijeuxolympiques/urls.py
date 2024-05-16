
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from studijeuxolympiques.studijeuxolympiques.views import RegisterUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('studijeuxolympiques.urls')),  # Inclure les URLs de l'application reservations
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

