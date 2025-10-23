from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    api_key: str = Field(unique=True)
    balance: float = Field()
    
class Zone(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    rate_per_min: str | None = Field(default=None)
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
    started_at: str = Field()
    ended_at: str | None = Field(default=None)
    minutes: int | None = Field(default=None)
    cost: float | None = Field(default=None)
    status: str = Field()