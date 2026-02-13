# 🛍️ Tienda Kalyzo

Plataforma de comercio electrónico desarrollada con **Django 5.2**, desplegada en **Render** con almacenamiento de medios en **AWS S3** y base de datos **PostgreSQL** en producción.

🌐 **Demo en vivo:** [https://kalyzo.shop](https://kalyzo.shop)

---

## 📋 Tabla de contenidos

- [Tecnologías](#-tecnologías)
- [Arquitectura del proyecto](#-arquitectura-del-proyecto)
- [Requisitos previos](#-requisitos-previos)
- [Instalación local](#-instalación-local)
- [Variables de entorno](#-variables-de-entorno)
- [Base de datos](#-base-de-datos)
- [AWS S3 - Archivos multimedia](#-aws-s3---archivos-multimedia)
- [Despliegue en Render](#-despliegue-en-render)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Apps del proyecto](#-apps-del-proyecto)

---

## 🚀 Tecnologías

| Tecnología | Uso |
|------------|-----|
| Django 5.2.8 | Framework principal |
| Python 3.13 | Lenguaje de programación |
| MySQL | Base de datos en desarrollo local |
| PostgreSQL | Base de datos en producción (Render) |
| AWS S3 | Almacenamiento de imágenes y archivos multimedia |
| Gunicorn | Servidor WSGI en producción |
| WhiteNoise | Archivos estáticos en producción |
| django-storages | Integración con AWS S3 |
| dj-database-url | Configuración de base de datos por URL |

---

## 🏗️ Arquitectura del proyecto

```
Local (Desarrollo)          Producción (Render)
─────────────────           ───────────────────
Django + MySQL         →    Django + PostgreSQL
Archivos locales       →    AWS S3 (imágenes)
Django dev server      →    Gunicorn
Archivos estáticos     →    WhiteNoise
```

---

## ✅ Requisitos previos

- Python 3.13+
- MySQL (para desarrollo local)
- Cuenta en AWS (para S3)
- Cuenta en Render (para despliegue)
- Git

---

## 💻 Instalación local

### 1. Clonar el repositorio

```bash
git clone https://github.com/mejiatian98/Tienda-Kalyzo.git
cd Tienda-Kalyzo
git checkout SebasTK98
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto (ver sección [Variables de entorno](#-variables-de-entorno)).

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

Abre tu navegador en [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔐 Variables de entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# ── Django ──────────────────────────────────────
SECRET_KEY=tu_secret_key_muy_segura_aqui
DEBUG=True

# ── Base de datos local (MySQL) ──────────────────
DB_NAME=nombre_base_de_datos
DB_USER=usuario_mysql
DB_PASSWORD=contraseña_mysql
DB_HOST=localhost
DB_PORT=3306

# ── AWS S3 (solo necesario en producción) ────────
# AWS_ACCESS_KEY_ID=tu_access_key_id
# AWS_SECRET_ACCESS_KEY=tu_secret_access_key
# AWS_STORAGE_BUCKET_NAME=kalyzo-tienda
# AWS_S3_REGION_NAME=us-east-2
```

> ⚠️ **Importante:** Nunca subas el archivo `.env` a Git. Ya está incluido en `.gitignore`.

### Variables de entorno en producción (Render)

Configura estas variables en **Render → Environment**:

| Variable | Descripción |
|----------|-------------|
| `SECRET_KEY` | Clave secreta de Django |
| `DEBUG` | `False` en producción |
| `DATABASE_URL` | Automático (proporcionado por Render) |
| `RENDER_EXTERNAL_HOSTNAME` | Automático (proporcionado por Render) |
| `AWS_ACCESS_KEY_ID` | Credencial de AWS |
| `AWS_SECRET_ACCESS_KEY` | Credencial secreta de AWS |
| `AWS_STORAGE_BUCKET_NAME` | Nombre del bucket S3 |
| `AWS_S3_REGION_NAME` | Región de AWS (ej: `us-east-2`) |

---

## 🗄️ Base de datos

El proyecto usa **dos bases de datos** según el entorno:

### Desarrollo local — MySQL

```python
# Configuración automática en settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
```

### Producción — PostgreSQL (Render)

```python
# Configuración automática usando DATABASE_URL de Render
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}
```

---

## ☁️ AWS S3 - Archivos multimedia

Las imágenes de productos y otros archivos multimedia se almacenan en **AWS S3** en producción.

### Configuración del bucket

1. Crea un bucket en S3 llamado `kalyzo-tienda` en la región `us-east-2`
2. Desactiva el "Block Public Access" en el bucket
3. Aplica la siguiente política de bucket:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowPublicRead",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::kalyzo-tienda/*"
    }
  ]
}
```

### Permisos IAM recomendados

Crea un usuario IAM con los siguientes permisos mínimos:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::kalyzo-tienda",
        "arn:aws:s3:::kalyzo-tienda/*"
      ]
    }
  ]
}
```

---

## 🚀 Despliegue en Render

### Archivos necesarios

#### `build.sh`

```bash
#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --no-input
```

> Recuerda dar permisos de ejecución: `chmod +x build.sh`

#### Configuración en Render Dashboard

| Campo | Valor |
|-------|-------|
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn tienda_kalyzo.wsgi:application --bind 0.0.0.0:$PORT` |
| **Python Version** | `3.13.5` |

### Dominio personalizado

El proyecto está configurado para funcionar con el dominio `kalyzo.shop`. Para conectar tu propio dominio:

1. Ve a **Render → Settings → Custom Domains**
2. Agrega tu dominio
3. Configura los registros DNS en tu proveedor:

| Tipo | Host | Valor |
|------|------|-------|
| A | @ | `216.24.57.1` |
| CNAME | www | `tienda-kalyzo.onrender.com` |

---

## 📁 Estructura del proyecto

```
Tienda-Kalyzo/
│
├── tienda_kalyzo/              # Configuración principal del proyecto
│   ├── settings.py             # Configuración de Django
│   ├── urls.py                 # URLs principales
│   ├── wsgi.py                 # Servidor WSGI
│   └── asgi.py                 # Servidor ASGI
│
├── app_store/                  # App principal de la tienda
│   ├── templates/
│   │   └── app_store/          # Templates de la tienda
│   ├── views.py
│   ├── urls.py
│   ├── models.py
│   └── context_processors.py
│
├── app_products/               # Gestión de productos
│   ├── templates/
│   │   └── app_products/
│   ├── views.py
│   ├── urls.py
│   └── models.py
│
├── app_customers/              # Gestión de clientes
│   ├── templates/
│   │   └── app_customers/
│   ├── views.py
│   ├── urls.py
│   └── models.py
│
├── app_orders/                 # Gestión de pedidos
│   ├── templates/
│   │   └── app_orders/
│   ├── views.py
│   ├── urls.py
│   └── models.py
│
├── static/                     # Archivos estáticos globales
├── staticfiles/                # Archivos estáticos compilados (generado)
├── requirements.txt            # Dependencias del proyecto
├── build.sh                    # Script de build para Render
├── manage.py
└── .env                        # Variables de entorno (NO subir a Git)
```

---

## 📦 Apps del proyecto

### `app_store`
Página principal de la tienda. Incluye vistas para la página de inicio, categorías, búsqueda de productos, productos destacados, productos con descuento, productos más vendidos y más nuevos.

### `app_products`
Gestión del catálogo de productos. Maneja modelos de `Product`, `Category`, `ProductVariant` e imágenes de variantes.

### `app_customers`
Gestión de clientes y autenticación. Registro, login y perfil de usuario.

### `app_orders`
Gestión de pedidos y carrito de compras. Proceso de checkout y historial de órdenes.

---

## 📦 Dependencias principales

```
Django==5.2.8
boto3==1.42.21
django-storages==1.14.6
dj-database-url==3.1.0
psycopg2-binary==2.9.10
mysqlclient==2.2.7
gunicorn==23.0.0
whitenoise==6.8.2
pillow==12.0.0
python-decouple==3.8
python-dotenv==1.2.1
```

---

## ⚠️ Notas importantes

- **Case sensitivity:** Linux distingue mayúsculas/minúsculas en nombres de archivos. Asegúrate de que los nombres de los templates en los `views.py` coincidan exactamente con los nombres de los archivos HTML.
- **Templates:** Deben estar en `app_name/templates/app_name/nombre.html` y referenciarse como `"app_name/nombre.html"` en los views.
- **Archivos estáticos:** En producción se sirven con WhiteNoise. Ejecuta `collectstatic` antes del despliegue.
- **Migraciones:** Se ejecutan automáticamente en el `build.sh` al desplegar en Render.

---

## 👨‍💻 Autor

Desarrollado por el equipo de **Kalyzo** 🛍️

---

*Documentación actualizada: Febrero 2026*
