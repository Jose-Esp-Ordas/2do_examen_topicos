from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Annotated
from fastapi import Depends
import datetime

engine = create_engine("sqlite:///database.db")
db = SQLModel.metadata

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    api_key: str = Field(unique=True)
    balance: float = Field()
    
class Zone(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    rate_per_min: float | None = Field(default=None)
    max_minutes: int | None = Field(default=None)

class Vehicle(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    plate: str = Field(unique=True)

class ParkingSession(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    vehicle_id: int = Field(foreign_key="vehicle.id")
    zone_id: int = Field(foreign_key="zone.id")
    started_at:  str = Field(default=str(datetime.datetime.now()))
    ended_at: str | None = Field(default=None)
    minutes: int | None = Field(default=None)
    cost: float | None = Field(default=None)
    status: str = Field(default="active")