"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token # <-- NEW
from . import views
from home.views import CustomAuthToken, index
from django.views.decorators.csrf import csrf_exempt

admin.site.index = index

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('accounts/register/', index), # To prevent register 
    path('', include('admin_datta.urls')),   
    # path('', include('django_dyn_dt.urls')), # <-- NEW: Dynamic_DT Routing   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Lazy-load on routing is needed
# During the first build, API is not yet generated
try:
    urlpatterns.append( path("api/"      , include("api.urls"))    )
    urlpatterns.append( path("login/jwt/", csrf_exempt(CustomAuthToken.as_view()) ))
except:
    pass

urlpatterns.append(re_path(r'^.*\.*', views.pages, name='pages'))
