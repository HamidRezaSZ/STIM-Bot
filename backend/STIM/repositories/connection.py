from enum import Enum
from typing import Type

from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from STIM.models.connection.model import ConnectionModel
from STIM.repositories.base import AsyncSession, BaseRepository


class ConnectionType(Enum):
    csv = "csv"
    sqlite = "sqlite"
    excel = "excel"
    postgres = "postgres"
    mysql = "mysql"
    snowflake = "snowflake"
    sas = "sas"


class ConnectionCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    dsn: str
    database: str
    name: str
    dialect: str
    type: str
    is_sample: bool = False


class ConnectionUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    dsn: str | None = None
    database: str | None = None
    name: str | None = None
    dialect: str | None = None
    type: str | None = None
    is_sample: bool | None = None


class ConnectionRepository(BaseRepository[ConnectionModel, ConnectionCreate, ConnectionUpdate]):
    @property
    def model(self) -> Type[ConnectionModel]:
        return ConnectionModel

    async def get_by_dsn(self, session: AsyncSession, dsn: str) -> ConnectionModel:
        """
        Fetch a record by id.
        :raises: NotFoundError if record not found
        """
        query = select(self.model).filter_by(dsn=dsn)
        return await self.get(session, query)
