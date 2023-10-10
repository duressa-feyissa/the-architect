from core.use_cases.use_case import UseCase
from app.domain.repositories.chat import BaseRepository
from core.common.equatable import Equatable
from core.common.either import Either
from core.errors.failure import Failure
from app.domain.entities.chat import Chat

class Params(Equatable):
    def __init__(self, chat_id: str) -> None:
        self.chat_id = chat_id

class DeleteChat(UseCase[Chat]):
    def __init__(self, repository: BaseRepository):
        self.repository = repository
    
    async def __call__(self, params: Params) -> Either[Failure, Chat]:
        return await self.repository.delete_chat(params.chat_id)