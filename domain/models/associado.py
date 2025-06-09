from datetime import datetime


class Associado:
    id: int
    nome: str
    cpf: str
    nascimento: datetime
    renda: float
    cadastro: datetime

    def __init__(
        self,
        id: int | None = None,
        nome: str | None = None,
        cpf: str | None = None,
        nascimento: datetime | None = None,
        renda: float | None = None,
        cadastro: datetime | None = None,
    ) -> None:
        if id is not None:
            self.id = id
        if nome is not None:
            self.nome = nome
        if cpf is not None:
            self.cpf = cpf
        if nascimento is not None:
            self.nascimento = nascimento
        if renda is not None:
            self.renda = renda
        if cadastro is not None:
            self.cadastro = cadastro
