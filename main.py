from fastapi import FastAPI
import api.v1
import uvicorn

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
