from core.use_cases.use_case import UseCase
from app.domain.repositories.sketch import BaseRepository
from core.common.equatable import Equatable
from core.common.either import Either
from core.errors.failure import Failure
from app.domain.entities.sketch import Sketch, SketchEntity

class Params(Equatable):
    def __init__(self, sketch: Sketch, sketch_id: str, team_id: str,  user_id: str) -> None:
        self.sketch = sketch
        self.sketch_id = sketch_id
        self.team_id = team_id
        self.user_id = user_id
        
class UpdateSketch(UseCase[SketchEntity]):
    def __init__(self, repository: BaseRepository):
        self.repository = repository
    
    async def __call__(self, params: Params) -> Either[Failure, SketchEntity]:
        return await self.repository.update_sketch(params.sketch, params.sketch_id, params.team_id, params.user_id)