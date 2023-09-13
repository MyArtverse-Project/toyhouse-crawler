from fastapi import FastAPI
from main import get_toyhouse_data

app = FastAPI()

@app.get("/")
async def root():
    return { "message": "Hello World", "status": 200 }

@app.get("/toyhouse/{username}")
async def toyhouse(username):
    data = {'data': get_toyhouse_data(username)}
    return { 'data': data, "status": 200 }