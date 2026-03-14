from fastapi import FastAPI
from routers.agent_router import agent_router
from db.postgre_db import engine
from db.models import Base
app = FastAPI()

app.include_router(agent_router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", reload=True)
