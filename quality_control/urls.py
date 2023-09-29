"""quality_control URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_swagger.views import get_swagger_view
from ore.views import (
    LogoutAPIView, 
    ConcentrateAPIView, 
    DeleteConcentrateAPIView,
    UpdateConcentratesByTableAPIView,
    AggregationOfConcentratesAPIView
)

schema_view = get_swagger_view(title="Reporting on concentrates API")

urlpatterns = [
    path('admin-panel/', admin.site.urls),
    path(
        'api/v1/schema/', 
        schema_view,
        name='schema_api'
    ),
    path('api/v1/login/', obtain_auth_token, name='login_api'),
    path('api/v1/logout/', LogoutAPIView.as_view(), name='logout_api'),
    path(
        'api/v1/concentrates/<int:year>/<int:month>/<str:concentrate_name>/',
        ConcentrateAPIView.as_view(), 
        name='concentrate_api'
    ),
    path(
        'api/v1/concentrates/<int:year>/<int:month>/<str:concentrate_name>/delete/',
        DeleteConcentrateAPIView.as_view(),
        name='delete_concentrate_api'
    ),
    path(
        'api/v1/concentrates/update-by-table/',
        UpdateConcentratesByTableAPIView.as_view(),
        name='update_concentrates_by_table_api'
    ),
    path(
        'api/v1/concentrates/',
        AggregationOfConcentratesAPIView.as_view(),
        name='aggregation_for_all_time_api'
    ),
    path(
        'api/v1/concentrates/<int:year>/',
        AggregationOfConcentratesAPIView.as_view(),
        name='aggregation_for_year_api'
    ),
    path(
        'api/v1/concentrates/<int:year>/<int:month>/',
        AggregationOfConcentratesAPIView.as_view(),
        name='aggregation_for_month_api'
    )
]
