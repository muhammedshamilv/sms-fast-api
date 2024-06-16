from fastapi import FastAPI
from .routers import auth
app = FastAPI()

app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')

@app.get('/')
def health():
    return {'Health': 'OK'}
