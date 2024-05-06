docker exec -it portfolio python manage.py reset_db --no-input

docker exec -it portfolio python manage.py migrate

docker cp backup portfolio:/app/genesis
docker exec -it portfolio python manage.py loaddata /app/genesis/backup/portfolios.json
docker exec -it portfolio python manage.py loaddata /app/genesis/backup/assets.json
docker exec -it portfolio python manage.py loaddata /app/genesis/backup/aips.json

docker exec -it portfolio /bin/bash -c "rm -rf /app/genesis/backup"