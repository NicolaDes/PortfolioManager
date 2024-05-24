from django.urls import path

from expenses.views import home
from expenses.views import portfolios
from expenses.views import rules
from expenses.views import categories
from expenses.views import transactions

urlpatterns = [
    path("", home.home, name="home"),
    path("<int:pk>/", portfolios.portfolio_detail, name="portfolio_detail"),
    path("rules/", rules.index, name="rule_index"),
    path("rules/delete/<int:pk>", rules.delete, name='delete_rule'),
    path("transactions/delete/<int:pk>", transactions.delete, name='transaction_delete'),
    path("categories/", categories.index, name='category_index'),
    path("categories/delete/<int:pk>", categories.delete, name='delete_category'),
    path("<int:pk>/rules", portfolios.portfolio_rules, name="portfolio_rules"),
    path("rules/create", rules.create, name='new_rule'),
    path("rules/edit", rules.edit, name='edit_rule'),
    path("categories/create", categories.create, name='new_category'),
    path("categories/edit", categories.edit, name='edit_category'),
    path("rules/assign", portfolios.portfolio_assign_rules, name="portfolio_assign_rules"),
    path("transactions/edit", transactions.edit, name="transaction_edit"),
    path("<int:pk>/analytics/<int:year>", portfolios.analytics, name="portfolio_analytics"),
    path("<int:pk>/report/<int:year>/<int:month>", portfolios.report, name="portfolio_report")
]