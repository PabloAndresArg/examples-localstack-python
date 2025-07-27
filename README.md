# examples-localstack-python

## Librerías necesarias para el proyecto

A continuación, se listan las librerías necesarias para ejecutar este proyecto:

### Librerías principales

- **FastAPI**: Framework para construir APIs rápidas y modernas.
- **Uvicorn**: Servidor ASGI para ejecutar aplicaciones FastAPI.
- **Boto3**: SDK de AWS para interactuar con servicios como S3 y DynamoDB.
- **Pydantic**: Para validación de datos y definición de esquemas.

### Comandos para instalar las librerías

Ejecuta los siguientes comandos en tu terminal para instalar las librerías necesarias:

````bash
pip install fastapi
pip install uvicorn
pip install boto3
pip install pydantic
````

## Image de Docker

```bash
docker pull localstack/localstack
docker run -d --name localstack -p 4566:4566 -p 4571:4571 localstack/localstack
```

## Comandos para levantar el proyecto en desarrollo

Sigue los pasos a continuación para iniciar el proyecto en modo desarrollo:

```bash
source /Users/pargueta/Desktop/PRUEBAS/.venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
