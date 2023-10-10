from core.use_cases.use_case import UseCase
from app.domain.repositories.user import BaseRepository
from core.common.equatable import Equatable
from core.common.either import Either
from core.errors.failure import Failure
from app.domain.entities.user import User, UserEntity

class Params(Equatable):
    def __init__(self, user: UserEntity) -> None:
        self.user = user
        
class UpdateUser(UseCase[User]):
    def __init__(self, repository: BaseRepository):
        self.repository = repository
    
    async def __call__(self, params: Params) -> Either[Failure, User]:
        return await self.repository.update_user(params.user)