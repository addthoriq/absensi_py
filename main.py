from fastapi import FastAPI

app = FastAPI(title="Absensi Python")


@app.get("/")
async def root():
    return {"message": "Hello World!"}
