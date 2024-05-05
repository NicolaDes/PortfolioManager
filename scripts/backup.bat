docker exec -it portfolio python manage.py dumpdata portfolios.Asset > backup/assets.json
docker exec -it portfolio python manage.py dumpdata portfolios.Portfolio > backup/portfolios.json
docker exec -it portfolio python manage.py dumpdata portfolios.AssetInPortfolio > backup/aips.json

pause