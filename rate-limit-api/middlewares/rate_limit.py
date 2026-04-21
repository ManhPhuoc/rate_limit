from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from services.rate_limiter import check_rate_limit

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)
        
        if request.url.path in ["/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)
        if request.url.path == "/config":
            return await call_next(request)
        # check for api key in header
        api_key = request.headers.get("x-api-key")
        if not api_key:
            try:
                body = await request.json()
                api_key = body.get("api_key")
            except:
                api_key = None
        if not api_key:
            return JSONResponse(status_code=400,content={"error": "Missing x-api-key header"})
        
        allow, remaining = check_rate_limit(api_key)
        request.state.allow = allow
        request.state.remaining = remaining
        response = await call_next(request)

        return response