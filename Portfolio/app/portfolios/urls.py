from django.urls import path
from portfolios import views

urlpatterns = [
    path("", views.portfolio_index, name="portfolio_index"),
    path("<int:pk>/", views.portfolio_detail, name="portfolio_detail"),
    path("<int:pk>/getTickerInfos/", views.get_ticker_infos, name='get_ticker_infos'),
    path("add_ticker/<int:pk>/", views.add_ticker, name='add_ticker')
]