
import os
import httpx

from fastapi import FastAPI, Request
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="API Gateway",
    description="Gateway para los servicios de los equipos 4, 5, 7 y 8",
    version="1.0.0"
)

# URLs configuradas mediante variables de entorno
SERVICES = {
    "eventos": os.getenv("EQUIPO_4_URL"),
    "entradas": os.getenv("EQUIPO_5_URL"),
    "tickets": os.getenv("EQUIPO_7_URL"),
    "impresiones": os.getenv("EQUIPO_8_URL"),
}

# CORS para aplicaciones Angular
origins = [
    "http://localhost:4200",
    # Agregar aquí los dominios de Angular desplegados
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "API Gateway"
    }


@app.api_route(
    "/api/{service}/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
)
@app.api_route(
    "/api/{service}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
)
async def gateway(request: Request, service: str, path: str = ""):

    # Verificar que el servicio exista
    if service not in SERVICES:
        return JSONResponse(
            status_code=404,
            content={"error": f"Servicio '{service}' no encontrado"}
        )

    base_url = SERVICES[service]

    if not base_url:
        return JSONResponse(
            status_code=502,
            content={"error": f"URL del servicio '{service}' no configurada"}
        )

    # Construir URL sin el prefijo /api
    target_url = f"{base_url.rstrip('/')}/{service}/{path}".rstrip("/")

    # Conservar parámetros de consulta
    if request.url.query:
        target_url += f"?{request.url.query}"

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:

            response = await client.request(
                method=request.method,
                url=target_url,
                content=await request.body(),
                headers={
                    key: value
                    for key, value in request.headers.items()
                    if key.lower() not in [
                        "host",
                        "content-length",
                        "connection"
                    ]
                }
            )

        # Mantener el código HTTP y Content-Type original
        headers = {}

        if "content-type" in response.headers:
            headers["Content-Type"] = response.headers["content-type"]

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=headers
        )

    except (httpx.TimeoutException, httpx.RequestError) as error:
        return JSONResponse(
            status_code=502,
            content={
                "error": "Servicio no disponible",
                "service": service,
                "detail": str(error)
            }
        )
