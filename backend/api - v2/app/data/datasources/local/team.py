from abc import ABC, abstractmethod
from typing import List
from uuid import uuid4

import requests
from app.data.datasources.remote.ai import AiGeneration
from app.data.models.team import TeamModel, UserTeamModel
from app.data.models.user import UserModel
from app.domain.entities.team import Team, TeamEntity
from app.domain.entities.user import UserEntity
from cloudinary.uploader import upload
from core.errors.exceptions import CacheException
from sqlalchemy.orm import Session


class TeamLocalDataSource(ABC):

    @abstractmethod
    async def create_team(self, team: Team, user_id: str) -> TeamEntity:
        ...

    @abstractmethod
    async def update_team(self, team: Team, team_id: str, user_id: str) -> TeamEntity:
        ...

    @abstractmethod
    async def delete_team(self, team_id: str) -> TeamEntity:
        ...

    @abstractmethod
    async def view_teams(self, user_id: str) -> List[TeamEntity]:
        ...

    @abstractmethod
    async def view_team(self, team_id: str) -> TeamEntity:
        ...

    @abstractmethod
    async def join_team(self, team_id: str, user_id: str) -> TeamEntity:
        ...

    @abstractmethod
    async def leave_team(self, team_id: str, user_id: str) -> TeamEntity:
        ...

    @abstractmethod
    async def team_members(self, team_id: str) -> List[UserEntity]:
        ...


class TeamLocalDataSourceImpl(TeamLocalDataSource):

    def __init__(self, db: Session):
        self.db = db
        self.ai_generation = AiGeneration(request=requests, upload=upload)

    async def create_team(self, team: Team, user_id: str) -> TeamEntity:
        existing_user = self.db.query(UserModel).filter(
            UserModel.id == user_id).first()
        if not existing_user:
            raise CacheException("User does not exist")

        creator_first_name = existing_user.first_name
        creator_last_name = existing_user.last_name

        _team = TeamModel(
            id=str(uuid4()),
            creator_id=user_id,
            title=team.title,
            description=team.description,
            image="https://i.pinimg.com/736x/6d/05/75/6d0575fb1f66c830cb71f07184cb2f94.jpg"
        )

        _teamUser = UserTeamModel(
            id=str(uuid4()),
            user_id=user_id,
            team_id=_team.id
        )

        self.db.add(_teamUser)
        self.db.add(_team)
        self.db.commit()
        self.db.refresh(_team)

        created_team = TeamEntity(
            id=_team.id,
            title=_team.title,
            description=_team.description,
            creator_id=_team.creator_id,
            creator_image=existing_user.image,
            image=_team.image,
            first_name=creator_first_name,
            last_name=creator_last_name,
            create_at=_team.date
        )

        return created_team

    async def update_team(self, team: Team, team_id: str, user_id: str) -> TeamEntity:
        existing_team = self.db.query(TeamModel).filter(
            TeamModel.id == team_id).first()
        if not existing_team:
            raise CacheException("Team does not exist")
        if existing_team.creator_id != user_id:
            raise CacheException("User is not the creator of the team")

        existing_team.title = team.title
        existing_team.description = team.description
        if team.image is not None and team.image != '':
            existing_team.image = await self.ai_generation.upload_image(team.image)

        existing_user = self.db.query(UserModel).filter(
            UserModel.id == existing_team.creator_id).first()

        self.db.commit()

        updated_team = TeamEntity(
            id=existing_team.id,
            title=existing_team.title,
            description=existing_team.description,
            creator_id=existing_team.creator_id,
            creator_image=existing_user.image,
            image=existing_team.image,
            create_at=existing_team.date,
            first_name=existing_user.first_name,
            last_name=existing_user.last_name
        )

        return updated_team

    async def delete_team(self, team_id: str) -> TeamEntity:
        existing_team = self.db.query(TeamModel).filter(
            TeamModel.id == team_id).first()
        if not existing_team:
            raise CacheException("Team does not exist")

        self.db.delete(existing_team)
        self.db.commit()

        deleted_team = TeamEntity(
            id=existing_team.id,
            title=existing_team.title,
            description=existing_team.description,
            creator_id=existing_team.creator_id,
            creator_image="",
            image=existing_team.image,
            create_at=existing_team.date,
            first_name="",
            last_name=""
        )

        return deleted_team

    async def view_teams(self, user_id: str) -> List[TeamEntity]:
        existing_user = self.db.query(UserModel).filter(
            UserModel.id == user_id).first()
        if not existing_user:
            raise CacheException("User does not exist")

        team_entities = []
        for user_team in existing_user.teams:
            team = user_team.team
            if team:
                team_entities.append(TeamEntity(
                    id=team.id,
                    title=team.title,
                    description=team.description,
                    creator_id=team.creator_id,
                    creator_image=existing_user.image,
                    image=team.image,
                    create_at=team.date,
                    first_name=existing_user.first_name,
                    last_name=existing_user.last_name
                ))

        return team_entities

    async def view_team(self, team_id: str) -> TeamEntity:
        existing_team = self.db.query(TeamModel).filter(
            TeamModel.id == team_id).first()

        existing_user = self.db.query(UserModel).filter(
            UserModel.id == existing_team.creator_id).first()

        if not existing_team:
            raise CacheException("Team does not exist")

        return TeamEntity(
            id=existing_team.id,
            title=existing_team.title,
            description=existing_team.description,
            creator_id=existing_team.creator_id,
            creator_image=existing_user.image,
            image=existing_team.image,
            create_at=existing_team.date,
            first_name=existing_user.first_name,
            last_name=existing_user.last_name
        )

    async def join_team(self, team_id: str, user_id: str) -> TeamEntity:
        existing_user = self.db.query(UserModel).filter(
            UserModel.id == user_id).first()
        if not existing_user:
            raise CacheException("User does not exist")

        existing_team = self.db.query(TeamModel).filter(
            TeamModel.id == team_id).first()
        if not existing_team:
            raise CacheException("Team does not exist")

        user_team_exists = self.db.query(UserTeamModel).filter(
            UserTeamModel.user_id == user_id, UserTeamModel.team_id == team_id
        ).first()

        if user_team_exists:
            raise CacheException("User is already a member of this team")

        user_team = UserTeamModel(
            id=str(uuid4()),
            user_id=user_id,
            team_id=team_id
        )
        self.db.add(user_team)
        self.db.commit()

        creator = self.db.query(UserModel).filter(
            UserModel.id == existing_team.creator_id).first()

        return TeamEntity(
            id=existing_team.id,
            title=existing_team.title,
            description=existing_team.description,
            creator_id=existing_team.creator_id,
            creator_image=creator.image,
            image=existing_team.image,
            create_at=existing_team.date,
            first_name=creator.first_name,
            last_name=creator.last_name
        )

    async def leave_team(self, team_id: str, user_id: str) -> TeamEntity:
        existing_user = self.db.query(UserModel).filter(
            UserModel.id == user_id).first()
        if not existing_user:
            raise CacheException("User does not exist")

        existing_team = self.db.query(TeamModel).filter(
            TeamModel.id == team_id).first()
        if not existing_team:
            raise CacheException("Team does not exist")

        user_team = self.db.query(UserTeamModel).filter(
            UserTeamModel.user_id == user_id,
            UserTeamModel.team_id == team_id
        ).first()

        if not user_team:
            raise CacheException("User isn't memeber of a time")

        if user_team:
            self.db.delete(user_team)
            self.db.commit()

        if existing_team.creator_id == user_id:
            self.db.delete(existing_team)
            self.db.commit()

        creator = self.db.query(UserModel).filter(
            UserModel.id == existing_team.creator_id).first()

        return TeamEntity(
            id=existing_team.id,
            title=existing_team.title,
            description=existing_team.description,
            creator_id=existing_team.creator_id,
            creator_image=creator.image,
            image=existing_team.image,
            create_at=existing_team.date,
            first_name=creator.first_name,
            last_name=creator.last_name
        )

    async def team_members(self, team_id: str) -> List[UserEntity]:
        existing_team = self.db.query(TeamModel).filter(
            TeamModel.id == team_id).first()
        if not existing_team:
            raise CacheException("Team does not exist")

        user_teams = existing_team.members

        return [
            UserEntity(
                id=user.user.id,
                firstName=user.user.first_name,
                lastName=user.user.last_name,
                bio=user.user.bio,
                email=user.user.email,
                image=user.user.image,
                password=user.user.password,
                country=user.user.country,
                followers=user.user.get_followers_count(self.db),
                following=user.user.get_following_count(self.db)
            ) for user in user_teams
        ]
