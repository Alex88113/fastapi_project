from pydantic import ValidationError

class EnvValidationException(Exception):
    def __init__(self, error: str) -> None:
        self.error = error
        message: str = f"Возникла ошибка при загрузке данных из .env: {error}"
        super().__init__(message)
