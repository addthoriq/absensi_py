from fastapi import FastAPI
from routes import routers

app = FastAPI(title="Absensi Python")
app.include_router(routers)


@app.get("/")
async def root():
    return {"message": "Absensi Python"}
