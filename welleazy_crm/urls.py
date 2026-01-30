"""
URL configuration for welleazy_crm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



from django.contrib import admin
from django.urls import path,include
from apps.accounts.views import (
    AdminLoginAPIView,
    AdminLogoutAPIView,
)


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("api/admin/login/", AdminLoginAPIView.as_view()),
    path("api/admin/logout/", AdminLogoutAPIView.as_view()),

    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    path("api/physical-medicals/", include("apps.physical_medicals.urls")), 
    path("api/second-opinion/", include("apps.second_opinion.urls")),
    path('api/second-opinion-master/',include('apps.second_opinion_master.urls')),
    path("api/physical-medical-master/",include("apps.physical_medical_master.urls")),

    path('api/master-management/', include('apps.master_management.urls')),
    path('api/client-masters/', include('apps.client_masters.urls')),
    path('api/clients/', include('apps.client.urls')),
    path('api/client-branches/', include('apps.client_branch.urls')),
    path('api/client-product-services/', include('apps.client_product_service.urls')),
    path('api/client-customers/', include('apps.client_customer.urls')),
    path('api/client-customer-login/', include('apps.client_customer_login.urls')),
    path('api/sub-clients/', include('apps.sub_client.urls')),
]
    

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
