# Prueba Técnica: To‑Do List (FastAPI + React + MongoDB)
Este entregable incluye backend REST con FastAPI, 
frontend en React, pruebas unitarias, 
justificación de arquitectura y un docker-compose opcional 
para levantar MongoDB y el backend rápidamente.
### Estructura del proyecto
```bash
├── backend/
│ ├── app/
│ │ ├── main.py
│ │ ├── db.py
│ │ ├── repositories.py
│ │ ├── schemas.py
│ │ ├── routes.py
│ │ └── utils.py
│ ├── tests/
│ │ └── test_tasks.py
│ ├── requirements.txt
│ └── Dockerfile
├── docker-compose.yml
└── frontend/
├── src/
│ ├── App.jsx
│ └── api.js
├── index.html
├── package.json
└── vite.config.js
```

### Por qué MongoDB (NoSQL) para este caso

* Modelo de datos simple y flexible: tareas con pocos campos (documentos). No requiere JOINS ni transacciones complejas.

* Escalabilidad horizontal y escritura rápida: ideal si el volumen de tareas crece.

* Esquema evolutivo: permite agregar campos (etiquetas, sub-tareas) sin migraciones rígidas.

### Patrón y capas

* API (FastAPI): capa de transporte HTTP (endpoints + validación Pydantic).

* Dominio/Modelos: schemas.py define contratos de entrada/salida y validaciones.

* Repositorio: interfaz TaskRepository y dos implementaciones: MongoTaskRepository (producción) e InMemoryTaskRepository (tests). Esto separa persistencia de la lógica de aplicación.

* Frontend (React): UI desacoplada que consume la API vía fetch (archivo api.js). Estado con useState/useEffect.


### Ejecutar tests:
```bash
 pytest -v
```