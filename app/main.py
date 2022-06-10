import uvicorn
from decouple import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, userinfo_orm
from database import db_session


app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
database_instance = db_session.database_instance


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(
        config('PORT_INT')), reload=True, debug=True)


@app.on_event("startup")
async def startup():
    await database_instance.connect()


@app.on_event("shutdown")
async def shutdown():
    await database_instance.disconnect()


@app.get('/')
async def root():
    return {'message': 'Go to /docs to see the documentation'}


@app.get('/health')
async def health():
    return 'OK'


app.include_router(userinfo_orm.router, tags=['userinfo_orm'])
app.include_router(auth.router, tags=['auth'])
