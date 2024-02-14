import uvicorn
from fastapi import FastAPI

import api.v1 as routes

app = FastAPI()

app.include_router(routes.router_shiftAssignment)
app.include_router(routes.router_products)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
