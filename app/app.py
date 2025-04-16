from fastapi import FastAPI
from app.routers import props_router, odds_router, baseball_router, dfs_router  # Import routers for organization
from fastapi.middleware.cors import CORSMiddleware




# Initialize FastAPI application
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include the routers with /api prefix
app.include_router(props_router.router, prefix="/api/props", tags=["props"])
app.include_router(odds_router.router, prefix="/api/odds", tags=["odds"])
app.include_router(baseball_router.router, prefix="/api/baseball", tags=["baseball"])  # ✅ add new router
app.include_router(dfs_router.router, prefix="/api/dfs", tags=["dfs"])  # ✅ add DFS router

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI backend!"}

print("App is being loaded")
