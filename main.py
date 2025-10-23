from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Status": "Api activa"}