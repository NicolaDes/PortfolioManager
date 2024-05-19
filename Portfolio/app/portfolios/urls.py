from django.urls import path
from portfolios import views

urlpatterns = [
    path("", views.portfolio_index, name="portfolio_index"),
    path("<int:pk>/", views.portfolio_detail, name="portfolio_detail"),
    path("<int:pk>/getTickerInfos/", views.get_ticker_infos, name='get_ticker_infos'),
    path("new_ticker/<int:pk>/", views.new_ticker, name='new_ticker'),
    path("remove_ticker/<int:pk>/", views.remove_ticker, name='remove_ticker'),
    path("increase_ticker/<int:pk>/", views.increase_ticker, name='increase_ticker'),
    path("edit_portfolio/<int:pk>/", views.edit_portfolio, name='edit_portfolio')
]