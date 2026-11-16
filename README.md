# EventPass - API Gateway

## Equipo 06 - Desarrollo Web y Móvil

## 1. Descripción del proyecto

EventPass API Gateway es un servicio intermediario desarrollado con FastAPI y HTTPX, cuya función principal es centralizar la comunicación entre las aplicaciones cliente y los diferentes servicios del sistema EventPass.

El Gateway funciona como un único punto de acceso para la web de ventas, el panel administrativo y la aplicación móvil (APK), permitiendo que las solicitudes sean dirigidas automáticamente a la API correspondiente.

Su objetivo es facilitar la comunicación entre los distintos componentes del sistema, sin modificar las reglas de negocio de los servicios internos.

## 2. Objetivos

- Centralizar las solicitudes de las aplicaciones cliente.
- Enrutar las peticiones HTTP hacia los servicios correspondientes.
- Reenviar los métodos HTTP, parámetros, encabezados y cuerpos de las solicitudes.
- Conservar los códigos de estado y las respuestas originales de las APIs.
- Configurar las direcciones de los servicios mediante variables de entorno.
- Implementar CORS para permitir la comunicación con aplicaciones Angular.
- Gestionar errores de conexión mediante respuestas HTTP 502.
- Proporcionar un endpoint para comprobar el estado del servicio.

## 3. Tecnologías utilizadas

| Tecnología    | Descripción                               |
| ------------- | ----------------------------------------- |
| Python        | Lenguaje de programación                  |
| FastAPI       | Framework para desarrollar la API Gateway |
| HTTPX         | Cliente HTTP para comunicar los servicios |
| Uvicorn       | Servidor ASGI                             |
| Python-dotenv | Gestión de variables de entorno           |
| Git           | Control de versiones                      |
| GitHub        | Repositorio del proyecto                  |
| Railway       | Plataforma de despliegue                  |

## 4. Arquitectura del sistema

El API Gateway recibe las solicitudes de los clientes y las redirige al servicio correspondiente.

Flujo de comunicación:

1. La aplicación cliente realiza una solicitud al API Gateway.
2. El Gateway identifica el servicio de destino mediante la ruta.
3. HTTPX reenvía la solicitud a la API correspondiente.
4. El servicio interno procesa la solicitud.
5. El Gateway devuelve al cliente la respuesta recibida.

### Servicios conectados

| Equipo   | Servicio    | Ruta               |
| -------- | ----------- | ------------------ |
| Equipo 4 | Eventos     | `/api/eventos`     |
| Equipo 5 | Entradas    | `/api/entradas`    |
| Equipo 7 | Tickets     | `/api/tickets`     |
| Equipo 8 | Impresiones | `/api/impresiones` |

El prefijo `/api` se elimina al reenviar las solicitudes a los servicios internos.

## 5. Estructura del proyecto

```text
EventPass-Gateway/
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
│
└── docs/
    └── secuencia.puml
```

### Descripción de archivos

- `main.py`: contiene la aplicación FastAPI y la lógica de enrutamiento.
- `.env`: almacena las URL de los servicios internos.
- `.gitignore`: evita subir archivos privados y temporales.
- `requirements.txt`: contiene las dependencias necesarias.
- `docs/secuencia.puml`: contiene el diagrama UML de secuencia.

## 6. Requisitos previos

Para ejecutar el proyecto localmente se necesita:

- Python 3.10 o superior.
- Visual Studio Code.
- Git.
- Conexión a Internet para acceder a los servicios desplegados.

## 7. Instalación y ejecución

### 7.1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
```

### 7.2. Entrar a la carpeta del proyecto

```bash
cd EventPass-Gateway
```

### 7.3. Crear un entorno virtual

```bash
python -m venv venv
```

### 7.4. Activar el entorno virtual

En Windows:

```bash
venv\Scripts\activate
```

En Linux o macOS:

```bash
source venv/bin/activate
```

### 7.5. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 7.6. Configurar las variables de entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
EVENTOS_URL=https://url-del-equipo-4
ENTRADAS_URL=https://url-del-equipo-5
TICKETS_URL=https://url-del-equipo-7
IMPRESION_URL=https://url-del-equipo-8
```

Reemplazar las direcciones de ejemplo por las URL reales proporcionadas por cada equipo.

### 7.7. Ejecutar el servidor

```bash
uvicorn main:app --reload
```

El servidor estará disponible en:

```text
http://127.0.0.1:8000
```

## 8. Endpoints disponibles

### Comprobación del servicio

| Método | Endpoint  | Descripción                           |
| ------ | --------- | ------------------------------------- |
| GET    | `/health` | Comprueba que el Gateway esté activo. |

Respuesta esperada:

```json
{
  "status": "ok"
}
```

### Enrutamiento de servicios

| Método | Endpoint del Gateway             | Servicio de destino          |
| ------ | -------------------------------- | ---------------------------- |
| GET    | `/api/eventos`                   | `/eventos`                   |
| POST   | `/api/entradas`                  | `/entradas`                  |
| POST   | `/api/entradas/{codigo}/validar` | `/entradas/{codigo}/validar` |
| GET    | `/api/tickets/{codigo}`          | `/tickets/{codigo}`          |
| POST   | `/api/impresiones`               | `/impresiones`               |

Las rutas adicionales bajo cada prefijo también son reenviadas al servicio correspondiente.

## 9. Gestión de respuestas y errores

El Gateway conserva el código HTTP y el contenido de las respuestas recibidas desde los servicios internos.

| Situación                 | Respuesta                        |
| ------------------------- | -------------------------------- |
| Solicitud exitosa         | Conserva el código HTTP original |
| Conflicto de solicitud    | HTTP 409                         |
| Compra de entrada exitosa | HTTP 201                         |
| Servicio no disponible    | HTTP 502                         |
| Gateway activo            | HTTP 200                         |

### Ejemplo de compra exitosa

Solicitud:

```http
POST /api/entradas
```

Cuerpo:

```json
{
  "evento_id": 1
}
```

Respuesta:

```json
{
  "codigo": "EP-A1B2C3D4",
  "evento_id": 1,
  "estado": "EMITIDA"
}
```

El Gateway devuelve el mismo código HTTP 201 y el mismo contenido recibido desde la API de entradas.

### Ejemplo de error de conexión

```json
{
  "error": "SERVICIO_NO_DISPONIBLE",
  "mensaje": "No se pudo contactar el servicio"
}
```

Código HTTP: `502 Bad Gateway`.

## 10. Configuración CORS

El proyecto utiliza CORSMiddleware de FastAPI para permitir solicitudes desde las aplicaciones web Angular.

Para este ejercicio se permite cualquier origen, sin credenciales.

## 11. Pruebas y comprobaciones

Se deben realizar las siguientes pruebas:

- Verificar que las consultas de eventos lleguen al equipo 4.
- Comprobar que las compras conserven el código HTTP 201.
- Comprobar que las respuestas HTTP 409 se reenvíen correctamente.
- Verificar que la consulta de tickets conserve el tipo de contenido `image/png`.
- Comprobar que un servicio desconectado produzca HTTP 502.
- Verificar que `/health` responda correctamente.

## 12. Documentación de la API

FastAPI proporciona documentación automática mediante Swagger UI.

Con el servidor iniciado, acceder a:

```text
http://127.0.0.1:8000/docs
```

También se encuentra disponible la documentación OpenAPI en:

```text
http://127.0.0.1:8000/openapi.json
```

## 13. Despliegue en Railway

El proyecto está preparado para desplegarse en Railway.

Configuración de despliegue:

- Repositorio: GitHub.
- Rama: `main`.
- Dependencias: `requirements.txt`.
- Comando de ejecución:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Variables de entorno necesarias:

```env
EVENTOS_URL=
ENTRADAS_URL=
TICKETS_URL=
IMPRESION_URL=
```

Una vez realizado el despliegue, Railway proporcionará una URL pública que será compartida con los equipos 1, 2 y 3 para integrar sus aplicaciones.
