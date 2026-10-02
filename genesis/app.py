from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy import select

from .api import router
from .background import supervisor
from .config import ROOT, settings
from .database import SessionLocal, User, init_db
from .security import hash_password
from .services import ensure_workspace

WEB = ROOT / "web"


def bootstrap_admin() -> None:
    if not (settings.admin_email and settings.admin_password):
        return
    with SessionLocal() as session:
        existing = session.scalar(select(User).where(User.email == settings.admin_email.lower()))
        if existing:
            if existing.role != "admin":
                existing.role = "admin"
                session.commit()
            return
        user = User(
            email=settings.admin_email.lower(),
            name="Genesis Administrator",
            password_hash=hash_password(settings.admin_password),
            role="admin",
            plan="enterprise",
        )
        session.add(user)
        session.flush()
        ensure_workspace(session, user)
        session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.environment.lower() == "production":
        weak_secret = len(settings.secret_key) < 32 or settings.secret_key.startswith(("change-me", "replace-with"))
        if weak_secret:
            raise RuntimeError("GENESIS_SECRET_KEY must be a strong random secret in production")
        if settings.admin_password and (len(settings.admin_password) < 12 or settings.admin_password.startswith("replace-with")):
            raise RuntimeError("GENESIS_ADMIN_PASSWORD must be changed before production launch")
    init_db()
    bootstrap_admin()
    supervisor.start()
    yield
    supervisor.stop()


app = FastAPI(
    title="Genesis AI Platform",
    version="1.0.0",
    description="Infrastructure for autonomous AI worlds, agents and civilization simulations.",
    lifespan=lifespan,
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=list(settings.trusted_hosts) or ["*"])
app.include_router(router)

@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'"
    return response

app.mount("/assets", StaticFiles(directory=WEB / "assets"), name="assets")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(WEB / "index.html")


@app.get("/{path:path}", include_in_schema=False)
def spa(path: str):
    candidate = WEB / path
    if candidate.is_file() and WEB in candidate.resolve().parents:
        return FileResponse(candidate)
    return FileResponse(WEB / "index.html")
