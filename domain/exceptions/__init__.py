class InvalidTokenException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__("Token inválido")


class WrongPasswordException(Exception):
    def __init__(self) -> None:
        super().__init__("Autenticação inválida")
        

class NotFoundException(Exception):
    def __init__(self, type_value: str):
        super().__init__("Valor não encontrado: " + type_value)
