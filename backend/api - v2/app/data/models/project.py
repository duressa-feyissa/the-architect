from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from core.config.database_config import Base

# class ProjectModel(Base):
#     __tablename__ = 'projects'
#     id = Column(String(36), primary_key=True, nullable=False)
#     name = Column(String(256), nullable=False)
#     team_id = Column(String(36), ForeignKey('teams.id'), nullable=False)
#     team = relationship('TeamModel', back_populates='projects')
#     sketches = relationship('SketchModel', back_populates='project')
    
#     def __repr__(self) -> str:
#         return f'<ProjectModel id={self.id} name={self.name}>'
