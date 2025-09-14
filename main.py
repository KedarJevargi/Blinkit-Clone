import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import logging


from config.connectDB import connect_DB, disconnect_DB 
from routes import userRoute

logging.basicConfig(level=logging.INFO)
PORT = int(os.getenv("PORT", 8000))
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")



@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_DB(app)  
    yield
    await disconnect_DB(app)
    



app = FastAPI(
    lifespan=lifespan,
    title="Blinkit Clone API",
    description="Backend services for the Blinkit application.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def helmet_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-DNS-Prefetch-Control"] = "off"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "0" # Deprecated, but this is the correct way to disable it.
    response.headers["Cross-Origin-Resource-Policy"] = "cross-origin"
    return response







@app.get("/", tags=["Health Check"])
async def root():
    return {"message":"Server is running 🚀"}


app.include_router(userRoute.router, prefix="/api/v1", tags=["User"])







if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)



