from core.config.database_config import Base
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


# class SketchModel(Base):
#     __tablename__ = 'sketches'
#     id = Column(String(36), primary_key=True, nullable=False)
#     sketch = Column(String(256))
#     chat = Column(String(256))
#     project_id = Column(String(36), ForeignKey('projects.id'), nullable=False)
#     project = relationship('ProjectModel', back_populates='sketches')

#     def __repr__(self) -> str:
#         return f'<SketchModel id={self.id} sketch={self.sketch} chat={self.chat}>'
