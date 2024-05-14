docker exec -it expenses python manage.py reset_db --no-input

docker exec -it expenses python manage.py migrate

docker cp backups/expenses expenses:/app/genesis

docker exec -it expenses python manage.py loaddata /app/genesis/portfolios.json
docker exec -it expenses python manage.py loaddata /app/genesis/categories.json
docker exec -it expenses python manage.py loaddata /app/genesis/transactions.json
docker exec -it expenses python manage.py loaddata /app/genesis/rules.json
docker exec -it expenses python manage.py loaddata /app/genesis/rips.json

docker exec -it expenses /bin/bash -c "rm -rf /app/genesis"