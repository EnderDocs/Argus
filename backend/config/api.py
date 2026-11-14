from ninja import NinjaAPI

api = NinjaAPI(
    title="Argus API",
    version="1.0.0",
    description="API RESTful para partilha e certificação de datasets de sensores de robótica (ModSI)",
    urls_namespace="api-v1",
)

@api.get("/health", tags=["Infraestrutura"])
def health_check(request):
    """Endpoint de verificação de integridade da API."""
    return {
        "status": "ok",
        "service": "Argus API",
        "version": "1.0.0"
    }
