import os
from dotenv import load_dotenv

load_dotenv()


def get_db_url(env: str) -> str:
    if env == "production":
        return os.getenv("DATABASE_URL_PROD")

    return os.getenv("DATABASE_URL_DEV")


BASE_HOSTNAME = "http://host.docker.internal"

services_hostnames = {
    "parameters": {
        "development": BASE_HOSTNAME + ":5200/api/v1",
        "testing": BASE_HOSTNAME + ":5195/api/v1",
        "production": BASE_HOSTNAME + ":5105/api/v1",
    },
    "users": {
        "development": BASE_HOSTNAME + ":5500/api/v1",
        "testing": BASE_HOSTNAME + ":5192/api/v1",
        "production": BASE_HOSTNAME + ":5102/api/v1",
    },
    "employees": {
        "development": BASE_HOSTNAME + ":8000/api/v1",
        "testing": BASE_HOSTNAME + ":5192/api/v1",
        "production": BASE_HOSTNAME + ":5104/api/v1",
    },
    "business": {
        "development": BASE_HOSTNAME + "/api/v1",
        "testing": BASE_HOSTNAME + ":5192/api/v1",
        "production": BASE_HOSTNAME + ":5103/api/v1",
    },
    "courses": {
        "development": BASE_HOSTNAME + ":5192/api/v1",
        "testing": BASE_HOSTNAME + ":5199/api/v1",
        "production": BASE_HOSTNAME + ":5109/api/v1",
    }
}

ENV = os.getenv("ENV")

DATABASE_URL = get_db_url(ENV)

SERVICES = {
    "parameters": services_hostnames["parameters"][ENV],
    "users": services_hostnames["users"][ENV],
    "employees": services_hostnames["employees"][ENV],
    "business": services_hostnames["business"][ENV],
    "courses": services_hostnames["courses"][ENV],
}
