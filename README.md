
# 🧩 Proyecto FastAPI - Gestión de Usuarios

Este proyecto es una API RESTful construida con **FastAPI**, diseñada para manejar la gestión de usuarios con autenticación JWT, control de roles y una arquitectura limpia y modular.

---

## 🚀 Tecnologías utilizadas

- **FastAPI**: Framework web moderno y rápido.
- **SQLAlchemy**: ORM para interacción con base de datos.
- **Alembic**: Migraciones de base de datos.
- **MySQL**: Motor de base de datos.
- **Pydantic**: Validación de datos.
- **dotenv**: Carga de configuración desde `.env`.

---

## 📂 Estructura del Proyecto

```
app/
├── api/               # Rutas organizadas por versiones
├── core/              # Utilidades, validaciones y seguridad
├── exceptions/        # Manejo personalizado de errores
├── models/            # Modelos ORM (SQLAlchemy)
├── repositories/      # Acceso a base de datos (repositorios)
├── schemas/           # Esquemas de validación Pydantic
├── services/          # Lógica de negocio
├── config.py          # Configuración del entorno
├── database.py        # Conexión a la base de datos
└── main.py            # Punto de entrada de la app FastAPI
```

---
## 📝 Configuracion inicial venv

Crear entorno virtual venv en linux
```bash
python3 -m venv venv
```
Activar entorno virtual venv en linux
```bash
source venv/bin/activate
```

Crear entorno virtual venv en windows
```bash
python -m venv venv
```
Activar entorno virtual venv en windows
```bash
venv\Scripts\activate
```





---

## 🔐 Autenticación

- Login con usuario y contraseña.
- Tokens JWT generados y almacenados en base de datos.
- Solo se permite un token activo por usuario.
- Control de acceso por roles: `admin` y `user`.

---

## 🛠️ Migraciones con Alembic

Ya está configurado con una migración inicial:

```bash
alembic upgrade head  # Aplica migraciones
```

Para crear nuevas migraciones:

```bash
alembic revision --autogenerate -m "mensaje"
```

---

## ⚙️ Variables de Entorno

Define un archivo `.env` con lo siguiente:

```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=tu_usuario
MYSQL_PASSWORD=tu_password
MYSQL_DB=tu_base_datos
TIMEZONE=America/Mexico_City
SECRET_KEY=clave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## ▶️ Ejecutar el proyecto

Instala dependencias:

```bash
pip install -r requirements.txt
```

Ejecuta el servidor:

```bash
uvicorn app.main:app --reload
```

---

## 📫 API disponible

Una vez levantado el servidor, accede a:

- Documentación automática: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## ✅ Estado actual

✅ CRUD de usuarios  
✅ Autenticación con JWT  
✅ Sistema de roles  
✅ Validaciones personalizadas  
✅ Migraciones listas  

---

## 📌 Próximos pasos sugeridos

- Implementar endpoints para ingresos y egresos.
- Panel de administración.
- Sistema de notificaciones o reportes financieros.

---

## 🧑 Autor

Desarrollado por Ivan Melo.