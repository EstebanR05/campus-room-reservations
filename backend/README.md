# Backend - FastAPI

API REST en Python para el sistema de reservas de salas por facultad.

## Requisitos

- Python 3.10+
- MongoDB en `mongodb://localhost:27017`
- Base de datos `base_datos_docu` cargada (semillas)

## Ejecutar

```bash
cd /home/estebanr/projects/campus-room-reservations/backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Swagger:

- http://127.0.0.1:8000/docs

## Reglas de negocio implementadas

- Reservas en horario institucional: 07:00 a 21:30.
- Sin solapamiento de reservas activas/ajustadas para la misma sala.
- Docente: reserva en su facultad y cancela solo sus reservas.
- Secretaria: reserva/ajusta en su facultad.
- Trazabilidad en `registrosModificaciones` para cancelaciones, ajustes y cambio de estado de sala.

## Endpoints principales

- `GET /health`
- `GET /facultades`
- `GET/POST /usuarios`
- `PATCH /usuarios/{usuario_id}/estado`
- `GET/POST /salas`
- `PATCH /salas/{sala_id}/estado` (requiere header `X-User-Id`)
- `GET/POST /reservas` (POST requiere header `X-User-Id`)
- `PATCH /reservas/{reserva_id}/cancelar` (header `X-User-Id`)
- `PATCH /reservas/{reserva_id}/ajustar` (header `X-User-Id`)
- `GET /auditoria`
