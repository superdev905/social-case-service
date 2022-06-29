#/bin/bash!
docker context use default
docker-compose --file docker-compose.image.yml up --build
docker tag social-case-service_social-case-api cchcprod.azurecr.io/social-case-service-prod:latest
docker push cchcprod.azurecr.io/social-case-service-prod:latest
#az acr login --name  cchcprod
docker context use azureprod
docker compose --file docker-compose.prod.yml up --build