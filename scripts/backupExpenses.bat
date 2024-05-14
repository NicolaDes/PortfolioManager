docker exec -it expenses python manage.py dumpdata expenses.Portfolio --indent 2 > backups/expenses/portfolios.json
docker exec -it expenses python manage.py dumpdata expenses.Category --indent 2 > backups/expenses/categories.json
docker exec -it expenses python manage.py dumpdata expenses.Transaction --indent 2 > backups/expenses/transactions.json
docker exec -it expenses python manage.py dumpdata expenses.Rule --indent 2 > backups/expenses/rules.json
docker exec -it expenses python manage.py dumpdata expenses.RuleInPortfolio --indent 2 > backups/expenses/rips.json