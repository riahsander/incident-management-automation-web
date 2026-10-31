from pydantic import BaseModel

class ApiResponse(BaseModel):
    success: bool
    message: str


class IncidenteResponse(ApiResponse):
    chamado: str | None = None