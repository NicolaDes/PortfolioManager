from django.urls import path

from expenses.views import home
from expenses.views import portfolios
from expenses.views import rules

urlpatterns = [
    path("", home.home, name="home"),
    path("<int:pk>/", portfolios.portfolio_detail, name="portfolio_detail"),
    path("rules/", rules.index, name="rule_index"),
    path("rules/create", rules.create, name='new_rule'),
    path("rules/edit", rules.edit, name='edit_rule'),
    path("rules/delete/<int:pk>", rules.delete, name='delete_rule')
]