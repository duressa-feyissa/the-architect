from abc import ABC, abstractmethod
from app.domain.repositories import ContextManagerRepository
from core.common.either import Either
from core.errors.failure import Failure
from app.domain.entities.message import Message, MessageEntity


class BaseWriteOnlyRepository(ContextManagerRepository):
    @abstractmethod
    async def create_message(self, message: Message, chat_id: str) -> Either[Failure, MessageEntity]:
        ...

class BaseRepository(BaseWriteOnlyRepository, ABC):
    ...
