from pydantic import BaseModel, Field


class ConsultarDTO(BaseModel):
    cooperado: str = Field()


class ConsultarResponseDTO(BaseModel):
    colaboradores: list[str] = Field()
    assuntos: list[str] = Field()
    evitar: list[str] = Field()
