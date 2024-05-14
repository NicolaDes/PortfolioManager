docker exec -it portfolio python manage.py dumpdata portfolios.Asset --indent 2 > backups/portfolio/assets.json
docker exec -it portfolio python manage.py dumpdata portfolios.Portfolio --indent 2 > backups/portfolio/portfolios.json
docker exec -it portfolio python manage.py dumpdata portfolios.AssetInPortfolio --indent 2 > backups/portfolio/aips.json