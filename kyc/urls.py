from django.urls import path
from .views import KYCApiView


app_name="single_search"
urlpatterns = [
    path('', KYCApiView.as_view(), name='api'),
]
