from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from predictor import train_model, predict_outcomes
from schema_tracker import schema_tracker
#from simulator import simulate_flat_strategy
from auth import router as auth_router
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

# Serve frontend static files
app.mount("/static", StaticFiles(directory="../frontend/dist/assets"), name="static")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

@app.get("/{full_path:path}", response_class=HTMLResponse)
async def serve_spa(full_path: str, request: Request):
    index_path = Path(__file__).parent.parent / "frontend" / "dist" / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return HTMLResponse(content="Index file not found", status_code=404)

@app.post("/api/train-model")
def train(data: dict, user: str = Depends(get_current_user)):
    for bet in data["bets"]:
        schema_tracker.update(bet)
    audit = train_model(data["bets"])
    return {"status": "Model trained", **audit}

@app.post("/api/predict")
def predict(data: dict, user: str = Depends(get_current_user)):
    return {"predictions": predict_outcomes(data["bets"])}

@app.get("/api/schema")
def get_schema(user: str = Depends(get_current_user)):
    return schema_tracker.get_schema()

#@app.post("/api/simulate")
#def simulate(data: dict, user: str = Depends(get_current_user)):
#    return simulate_flat_strategy(data["bets"])

@app.post("/api/upload-session")
def upload_session(bets: list, user: str = Depends(get_current_user)):
    # For simplicity, save sessions per user in a JSON file
    import json
    user_sessions_file = f"sessions_{user}.json"
    if os.path.exists(user_sessions_file):
        with open(user_sessions_file, "r") as f:
            sessions = json.load(f)
    else:
        sessions = []
    sessions.append(bets)
    with open(user_sessions_file, "w") as f:
        json.dump(sessions, f)
    return {"status": "Session uploaded"}

@app.get("/api/my-sessions")
def my_sessions(user: str = Depends(get_current_user)):
    import json
    user_sessions_file = f"sessions_{user}.json"
    if os.path.exists(user_sessions_file):
        with open(user_sessions_file, "r") as f:
            sessions = json.load(f)
    else:
        sessions = []
    return sessions
