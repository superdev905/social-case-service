#/bin/bash!
docker context use default
docker-compose --file docker-compose.test.yml up --build
docker tag social-case-service_social-case-api-test cchcdev.azurecr.io/social-case-service:latest
docker push cchcdev.azurecr.io/social-case-service:latest
docker context use azurecontext
docker compose --file docker-compose.azure.yml up --build