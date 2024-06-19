from fastapi import FastAPI
from .routers import auth,sms
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
from .middleware.logs import LoggingRoute

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.router.route_class = LoggingRoute
app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
app.include_router(sms.router, tags=['Sms'], prefix='/api')

@app.get('/')
def health():
    return {'Health': 'OK'}
