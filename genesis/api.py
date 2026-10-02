from __future__ import annotations

import json
import re
import random
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .config import settings
from .billing import create_checkout, process_webhook, provider_status
from .database import Agent, ApiKey, AuditLog, Event, SessionLocal, Snapshot, User, Workspace, WorkspaceMember, World, db_session
from .engine import tick_world
from .plans import PLANS
from .schemas import AdminUserPatch, AgentCreate, AgentTaskRequest, ApiKeyCreate, CheckoutRequest, LoginRequest, PasswordChange, ProfilePatch, RegisterRequest, TickRequest, WorkspaceMemberCreate, WorldCreate, WorldPatch
from .security import api_key_hash, create_token, decode_token, hash_password, new_api_key, verify_password
from .services import TEMPLATES, accessible_workspace, audit, create_world, ensure_workspace, owned_world, serialize_user, serialize_world, world_detail

router = APIRouter(prefix="/api/v1")
bearer = HTTPBearer(auto_error=False)

_auth_rate_lock = threading.Lock()
_auth_rate: dict[str, list[float]] = {}

def enforce_auth_rate(request: Request, limit: int = 12, window: int = 300) -> None:
    host = request.client.host if request.client else "unknown"
    now = time.time()
    with _auth_rate_lock:
        hits = [t for t in _auth_rate.get(host, []) if now - t < window]
        if len(hits) >= limit:
            raise HTTPException(status_code=429, detail="too many authentication attempts")
        hits.append(now)
        _auth_rate[host] = hits


def get_db() -> Session:
    with SessionLocal() as session:
        yield session


def current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    session: Session = Depends(get_db),
) -> User:
    token = credentials.credentials if credentials else None
    user: User | None = None
    if token:
        try:
            payload = decode_token(token)
            user = session.get(User, payload["sub"])
            if user and int(payload.get("ver", -1)) != user.token_version:
                user = None
        except Exception:
            user = None
    if not user:
        raw_key = request.headers.get("X-API-Key")
        if raw_key:
            key = session.scalar(select(ApiKey).where(ApiKey.key_hash == api_key_hash(raw_key)))
            if key:
                user = session.get(User, key.user_id)
                key.last_used_at = datetime.now(timezone.utc)
                session.commit()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="authentication required")
    return user


def admin_user(user: User = Depends(current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="admin role required")
    return user


def password_ok(password: str) -> bool:
    return bool(re.search(r"[A-Za-z]", password) and re.search(r"\d", password))


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "genesis", "version": "1.0.0", "environment": settings.environment}


@router.post("/auth/register")
def register(data: RegisterRequest, request: Request, session: Session = Depends(get_db)) -> dict:
    enforce_auth_rate(request)
    if not settings.allow_registration:
        raise HTTPException(status_code=403, detail="registration disabled")
    if not password_ok(data.password):
        raise HTTPException(status_code=422, detail="password must contain letters and numbers")
    email = data.email.lower().strip()
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise HTTPException(status_code=422, detail="valid email required")
    if session.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=409, detail="account already exists")
    user = User(email=email, name=data.name.strip(), password_hash=hash_password(data.password), plan="free", role="user")
    session.add(user)
    session.flush()
    ensure_workspace(session, user)
    audit(session, user.id, "auth.register", user.id)
    session.commit()
    return {"token": create_token(user.id, user.role, user.token_version), "user": serialize_user(user)}


@router.post("/auth/login")
def login(data: LoginRequest, request: Request, session: Session = Depends(get_db)) -> dict:
    enforce_auth_rate(request)
    user = session.scalar(select(User).where(User.email == data.email.lower().strip()))
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="invalid email or password")
    audit(session, user.id, "auth.login", user.id)
    session.commit()
    return {"token": create_token(user.id, user.role, user.token_version), "user": serialize_user(user)}


@router.get("/me")
def me(user: User = Depends(current_user), session: Session = Depends(get_db)) -> dict:
    workspace = ensure_workspace(session, user)
    return {"user": serialize_user(user), "workspace": {"id": workspace.id, "name": workspace.name}, "entitlements": PLANS.get(user.plan, PLANS["free"])}


@router.patch("/me")
def update_me(data: ProfilePatch, user: User = Depends(current_user), session: Session = Depends(get_db)) -> dict:
    if data.name:
        user.name = data.name.strip()
    audit(session, user.id, "profile.update", user.id)
    session.commit()
    return {"user": serialize_user(user)}


@router.post("/me/password")
def change_password(data: PasswordChange, user: User = Depends(current_user), session: Session = Depends(get_db)) -> dict:
    if not verify_password(data.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="current password is incorrect")
    if not password_ok(data.new_password):
        raise HTTPException(status_code=422, detail="new password must contain letters and numbers")
    user.password_hash = hash_password(data.new_password)
    user.token_version += 1
    audit(session, user.id, "profile.password.change", user.id)
    session.commit()
    return {"changed": True, "token": create_token(user.id, user.role, user.token_version)}


@router.get("/plans")
def plans() -> dict:
    return {"plans": PLANS}


@router.get("/billing/status")
def billing_status(user: User = Depends(current_user)) -> dict:
    return {"plan": user.plan, **provider_status()}


@router.post("/billing/checkout")
def billing_checkout(data: CheckoutRequest, user: User = Depends(current_user)) -> dict:
    return create_checkout(user, data.plan)


@router.post("/billing/webhook")
async def billing_webhook(request: Request, session: Session = Depends(get_db)) -> dict:
    payload = await request.body()
    signature = request.headers.get("stripe-signature", "")
    return process_webhook(payload, signature, session)


@router.get("/marketplace")
def marketplace() -> dict:
    return {"templates": [{"id": key, **value} for key, value in TEMPLATES.items()]}


@router.get("/workspaces")
def workspaces(user: User = Depends(current_user), session: Session = Depends(get_db)) -> dict:
    ensure_workspace(session, user)
    if user.role == "admin":
        rows = session.scalars(select(Workspace).order_by(Workspace.created_at)).all()
        return {"workspaces": [{"id": w.id, "name": w.name, "owner_id": w.owner_id, "role": "admin"} for w in rows]}
    rows = session.execute(select(Workspace, WorkspaceMember).join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id).where(WorkspaceMember.user_id == user.id).order_by(Workspace.created_at)).all()
    return {"workspaces": [{"id": w.id, "name": w.name, "owner_id": w.owner_id, "role": m.role} for w, m in rows]}


@router.get("/dashboard")
def dashboard(workspace_id: str | None = None, user: User = Depends(current_user), session: Session = Depends(get_db)) -> dict:
    workspace = accessible_workspace(session, user, workspace_id)
    worlds = session.scalars(select(World).where(World.workspace_id == workspace.id).order_by(World.updated_at.desc())).all()
    world_ids = [w.id for w in worlds]
    agent_count = session.scalar(select(func.count(Agent.id)).where(Agent.world_id.in_(world_ids))) if world_ids else 0
    event_count = session.scalar(select(func.count(Event.id)).where(Event.world_id.in_(world_ids))) if world_ids else 0
    return {
        "workspace": {"id": workspace.id, "name": workspace.name},
        "totals": {"worlds": len(worlds), "running": sum(w.status == "running" for w in worlds), "agents": agent_count or 0, "events": event_count or 0, "simulation_years": sum(w.age for w in worlds)},
        "worlds": [serialize_world(w) for w in worlds],
    }


@router.get("/worlds")
def list_worlds(workspace_id: str | None = None, user: User = Depends(current_user), session: Session = Depends(get_db)) -> dict:
    workspace = accessible_workspace(session, user, workspace_id)
    worlds = session.scalars(select(World).where(World.workspace_id == workspace.id).order_by(World.updated_at.desc())).all()
    return {"worlds": [serialize_world(w) for w in worlds]}


@router.post("/worlds", status_code=201)
def new_world(data: WorldCreate, user: User = Depends(current_user), session: Session = Depends(get_db)) -> dict:
    world = create_world(session, user, data)
    return world_detail(session, world)


@router.get("/worlds/{world_id}")
def get_world(world_id: str, user: User = Depends(current_user), session: Session = Depends(get_db)) -> dict:
    return world_detail(session, owned_world(session, user, world_id))


@router.patch("/worlds/{world_id}")
def patch_world(world_id: str, data: WorldPatch, user: User = Depends(current_user), session: Session = Depends(get_db)) -> dict:
    world = owned_world(session, user, world_id)
    accessible_workspace(session, user, world.workspace_id, write=True)
    if data.name is not None:
        world.name = data.name.strip()
    if data.speed is not None:
        workspace = session.get(Workspace, world.workspace_id)
        billing_user = session.get(User, workspace.owner_id) if workspace else user
        max_speed = PLANS.get((billing_user or user).plan, PLANS["free"])["max_speed"]
        if user.role != "admin" and data.speed > max_speed:
            raise HTTPException(status_code=403, detail=f"plan allows simulation speed up to {max_speed}x")
        world.speed = data.speed
    audit(session, user.id, "world.update", world.id)
    session.commit()
    return {"world": serialize_world(world)}


@router.post("/worlds/{world_id}/start")
def start_world(world_id: str, user: User = Depends(current_user), session: Session = Depends(get_db)) -> dict:
    world = owned_world(session, user, world_id)
    accessible_workspace(session, user, world.workspace_id, write=True)
    world.status = "running"
    audit(session, user.id, "world.start", world.id)
    session.commit()
    return {"world": serialize_world(world)}


@router.post("/worlds/{world_id}/pause")
def pause_world(world_id: str, user: User = Depends(current_user), session: Session = Depends(get_db)) -> dict:
    world = owned_world(session, user, world_id)
    accessible_workspace(session, user, world.workspace_id, write=True)
    world.status = "paused"
    audit(session, user.id, "world.pause", world.id)
    session.commit()
    return {"world": serialize_world(world)}


@router.post("/worlds/{world_id}/tick")
def tick(world_id: str, data: TickRequest, user: User = Depends(current_user), session: Session = Depends(get_db)) -> dict:
    world = owned_world(session, user, world_id)
    accessible_workspace(session, user, world.workspace_id, write=True)
    if world.status == "paused":
        world.status = "running"
    tick_world(session, world, data.steps)
    audit(session, user.id, "world.tick", world.id, {"steps": data.steps})
    session.commit()
    return world_detail(session, world)


@router.delete("/worlds/{world_id}", status_code=204)
def delete_world(world_id: str, user: User = Depends(current_user), session: Session = Depends(get_db)):
    world = owned_world(session, user, world_id)
    accessible_workspace(session, user, world.workspace_id, write=True)
    audit(session, user.id, "world.delete", world.id)
    session.delete(world)
    session.commit()
    return None


@router.post("/worlds/{world_id}/agents", status_code=201)
def deploy_agent(world_id: str, data: AgentCreate, user: User = Depends(current_user), session: Session = Depends(get_db)) -> dict:
    world = owned_world(session, user, world_id)
    workspace = accessible_workspace(session, user, world.workspace_id, write=True)
    billing_user = session.get(User, workspace.owner_id) or user
    limit = PLANS.get(billing_user.plan, PLANS["free"])["agents_per_world"] if user.role != "admin" else 10000
    count = session.scalar(select(func.count(Agent.id)).where(Agent.world_id == world.id)) or 0
    if count >= limit:
        raise HTTPException(status_code=403, detail=f"agent limit reached ({limit})")
    rng = random.Random(world.seed + count * 131 + world.age)
    agent = Agent(
        world_id=world.id, name=data.name.strip(), role=data.role.strip().lower(), goal=data.goal.strip(),
        skills_json=json.dumps([x.strip() for x in data.skills if x.strip()][:12]),
        personality_json=json.dumps({"curiosity": round(rng.uniform(.4, 1), 2), "cooperation": round(rng.uniform(.35, 1), 2), "risk": round(rng.uniform(.2, .9), 2)}),
        energy=round(rng.uniform(75, 100), 2), knowledge=round(rng.uniform(5, 20), 2),
        influence=round(rng.uniform(3, 16), 2), wealth=round(rng.uniform(4, 20), 2),
        mood=round(rng.uniform(60, 90), 2), x=rng.random(), y=rng.random(),
    )
    session.add(agent)
    audit(session, user.id, "agent.deploy", agent.id, {"world_id": world.id, "role": agent.role})
    session.commit()
    session.refresh(agent)
    from .services import serialize_agent
    return {"agent": serialize_agent(agent)}


@router.post("/worlds/{world_id}/agents/{agent_id}/task")
def run_agent_task(world_id: str, agent_id: str, data: AgentTaskRequest, user: User = Depends(current_user), session: Session = Depends(get_db)) -> dict:
    world = owned_world(session, user, world_id)
    accessible_workspace(session, user, world.workspace_id, write=True)
    agent = session.scalar(select(Agent).where(Agent.id == agent_id, Agent.world_id == world.id))
    if not agent:
        raise HTTPException(status_code=404, detail="agent not found")
    cost = min(35.0, 3.0 + data.difficulty * 2.2)
    if agent.energy < cost:
        raise HTTPException(status_code=409, detail="agent does not have enough energy for this task")
    rng = random.Random(world.seed + world.age * 911 + sum(map(ord, data.task)))
    gain = round(data.difficulty * rng.uniform(.4, 1.1), 2)
    agent.energy = max(0.0, agent.energy - cost)
    agent.knowledge = min(100.0, agent.knowledge + gain)
    agent.influence = min(100.0, agent.influence + gain * .18)
    memory = json.loads(agent.memory_json or "[]")
    memory.append({"year": world.age, "task": data.task, "difficulty": data.difficulty, "knowledge_gain": gain})
    agent.memory_json = json.dumps(memory[-20:])
    audit(session, user.id, "agent.task", agent.id, {"world_id": world.id, "difficulty": data.difficulty})
    session.commit()
    from .services import serialize_agent
    return {"agent": serialize_agent(agent), "result": {"task": data.task, "knowledge_gain": gain, "status": "completed"}}


@router.get("/worlds/{world_id}/export")
def export_world(world_id: str, user: User = Depends(current_user), session: Session = Depends(get_db)) -> dict:
    world = owned_world(session, user, world_id)
    data = world_detail(session, world)
    data["export"] = {"format": "genesis-world-v1", "generated_at": datetime.now(timezone.utc).isoformat()}
    return data


@router.get("/workspace/members")
def workspace_members(workspace_id: str | None = None, user: User = Depends(current_user), session: Session = Depends(get_db)) -> dict:
    workspace = accessible_workspace(session, user, workspace_id)
    membership = session.scalar(select(WorkspaceMember).where(WorkspaceMember.workspace_id == workspace.id, WorkspaceMember.user_id == user.id))
    if user.role != "admin" and not membership:
        raise HTTPException(status_code=403, detail="workspace access required")
    rows = session.execute(select(WorkspaceMember, User).join(User, User.id == WorkspaceMember.user_id).where(WorkspaceMember.workspace_id == workspace.id).order_by(WorkspaceMember.created_at)).all()
    return {"workspace": {"id": workspace.id, "name": workspace.name}, "members": [{"id": m.id, "user_id": u.id, "name": u.name, "email": u.email, "role": m.role, "created_at": m.created_at.isoformat()} for m, u in rows]}


@router.post("/workspace/members", status_code=201)
def add_workspace_member(data: WorkspaceMemberCreate, workspace_id: str | None = None, user: User = Depends(current_user), session: Session = Depends(get_db)) -> dict:
    workspace = accessible_workspace(session, user, workspace_id)
    caller = session.scalar(select(WorkspaceMember).where(WorkspaceMember.workspace_id == workspace.id, WorkspaceMember.user_id == user.id))
    if user.role != "admin" and (not caller or caller.role != "admin"):
        raise HTTPException(status_code=403, detail="workspace admin role required")
    target = session.scalar(select(User).where(User.email == data.email.lower().strip()))
    if not target:
        raise HTTPException(status_code=404, detail="user must register before being added")
    existing = session.scalar(select(WorkspaceMember).where(WorkspaceMember.workspace_id == workspace.id, WorkspaceMember.user_id == target.id))
    if existing:
        existing.role = data.role
        member = existing
    else:
        member = WorkspaceMember(workspace_id=workspace.id, user_id=target.id, role=data.role)
        session.add(member)
    audit(session, user.id, "workspace.member.add", target.id, {"role": data.role})
    session.commit()
    return {"member": {"id": member.id, "user_id": target.id, "name": target.name, "email": target.email, "role": member.role}}


@router.delete("/workspace/members/{member_id}", status_code=204)
def remove_workspace_member(member_id: str, workspace_id: str | None = None, user: User = Depends(current_user), session: Session = Depends(get_db)):
    workspace = accessible_workspace(session, user, workspace_id)
    caller = session.scalar(select(WorkspaceMember).where(WorkspaceMember.workspace_id == workspace.id, WorkspaceMember.user_id == user.id))
    if user.role != "admin" and (not caller or caller.role != "admin"):
        raise HTTPException(status_code=403, detail="workspace admin role required")
    member = session.scalar(select(WorkspaceMember).where(WorkspaceMember.id == member_id, WorkspaceMember.workspace_id == workspace.id))
    if not member:
        raise HTTPException(status_code=404, detail="member not found")
    if member.user_id == workspace.owner_id:
        raise HTTPException(status_code=400, detail="workspace owner cannot be removed")
    audit(session, user.id, "workspace.member.remove", member.user_id)
    session.delete(member)
    session.commit()
    return None


@router.get("/api-keys")
def list_api_keys(user: User = Depends(current_user), session: Session = Depends(get_db)) -> dict:
    keys = session.scalars(select(ApiKey).where(ApiKey.user_id == user.id).order_by(ApiKey.created_at.desc())).all()
    return {"keys": [{"id": k.id, "name": k.name, "prefix": k.prefix, "last_used_at": k.last_used_at.isoformat() if k.last_used_at else None, "created_at": k.created_at.isoformat()} for k in keys]}


@router.post("/api-keys", status_code=201)
def create_api_key(data: ApiKeyCreate, user: User = Depends(current_user), session: Session = Depends(get_db)) -> dict:
    limit = PLANS.get(user.plan, PLANS["free"])["api_keys"]
    count = session.scalar(select(func.count(ApiKey.id)).where(ApiKey.user_id == user.id)) or 0
    if count >= limit:
        raise HTTPException(status_code=403, detail=f"{user.plan} plan API key limit reached")
    raw, prefix, digest = new_api_key()
    record = ApiKey(user_id=user.id, name=data.name, prefix=prefix, key_hash=digest)
    session.add(record)
    audit(session, user.id, "api_key.create", prefix)
    session.commit()
    return {"id": record.id, "name": record.name, "key": raw, "warning": "This key is shown once. Store it securely."}


@router.delete("/api-keys/{key_id}", status_code=204)
def delete_api_key(key_id: str, user: User = Depends(current_user), session: Session = Depends(get_db)):
    key = session.scalar(select(ApiKey).where(ApiKey.id == key_id, ApiKey.user_id == user.id))
    if not key:
        raise HTTPException(status_code=404, detail="API key not found")
    session.delete(key)
    audit(session, user.id, "api_key.delete", key.prefix)
    session.commit()
    return None


@router.get("/admin/stats")
def admin_stats(_: User = Depends(admin_user), session: Session = Depends(get_db)) -> dict:
    return {
        "users": session.scalar(select(func.count(User.id))) or 0,
        "worlds": session.scalar(select(func.count(World.id))) or 0,
        "running_worlds": session.scalar(select(func.count(World.id)).where(World.status == "running")) or 0,
        "agents": session.scalar(select(func.count(Agent.id))) or 0,
        "events": session.scalar(select(func.count(Event.id))) or 0,
    }


@router.get("/admin/users")
def admin_users(_: User = Depends(admin_user), session: Session = Depends(get_db)) -> dict:
    users = session.scalars(select(User).order_by(User.created_at.desc()).limit(250)).all()
    return {"users": [serialize_user(u) for u in users]}


@router.patch("/admin/users/{user_id}")
def admin_update_user(user_id: str, data: AdminUserPatch, admin: User = Depends(admin_user), session: Session = Depends(get_db)) -> dict:
    target = session.get(User, user_id)
    if not target:
        raise HTTPException(status_code=404, detail="user not found")
    if data.plan is not None:
        target.plan = data.plan
    if data.role is not None:
        if target.id == admin.id and data.role != "admin":
            raise HTTPException(status_code=400, detail="cannot remove your own admin role")
        target.role = data.role
    if data.is_active is not None:
        if target.id == admin.id and not data.is_active:
            raise HTTPException(status_code=400, detail="cannot deactivate your own account")
        target.is_active = data.is_active
    audit(session, admin.id, "admin.user.update", target.id, data.model_dump(exclude_none=True))
    session.commit()
    return {"user": serialize_user(target) | {"is_active": target.is_active}}


@router.get("/admin/worlds")
def admin_worlds(_: User = Depends(admin_user), session: Session = Depends(get_db)) -> dict:
    worlds = session.scalars(select(World).order_by(World.updated_at.desc()).limit(500)).all()
    return {"worlds": [serialize_world(w) for w in worlds]}


@router.get("/admin/audit")
def admin_audit(_: User = Depends(admin_user), session: Session = Depends(get_db)) -> dict:
    logs = session.scalars(select(AuditLog).order_by(AuditLog.created_at.desc()).limit(200)).all()
    return {"logs": [{"id": x.id, "user_id": x.user_id, "action": x.action, "target": x.target, "metadata": json.loads(x.metadata_json or "{}"), "created_at": x.created_at.isoformat()} for x in logs]}
