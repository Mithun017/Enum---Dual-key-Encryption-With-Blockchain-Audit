from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.encryption.routes import router as encryption_router
from app.blockchain.routes import router as blockchain_router
from app.monitoring.routes import router as monitoring_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Dual-Key Encryption System",
    description="Secure backend with dual-key encryption and blockchain audit.",
    version="1.0.0"
)

# Enable CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, set to specific frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(encryption_router, prefix="/encryption")
app.include_router(blockchain_router, prefix="/audit")
app.include_router(monitoring_router, prefix="/monitor")

@app.get("/")
async def root():
    return {"message": "System Operational"}
