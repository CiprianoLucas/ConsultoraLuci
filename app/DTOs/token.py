from pydantic import BaseModel, Field


class TokenDTO(BaseModel):
    agencia: int = Field()
    senha: str = Field()


class TokenResponseDTO(BaseModel):
    token: str = Field()
