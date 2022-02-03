import os
from dotenv import load_dotenv

load_dotenv()


def get_db_url(env: str) -> str:
    if env == "production":
        return os.getenv("DATABASE_URL_PROD")

    return os.getenv("DATABASE_URL_DEV")


def get_env_prefix(env: str) -> str:
    if env == "production":
        return "PROD"
    if env == "testing":
        return "TEST"
    return "DEV"


ENV = os.getenv("ENV")

services_hostnames = {
    "assistance": os.getenv("ASSISTANCE_SERVICE_%s" % (get_env_prefix(ENV))) + "/api/v1",
    "users": os.getenv("AUTH_SERVICE_%s" % (get_env_prefix(ENV))) + "/api/v1",
    "benefits": os.getenv("BENEFITS_SERVICE_%s" % (get_env_prefix(ENV))) + "/api/v1",
    "business": os.getenv("BUSINESS_SERVICE_%s" % (get_env_prefix(ENV))) + "/api/v1",
    "cesantes": os.getenv("CESANTES_SERVICE_%s" % (get_env_prefix(ENV))) + "/api/v1",
    "consultas_web": os.getenv("CONSULTAS_WEB_SERVICE_%s" % (get_env_prefix(ENV))) + "/api/v1",
    "courses": os.getenv("CURSOS_SERVICE_%s" % (get_env_prefix(ENV))) + "/api/v1",
    "employees": os.getenv("EMPLOYEE_SERVICE_%s" % (get_env_prefix(ENV))) + "/api/v1",
    "inclusion": os.getenv("INCLUSION_SERVICE_%s" % (get_env_prefix(ENV))) + "/api/v1",
    "migrantes": os.getenv("MIGRANTES_SERVICE_%s" % (get_env_prefix(ENV))) + "/api/v1",
    "parameters": os.getenv("PARAMETERS_SERVICE_%s" % (get_env_prefix(ENV))) + "/api/v1",
    "poll": os.getenv("POLLS_SERVICE_%s" % (get_env_prefix(ENV))) + "/api/v1",
    "protocols": os.getenv("PROTOCOLS_SERVICE_%s" % (get_env_prefix(ENV))) + "/api/v1",
    "schedule": os.getenv("SCHEDULE_SERVICE_%s" % (get_env_prefix(ENV))) + "/api/v1",
    "scholarship": os.getenv("SCHOLARSHIP_SERVICE_%s" % (get_env_prefix(ENV))) + "/api/v1",
    "socialCase": os.getenv("SOCIAL_CASE_SERVICE_%s" % (get_env_prefix(ENV))) + "/api/v1",
    "vivienda": os.getenv("VIVIENDA_SERVICE_%s" % (get_env_prefix(ENV))) + "/api/v1",

}

DATABASE_URL = get_db_url(ENV)

SERVICES = {
    "parameters": services_hostnames["parameters"],
    "users": services_hostnames["users"],
    "employees": services_hostnames["employees"],
    "business": services_hostnames["business"],
    "courses": services_hostnames["courses"],
    "housing": services_hostnames["vivienda"],
    "assistance": services_hostnames["assistance"],
}
