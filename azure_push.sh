#/bin/bash!
docker context use default
docker-compose --file docker-compose.image.yml up --build
docker tag social-case-service_social-case-api cchcdev.azurecr.io/social-case-service-prod:latest
docker push cchcdev.azurecr.io/social-case-service-prod:latest
docker context use azureprod
docker compose --file docker-compose.prod.yml up --build