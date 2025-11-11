# mediaflow_proxy/security.py
from fastapi import Header, Query, HTTPException, Request, Depends
from .settings import settings  # your existing settings loader

def require_api_key(
    request: Request,
    x_api_password: str | None = Header(default=None, alias="X-API-Password"),
    api_password: str | None = Query(default=None),
    token: str | None = Query(default=None),  # MediaFusion compatibility
):
    """
    Accept password from header, 'api_password', or legacy 'token'.
    Raises 403 if missing or mismatched.
    """
    pwd = x_api_password or api_password or token
    if not pwd or pwd != settings.api_password:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    # Optionally mark request as authenticated for downstream code
    request.state.api_auth_ok = True
    return True
