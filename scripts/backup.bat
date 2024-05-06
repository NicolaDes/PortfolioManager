docker exec -it portfolio python manage.py dumpdata portfolios.Asset --indent 2 > backup/assets.json
docker exec -it portfolio python manage.py dumpdata portfolios.Portfolio --indent 2 > backup/portfolios.json
docker exec -it portfolio python manage.py dumpdata portfolios.AssetInPortfolio --indent 2 > backup/aips.json