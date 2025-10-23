from fastapi import APIRouter, HTTPException
from db.models import SessionDep, User

router = APIRouter(prefix="/wallet", tags=["wallet"])

@router.post("/deposit/{user_id}/{amount}")
async def deposit_funds(user_id: int, amount: float, Session: SessionDep) -> User:
    user = Session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail={"No encontrado": f"Usuario: {user_id}"})
    user.balance += amount
    Session.add(user)
    Session.commit()
    Session.refresh(user)
    return user