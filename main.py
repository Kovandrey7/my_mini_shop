import uvicorn
from fastapi import FastAPI

from api.buyer.handlers import router as buyer_router

app = FastAPI()

app.include_router(buyer_router)


if __name__ == "__main__":
    uvicorn.run(app)
