from fastapi import FastAPI
from db.models import engine, SessionDep,User, Zone
from sqlmodel import SQLModel
from info import info
from sessions import sessions
from wallet import wallet

app = FastAPI(title="ParkiLite", version="1.0.0")

SQLModel.metadata.create_all(engine)

@app.get("/")
async def read_root():
    return {"Status": "Api activa"}

app.include_router(wallet.router) 
app.include_router(info.router)
app.include_router(sessions.router)


if __name__ == "__main__":
    with SessionDep() as session:
        x = session.get(User, 1)
        if not x:
            from demo import usuario_demo, zona_demo_a, zona_demo_b
            session.add(usuario_demo)
            session.add(zona_demo_a)
            session.add(zona_demo_b)
            session.commit()