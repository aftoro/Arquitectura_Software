# Arquitectura Software - Taller 02

Este repositorio implementa una evolucion del monolito Django aplicando Strangler Pattern.

## Objetivo de migracion
Se extrajo una funcionalidad de negocio a un microservicio Flask:
- Ruta nueva: /api/v2/funcionalidad
- Rutas existentes del monolito: /api/v1/*

Nginx enruta por URL para permitir coexistencia progresiva.

## Ejecucion local (sin Docker)
1. Activar entorno virtual.
2. Instalar dependencias:
   - pip install -r requirements.txt
3. Ejecutar Django:
   - python manage.py migrate
   - python manage.py runserver

## Ejecucion con Docker
1. Levantar servicios:
   - docker compose up --build
2. Probar rutas:
   - Django v1 via Nginx: http://localhost:8080/api/v1/clientes/
   - Flask v2 via Nginx: http://localhost:8080/api/v2/funcionalidad

## Ejemplo de request al microservicio Flask
POST /api/v2/funcionalidad
Body JSON:
{
  "precio_base": 25000,
  "tipo": "premium"
}

Respuesta esperada:
{
  "mensaje": "Cotizacion calculada",
  "tipo": "premium",
  "precio_base": 25000.0,
  "total": 33750.0
}

## Estructura agregada para la migracion
- flask_service/app.py
- flask_service/Dockerfile
- flask_service/requirements.txt
- nginx/nginx.conf
- docker-compose.yml
- Dockerfile
- citas/api_v1_urls.py
