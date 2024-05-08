from fastapi import FastAPI
from api import model

app = FastAPI()
app.include_router(model.router)

@app.get("/")
def health_check_handler():
    return {"message": "Hello World!"}
