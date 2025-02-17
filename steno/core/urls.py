from django.urls import path
from .views import home, pricing, dashboard

urlpatterns = [
    path("/", home, name="home"),
    path("pricing/", pricing, name="pricing"),
    path("dashboard/", dashboard, name="dashboard"),
]
