from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('user/', include('users.urls')),
    path("", include("rates.urls")),

    path('user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/doc/", 
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="docs"
    ),
]
