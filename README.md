
# API de Tareas (TODOs) - Prueba Técnica

Esta es una solución para la prueba técnica de **Programador Backend**.  
Se ha desarrollado una **API REST** utilizando **FastAPI** y **PostgreSQL** para administrar una lista de tareas (**TODOs**), siguiendo todos los requerimientos y considerando las problemáticas adicionales propuestas.

---

## ✨ Características Principales

- **Stack Tecnológico**: FastAPI, PostgreSQL, SQLAlchemy, Pydantic, Alembic.  
- **Asíncrono**: Toda la API, incluyendo las interacciones con la base de datos, es completamente asíncrona para un alto rendimiento.  
- **Autenticación**: Sistema robusto basado en tokens JWT (JSON Web Tokens).  
- **Seguridad**: Cada usuario solo puede acceder y gestionar sus propias tareas.  
- **Manejo de Datos**: Paginación para manejar grandes volúmenes de tareas de manera eficiente.  
- **Contenerización**: Proyecto dockerizado con Docker Compose para un despliegue y desarrollo sencillos.  
- **Migraciones**: Alembic para gestionar las migraciones del esquema de la base de datos.  
- **Testing**: Conjunto de tests automatizados con `pytest` para garantizar la fiabilidad del código.  
- **Logging**: Sistema de logging configurado para monitorizar errores y eventos importantes.  

---

## 🚀 Cómo Correr el Proyecto

### 📋 Pre-requisitos
- Tener instalado **Docker** y **Docker Compose**.

### 🔧 Instrucciones de Levantamiento

1. Clona el repositorio:

```bash
git clone https://github.com/alejandrofonsecacuza/TODO-Technical-test.git
cd TODO-Technical-test
````

2. Crea un archivo de entorno:

```bash
cp .env.example .env
```

3. Levanta los servicios con Docker Compose:

```bash
docker-compose up -d --build
```

La API estará disponible en **[http://localhost:8000](http://localhost:8000)**.

---

## 📖 Documentación Interactiva

Una vez que la API está corriendo, puedes acceder a la documentación generada por FastAPI:

* **Swagger UI** → [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc** → [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## ⚙️ Ejemplos de Uso de los Endpoints

### 1. Registrar un nuevo usuario

```bash
curl -X POST "http://localhost:8000/users/register" \
-H "Content-Type: application/json" \
-d '{
  "email": "user@example.com",
  "password": "a_strong_password"
}'
```

---

### 2. Obtener un Token de Acceso (Login)

```bash
curl -X POST "http://localhost:8000/users/login" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=user@example.com&password=a_strong_password"
```

**Respuesta:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR...",
  "token_type": "bearer"
}
```

> 💡 Guarda el `access_token` para usarlo en las siguientes peticiones.

---

### 3. Crear una Nueva Tarea

```bash
curl -X POST "http://localhost:8000/tasks/" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
-H "Content-Type: application/json" \
-d '{
  "title": "Mi primera tarea",
  "description": "Descripción de la tarea."
}'
```

---

### 4. Listar Todas las Tareas del Usuario

```bash
curl -X GET "http://localhost:8000/tasks/" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### 5. Obtener una Tarea Específica

```bash
curl -X GET "http://localhost:8000/tasks/{task_id}" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### 6. Actualizar una Tarea

```bash
curl -X PUT "http://localhost:8000/tasks/{task_id}" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
-H "Content-Type: application/json" \
-d '{
  "title": "Título actualizado",
  "description": "Descripción actualizada",
  "status": "completed"
}'
```

---

### 7. Eliminar una Tarea

```bash
curl -X DELETE "http://localhost:8000/tasks/{task_id}" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🧪 Cómo Correr los Tests

Ejecuta los tests automatizados con:

```bash
docker-compose exec web pytest
```

---

## 🏛️ Decisiones de Diseño y Arquitectura

### ✅ Resolución de Problemáticas Adicionales

**Alta Concurrencia**

* Uso de **FastAPI** (asíncrono) para manejar múltiples peticiones concurrentes sin bloqueo.
* Conexión a PostgreSQL con **asyncpg**, el driver asíncrono más rápido para Python.

**Grandes Volúmenes de Datos**

* Paginación en `GET /tasks/` con parámetros `skip` y `limit`.
* Índices en `user_id` de la tabla de tareas para mejorar rendimiento en consultas.

**Escenarios de Error**

* Validación con **Pydantic** → errores 422 con mensajes claros.
* Manejo explícito de errores → 404 cuando una tarea no existe para el usuario.

**Seguridad**

* Autenticación con **JWT**.
* Aislamiento de datos → un usuario solo accede a sus propias tareas.

---

## 📂 Estructura del Proyecto


```markdown
.
├── alembic/               # Archivos de migración de Alembic
├── app/                   # Directorio principal de la aplicación
│   ├── core/              # Configuración de la aplicación (settings, utils)
│   ├── db/                # Conexión y modelos de base de datos
│   │   ├── models/        # Definición de modelos ORM (SQLAlchemy)
│   │   ├── session.py     # Configuración de la sesión/engine
│   │   └── base.py        # Base declarativa de SQLAlchemy
│   ├── dependens/         # Dependencias de seguridad y DB (FastAPI Depends)
│   ├── api/               # Routers de la API (endpoints)
│   │   └── v1/            # Versión 1 de la API con submódulos de rutas
│   ├── schemas/           # Esquemas Pydantic para validación
│   └── main.py            # Punto de entrada de la aplicación
├── tests/                 # Tests automatizados (pytest)
├── .env                   # Variables de entorno
├── .env.example           # Ejemplo de variables de entorno
├── docker-compose.yml     # Orquestación de servicios Docker
├── openapi.json           # Especificación OpenAPI exportada
├── requirements.txt       # Dependencias del proyecto
├── Dockerfile             # Definición del contenedor de la API
└── README.md              # Documentación principal

```



