from fastapi import APIRouter
from db.models import Vehicle, User, SessionDep
from fastapi import HTTPException

router = APIRouter()

@router.get("/zones")
async def get_zones(Session: SessionDep) -> list:
    zones = Session.exec("SELECT * FROM Zone").all()
    return zones

@router.post("/vehicles/")
async def create_vehicle(vehicle: Vehicle, Session: SessionDep) -> Vehicle:
    try:
        Session.add(vehicle)
        Session.commit()
        Session.refresh(vehicle)
        return vehicle
    except Exception as e:
        raise HTTPException(status_code=400, detail={e:"Error al crear el"
        "vehículo"}) from e

@router.get("/vehicles/{user_id}")
async def get_vehicles(user_id: int, Session: SessionDep) -> list:
    try:
        vehicles = Session.exec(
            "SELECT * FROM Vehicle WHERE user_id = :user_id"
        , {"user_id": user_id}).all()
        return vehicles
    except Exception as e:
        raise HTTPException(status_code=404, detail={e:"Error al obtener los"
        "autos"}) from e