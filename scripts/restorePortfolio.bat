docker exec -it portfolio python manage.py reset_db --no-input

docker exec -it portfolio python manage.py migrate

docker cp backups/portfolio portfolio:/app/genesis
docker exec -it portfolio python manage.py loaddata /app/genesis/portfolio/portfolios.json
docker exec -it portfolio python manage.py loaddata /app/genesis/portfolio/assets.json
docker exec -it portfolio python manage.py loaddata /app/genesis/portfolio/aips.json

docker exec -it portfolio /bin/bash -c "rm -rf /app/genesis/portfolio"