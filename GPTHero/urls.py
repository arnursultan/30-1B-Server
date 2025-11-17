from django.urls import path
from .views import ArlyView

urlpatterns = [
    path('arly', ArlyView.as_view(), name='arly'),
]
