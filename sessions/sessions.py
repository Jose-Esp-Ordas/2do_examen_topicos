from fastapi import APIRouter, HTTPException, Header, Depends
from db.models import SessionDep, ParkingSession, User, Zone, Vehicle
from math import ceil
import datetime

router = APIRouter(prefix="/sessions", tags=["sessions"])

def verify_api_key(x_api_key: str = Header(None)) -> str:
    API_KEY = "testkey"
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail={"Error": "API key inválida/requerida"})
    return x_api_key


@router.post("/start", dependencies=[Depends(verify_api_key)])
async def start_parking(session: ParkingSession, Session: SessionDep) -> {Vehicle.plate,Zone.id}:
    active_session = Session.exec(
        f"SELECT * FROM ParkingSession WHERE vehicle_id = {session.vehicle_id} " \
        "AND status = 'active'").all()
    if not active_session:
        Session.add(session)
        Session.commit()
        Session.refresh(session)
    else:
        raise HTTPException(status_code=409, detail={"Detail":
        "El vehículo ya tiene una sesión activa"})
    return {"plate": Session.get(Vehicle, session.vehicle_id).plate,
            "zone_id": session.zone_id, "zona": Session.get(Zone, session.zone_id).name}

@router.post("/stop/{session_id}", dependencies=[Depends(verify_api_key)])
async def stop_parking(session_id: int, Session: SessionDep) -> ParkingSession:
    active_session = Session.get(ParkingSession, session_id)
    if active_session.status == "active":
    
        active_session.ended_at = str(datetime.datetime.now())
        total_minutes = datetime.strptime(active_session.started_at, "%Y-%m-%d %H:%M:%S") - datetime.datetime.now()
        active_session.minutes = ceil(int(total_minutes))
        
        if total_minutes <= 3:
            active_session.cost = 0.0
        elif total_minutes > Session.get(Zone, active_session.zone_id).max_minutes:
            fine = 100 + total_minutes * Session.get(Zone,
            active_session.zone_id).rate_per_min
            active_session.cost = fine        
        else:
            active_session.cost = total_minutes * Session.get(Zone,
            active_session.zone_id).rate_per_min
        if active_session.cost > Session.get(User, active_session.user_id).balance:
            active_session.status = "pending_payment"
        else:
            active_session.status = "completed"
            user = Session.get(User, active_session.user_id)
            user.balance -= active_session.cost
            Session.add(user)
        Session.add(active_session)
        Session.commit()
    else:
        raise HTTPException(status_code=409, detail={"Detail":
        "La sesión ya ha sido finalizada"})

@router.get("/{session_id}", dependencies=[Depends(verify_api_key)])
async def get_session_status(session_id: int, Session: SessionDep) -> ParkingSession:
    parking_session = Session.get(ParkingSession, session_id)
    if not parking_session:
        raise HTTPException(status_code=404, detail={"Detail":
        "La sesión no existe"})
    if parking_session.status == "":
        return {"minutes": parking_session.minutes,
            "status": parking_session.status,
            "cost_total": parking_session.cost}