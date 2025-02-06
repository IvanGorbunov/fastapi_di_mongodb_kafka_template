# FastAPI DI + MongoDB + Kafka template


## Installation:

```bash
docker compose -f ./docker-compose.yml up --detach --build
```

## Endpoints:

- Kafka: http://127.0.0.1:18080/
- FastAPI service:
  - documentation: http://127.0.0.1:18000/redoc
  - documentation: http://127.0.0.1:18000/docs
  - send message: http://127.0.0.1:18000/start
  - get messages: http://127.0.0.1:18000/messages