# Frontend - Campus Room Reservations

Frontend en React + Tailwind para consumir el backend FastAPI.

## Requisitos

- Node 20+
- Backend corriendo en `http://127.0.0.1:8000`

## Configuracion

```bash
cd /home/estebanr/projects/campus-room-reservations/frontend
cp .env.example .env
npm install
```

Variable:

- `VITE_API_BASE_URL`: URL base del backend.

## Ejecucion

```bash
npm run dev
```

## Arquitectura de servicios

- `src/services/baseService.js`: unico punto de `fetch`.
- `src/services/facultadesService.js`
- `src/services/usuariosService.js`
- `src/services/salasService.js`
- `src/services/reservasService.js`
- `src/services/auditoriaService.js`

Cada service extiende `BaseService` para centralizar manejo de URL, headers, query params, errores y parseo de respuestas.
