from .views import attempt_test_page, attempt_test_api, user_dashboard
from django.urls import path

urlpatterns = [
    path("test/<int:test_id>/attempt/", attempt_test_page, name="attempt_test_page"),
    path("test/<int:test_id>/submit_test/", attempt_test_api, name="attempt_test_api"),
    path("dashboard/", user_dashboard, name="user_dashboard"),
]
