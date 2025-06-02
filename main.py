import uvicorn
from fastapi import FastAPI
from routes import router
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3333))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)