from core.use_cases.use_case import UseCase
from app.domain.repositories.user import BaseRepository
from core.common.equatable import Equatable
from core.common.either import Either
from core.errors.failure import Failure
from app.domain.entities.user import UserEntity, UpdatUserRequest

class Params(Equatable):
    def __init__(self, user: UpdatUserRequest, user_id: str) -> None:
        self.user = user
        self.user_id = user_id
        
class UpdateUser(UseCase[UserEntity]):
    def __init__(self, repository: BaseRepository):
        self.repository = repository
    
    async def __call__(self, params: Params) -> Either[Failure, UserEntity]:
        return await self.repository.update_user(params.user, params.user_id)