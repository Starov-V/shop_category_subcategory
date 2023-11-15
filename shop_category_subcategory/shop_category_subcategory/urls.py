from django.contrib import admin
from rest_framework.authtoken import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('', include('api.urls'))
]
