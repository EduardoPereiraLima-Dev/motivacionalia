import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    host = "0.0.0.0"   # escuta em todas interfaces (útil para servidores)
    port = 8000        # porta padrão
    uvicorn.run(app, host=host, port=port)
