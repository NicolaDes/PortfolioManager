docker exec -it expenses python manage.py reset_db --no-input

docker exec -it expenses python manage.py migrate

docker cp backups/expenses expenses:/app/genesis

docker exec -it expenses python manage.py loaddata /app/genesis/expenses/portfolios.json
docker exec -it expenses python manage.py loaddata /app/genesis/expenses/categories.json
docker exec -it expenses python manage.py loaddata /app/genesis/expenses/transactions.json
docker exec -it expenses python manage.py loaddata /app/genesis/expenses/rules.json
docker exec -it expenses python manage.py loaddata /app/genesis/expenses/rips.json

docker exec -it expenses /bin/bash -c "rm -rf /app/genesis/expenses"