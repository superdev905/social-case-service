# Servicio de Casos sociales

## Running migrations

Running new migration

```bash
alembic revision --autogenerate -m "Migration name"
```

Undo last migration

```bash
alembic downgrade -1
```

Updating migrations

```bash
alembic upgrade head
```
