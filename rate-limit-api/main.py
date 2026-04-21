from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config_store import set_config
from middlewares.rate_limit import RateLimitMiddleware
from fastapi import Request

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RateLimitMiddleware)
class CheckRequest(BaseModel):
    api_key : str
class ConfigRequest(BaseModel):
    api_key : str
    limit : int
    window : int
    strategy : str

@app.post("/check")
def check(request: Request, api_key: str = Header(None, alias="x-api-key")):
    allow = getattr(request.state, "allow", True)
    remaining = getattr(request.state, "remaining", None)

    return {
        "status": "ok",
        "data":{
            "api_key": api_key,
            "allow": allow,
            "remaining" : remaining
        }

    }
@app.post("/config")
def config(req: ConfigRequest): 
    set_config(
        api_key=req.api_key,
        limit=req.limit,
        window=req.window,
        strategy=req.strategy
    )
    return {"message": "Config updated"}
