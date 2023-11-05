from dataclasses import dataclass
from typing import Optional

from app.domain.entities import BaseEntity
from pydantic import BaseModel


class Project(BaseModel):
    title: str
    class Config:
        arbitrary_types_allowed = True

@dataclass
class ProjectEntity(BaseEntity):
    id: Optional[str]
    title: str
    team_id: str
    sketch_ids: Optional[list]
    create_at: str

    @classmethod
    def from_dict(cls, adict):
        return cls(**adict)
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "team_id": self.team_id,
            "sketch_ids": self.sketch_ids,
            "create_at": self.create_at
        }
