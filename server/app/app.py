import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

load_dotenv()

CLIENT_URL = os.getenv("CLIENT_URL", "http://localhost:5173")

app = FastAPI(
    title="MindTrace",
    version="1.0",
    description="API for RAG ChatBot",
)

origins = [
    CLIENT_URL,
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/")
def server_status():
    return JSONResponse(content={ "message": "Server is live" }, status_code=200)
