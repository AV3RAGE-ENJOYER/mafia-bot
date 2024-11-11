# Magfia and Minefia source code

## Configuration

You need to create a **config.env** file with all variables passed.

## Installation

```bash
docker build ./bot -t magfia_bot:v1
docker build ./migrations -t mafia_migrations:v1
docker build ./prometheus -t mafia_prometheus_metrics:v1
docker compose up -d
```