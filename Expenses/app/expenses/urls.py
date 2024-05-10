from django.urls import path
from expenses import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:pk>/", views.portfolio_detail, name="portfolio_detail"),
]