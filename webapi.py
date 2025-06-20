from fastapi import FastAPI
from api.webhook_listener import router as webhook_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "BlackStrike API is running"}

app.include_router(webhook_router)

