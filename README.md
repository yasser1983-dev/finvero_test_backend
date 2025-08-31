# Prueba Técnica: To‑Do List (FastAPI + React + MongoDB)
Este entregable incluye backend REST con FastAPI, 
frontend en React, pruebas unitarias, 
justificación de arquitectura y un docker-compose opcional 
para levantar MongoDB y el backend rápidamente.
### Estructura de los proyectos de Frontend y Backend
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
frontend/
├─ src/
│  ├─ api/           # para llamadas al backend
│  │   └─ tasks.js
│  ├─ components/
│  │   ├─ TaskList.jsx
│  │   ├─ TaskForm.jsx
│  ├─ App.jsx
│  └─ main.jsx
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

### Manejo de Rendimiento

* Paginación y filtrado en el backend. En lugar de devolver todas las tareas en una sola consulta, se implementó paginación (limit, offset) y filtros. 
Esto evita que el servidor y el frontend carguen miles de registros de golpe.

### Instalación y ejecuciòn con entorno virtual

1. Clonar el repositorio:
```bash
git clone <repo_url>
cd <repo_name>
```
2. Crear y activar un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows
```
3. Instalar dependencias del backend:
```bash
pip install -r backend/requirements.txt
```
4. Navegar al directorio del frontend e instalar dependencias:
```bash
cd frontend
npm install
```
5. Configurar variables de entorno (si es necesario). Crear un archivo `.env` en el directorio raíz del backend con la URL de conexión a MongoDB:
```
MONGO_URI=mongodb://localhost:27017
FRONTEND_ORIGIN=http://localhost:3000
```

6. Iniciar MongoDB usando docker-compose:
```bash
docker-compose up -d
```
7. Iniciar el backend:
```bash
cd ../backend
uvicorn app.main:app --reload
```
8. Iniciar el frontend:
```bash
cd ../frontend
npm run dev
```
9. Acceder a la aplicación en el navegador:
```bash
http://localhost:3000
```
