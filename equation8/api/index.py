"""Minimal Vercel ASGI entrypoint; no document-ingestion dependencies or local disk."""
import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from equation8.config import load_environment
load_environment()
from equation8 import et617, checkpoints, provider

app=FastAPI(title='Equation8',version='1.0.0')
app.include_router(et617.router)

@app.middleware('http')
async def checkpoint_context(request: Request, call_next):
    context_token=checkpoints.current.set(None)
    try:
        if checkpoints.enabled() and request.method in ('POST','PATCH'):
            try:body=await request.json()
            except (ValueError,json.JSONDecodeError):body={}
            token=body.get('session_token') if isinstance(body,dict) else None
            if token:checkpoints.current.set(checkpoints.unseal(token))
        response=await call_next(request)
        if request.url.path.startswith('/api/'):
            response.headers['Cache-Control']='no-store'
        return response
    except Exception as e:
        from fastapi import HTTPException
        if isinstance(e,HTTPException):return JSONResponse({'detail':e.detail},status_code=e.status_code)
        raise
    finally:checkpoints.current.reset(context_token)

@app.get('/api/health')
def health():
    return {'status':'ok','app':'Equation8','ai_configured':provider.configured(),'storage':'encrypted-device-checkpoint' if checkpoints.enabled() else 'sqlite-local'}

# SQLite is used only by the local standalone server, not by Vercel.
if not checkpoints.enabled():et617.initialize()
