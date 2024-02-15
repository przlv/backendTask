import uvicorn
from fastapi import FastAPI

import api.v1 as routes
from db.database import create_tables

app = FastAPI()

app.include_router(routes.router_shiftAssignment)
app.include_router(routes.router_products)


@app.on_event("startup")
async def startup_event():
    await create_tables()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
