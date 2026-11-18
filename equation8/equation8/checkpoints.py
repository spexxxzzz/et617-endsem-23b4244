"""Authenticated encrypted checkpoints for a stateless single-learner deployment."""
import base64
import hashlib
import json
import os
import zlib
from contextvars import ContextVar
from cryptography.fernet import Fernet, InvalidToken
from fastapi import HTTPException

current: ContextVar[dict | None] = ContextVar('equation8_checkpoint', default=None)


def enabled():
    return os.getenv('VERCEL') == '1' or os.getenv('EQUATION8_STATELESS') == '1'


def cipher():
    secret = os.getenv('SESSION_SECRET') or os.getenv('HYDE_API_KEY')
    if not secret:
        raise HTTPException(503, 'Set SESSION_SECRET and HYDE_API_KEY in the deployment environment.')
    return Fernet(base64.urlsafe_b64encode(hashlib.sha256(secret.encode()).digest()))


def seal(state):
    raw = json.dumps(state, separators=(',', ':')).encode()
    return cipher().encrypt(zlib.compress(raw)).decode()


def unseal(token):
    if not isinstance(token,str) or len(token)>100000:
        raise HTTPException(400,'Invalid learning checkpoint.')
    try:
        compressed=cipher().decrypt(token.encode(),ttl=30*24*3600)
        raw=zlib.decompress(compressed)
        state=json.loads(raw)
        if not isinstance(state,dict) or not isinstance(state.get('id'),str):raise ValueError()
        return state
    except (InvalidToken,ValueError,TypeError,zlib.error,json.JSONDecodeError):
        raise HTTPException(400,'This checkpoint is invalid or expired. Start a fresh learning session.') from None


def attach(result,state):
    return {**result,'session_token':seal(state),'checkpoint_id':state['id']} if enabled() else result
