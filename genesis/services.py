from __future__ import annotations

import json
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .database import Agent, ApiKey, AuditLog, Event, Snapshot, User, Workspace, WorkspaceMember, World
from .engine import spawn_agents, snapshot, tick_world, world_analysis
from .plans import PLANS
from .schemas import WorldCreate
from .security import new_api_key

TEMPLATES = {
    "genesis-earth": {
        "name": "Genesis Earth",
        "description": "Balanced autonomous civilization with research, markets, governance and resource pressure.",
        "economy": 50.0, "technology": 12.0, "stability": 76.0, "resources": 82.0, "knowledge": 14.0,
    },
    "market-lab": {
        "name": "Market Lab",
        "description": "Economy-first scenario for competitive organizations, capital formation and market events.",
        "economy": 68.0, "technology": 28.0, "stability": 69.0, "resources": 70.0, "knowledge": 24.0,
    },
    "workforce-lab": {
        "name": "AI Workforce Lab",
        "description": "Agent-heavy scenario focused on specialization, knowledge transfer and organizational behavior.",
        "economy": 58.0, "technology": 38.0, "stability": 74.0, "resources": 76.0, "knowledge": 44.0,
    },
    "stress-test": {
        "name": "Civilization Stress Test",
        "description": "Low-resource, lower-stability scenario for recovery and resilience experiments.",
        "economy": 42.0, "technology": 24.0, "stability": 48.0, "resources": 34.0, "knowledge": 26.0,
    },
}


def audit(session: Session, user_id: str | None, action: str, target: str = "", metadata: dict | None = None) -> None:
    session.add(AuditLog(user_id=user_id, action=action, target=target, metadata_json=json.dumps(metadata or {})))


def ensure_workspace(session: Session, user: User) -> Workspace:
    workspace = session.scalar(select(Workspace).where(Workspace.owner_id == user.id).order_by(Workspace.created_at))
    if workspace:
        return workspace
    workspace = Workspace(owner_id=user.id, name=f"{user.name}'s Workspace")
    session.add(workspace)
    session.flush()
    session.add(WorkspaceMember(workspace_id=workspace.id, user_id=user.id, role="admin"))
    session.commit()
    session.refresh(workspace)
    return workspace



def accessible_workspace(session: Session, user: User, workspace_id: str | None = None, write: bool = False) -> Workspace:
    if workspace_id is None:
        return ensure_workspace(session, user)
    workspace = session.get(Workspace, workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="workspace not found")
    if user.role == "admin":
        return workspace
    membership = session.scalar(select(WorkspaceMember).where(WorkspaceMember.workspace_id == workspace.id, WorkspaceMember.user_id == user.id))
    if not membership:
        raise HTTPException(status_code=403, detail="workspace access required")
    if write and membership.role not in {"admin", "developer", "researcher"}:
        raise HTTPException(status_code=403, detail="workspace write access required")
    return workspace


def serialize_user(user: User) -> dict:
    return {"id": user.id, "email": user.email, "name": user.name, "role": user.role, "plan": user.plan, "is_active": user.is_active, "created_at": user.created_at.isoformat()}


def serialize_world(world: World) -> dict:
    return {
        "id": world.id, "workspace_id": world.workspace_id, "name": world.name,
        "description": world.description, "template": world.template, "status": world.status,
        "age": world.age, "population": world.population, "economy": round(world.economy, 2),
        "technology": round(world.technology, 2), "stability": round(world.stability, 2),
        "resources": round(world.resources, 2), "knowledge": round(world.knowledge, 2),
        "speed": world.speed, "seed": world.seed,
        "created_at": world.created_at.isoformat(), "updated_at": world.updated_at.isoformat(),
    }


def serialize_agent(agent: Agent) -> dict:
    return {
        "id": agent.id, "name": agent.name, "role": agent.role, "goal": agent.goal,
        "skills": json.loads(agent.skills_json or "[]"),
        "personality": json.loads(agent.personality_json or "{}"),
        "energy": round(agent.energy, 2), "knowledge": round(agent.knowledge, 2),
        "influence": round(agent.influence, 2), "wealth": round(agent.wealth, 2),
        "mood": round(agent.mood, 2), "x": agent.x, "y": agent.y, "status": agent.status,
        "memory_count": len(json.loads(agent.memory_json or "[]")),
    }


def serialize_event(event: Event) -> dict:
    return {
        "id": event.id, "year": event.year, "kind": event.kind, "title": event.title,
        "description": event.description, "impact": event.impact,
        "payload": json.loads(event.payload_json or "{}"), "created_at": event.created_at.isoformat(),
    }


def create_world(session: Session, user: User, data: WorldCreate) -> World:
    workspace = accessible_workspace(session, user, data.workspace_id, write=True)
    billing_user = session.get(User, workspace.owner_id) or user
    limits = PLANS.get(billing_user.plan, PLANS["free"])
    existing = session.scalar(select(func.count(World.id)).where(World.workspace_id == workspace.id)) or 0
    if existing >= limits["worlds"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{billing_user.plan} plan world limit reached")
    if data.agent_count > limits["agents_per_world"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{billing_user.plan} plan allows at most {limits['agents_per_world']} agents per world")
    template = TEMPLATES.get(data.template, TEMPLATES["genesis-earth"])
    world = World(
        workspace_id=workspace.id, name=data.name, description=data.description or template["description"],
        template=data.template if data.template in TEMPLATES else "custom", population=data.population,
        seed=data.seed, economy=template["economy"], technology=template["technology"],
        stability=template["stability"], resources=template["resources"], knowledge=template["knowledge"],
    )
    session.add(world)
    session.flush()
    spawn_agents(session, world, data.agent_count)
    snapshot(session, world)
    audit(session, user.id, "world.create", world.id, {"template": data.template, "agents": data.agent_count})
    session.commit()
    session.refresh(world)
    return world


def owned_world(session: Session, user: User, world_id: str) -> World:
    query = select(World).where(World.id == world_id)
    if user.role != "admin":
        query = query.join(WorkspaceMember, WorkspaceMember.workspace_id == World.workspace_id).where(WorkspaceMember.user_id == user.id)
    world = session.scalar(query)
    if not world:
        raise HTTPException(status_code=404, detail="world not found")
    return world


def world_detail(session: Session, world: World) -> dict:
    agents = session.scalars(select(Agent).where(Agent.world_id == world.id).order_by(Agent.influence.desc()).limit(250)).all()
    events = session.scalars(select(Event).where(Event.world_id == world.id).order_by(Event.year.desc(), Event.created_at.desc()).limit(40)).all()
    snapshots = session.scalars(select(Snapshot).where(Snapshot.world_id == world.id).order_by(Snapshot.year.desc()).limit(120)).all()
    ordered = list(reversed(snapshots))
    return {
        "world": serialize_world(world),
        "agents": [serialize_agent(a) for a in agents],
        "events": [serialize_event(e) for e in events],
        "series": [{"year": s.year, "population": s.population, "economy": s.economy, "technology": s.technology, "stability": s.stability, "resources": s.resources, "knowledge": s.knowledge} for s in ordered],
        "analysis": world_analysis(world, events),
    }
