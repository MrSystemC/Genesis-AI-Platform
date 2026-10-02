from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import Agent, Event, Snapshot, World, utcnow

ROLES = [
    "researcher", "engineer", "entrepreneur", "planner", "diplomat",
    "analyst", "builder", "educator", "operator", "scientist",
]

ROLE_PROFILES = {
    "researcher": ("Expand the world knowledge frontier", ["research", "hypothesis", "synthesis"]),
    "engineer": ("Convert knowledge into reliable systems", ["engineering", "automation", "systems"]),
    "entrepreneur": ("Create organizations and economic value", ["markets", "strategy", "organization"]),
    "planner": ("Coordinate long-horizon development", ["planning", "resources", "forecasting"]),
    "diplomat": ("Improve cooperation between groups", ["negotiation", "governance", "communication"]),
    "analyst": ("Detect patterns and system risks", ["analysis", "metrics", "scenarios"]),
    "builder": ("Expand physical and digital infrastructure", ["construction", "operations", "logistics"]),
    "educator": ("Diffuse knowledge through the population", ["teaching", "communication", "knowledge"]),
    "operator": ("Keep organizations and infrastructure reliable", ["operations", "reliability", "coordination"]),
    "scientist": ("Discover new scientific capabilities", ["science", "experiments", "discovery"]),
}

EVENT_CATALOG = {
    "innovation": (
        "Technology breakthrough",
        "A research network converted accumulated knowledge into a new technological capability.",
    ),
    "market": (
        "New market formed",
        "Agents coordinated around a new exchange network, increasing economic activity.",
    ),
    "social": (
        "Civic coalition emerged",
        "A new coalition formed around shared objectives and improved coordination.",
    ),
    "resource": (
        "Resource pressure detected",
        "Consumption temporarily outpaced replenishment and forced adaptive behavior.",
    ),
    "governance": (
        "Governance reform",
        "Institutions adjusted decision rules in response to changing social conditions.",
    ),
    "crisis": (
        "Systemic disruption",
        "A short-lived disruption reduced stability and triggered recovery behavior.",
    ),
}


def clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return round(max(lo, min(hi, value)), 2)


def spawn_agents(session: Session, world: World, count: int) -> None:
    rng = random.Random(world.seed)
    for i in range(count):
        role = ROLES[i % len(ROLES)]
        goal, skills = ROLE_PROFILES[role]
        session.add(
            Agent(
                world_id=world.id,
                name=f"{role.title()}-{i + 1:03d}",
                role=role,
                goal=goal,
                skills_json=json.dumps(skills),
                personality_json=json.dumps({"curiosity": round(rng.uniform(0.4, 1.0), 2), "cooperation": round(rng.uniform(0.35, 1.0), 2), "risk": round(rng.uniform(0.2, 0.9), 2)}),
                energy=round(rng.uniform(72, 100), 2),
                knowledge=round(rng.uniform(5, 24), 2),
                influence=round(rng.uniform(2, 20), 2),
                wealth=round(rng.uniform(4, 24), 2),
                mood=round(rng.uniform(55, 92), 2),
                x=rng.random(),
                y=rng.random(),
            )
        )


def snapshot(session: Session, world: World) -> None:
    session.add(
        Snapshot(
            world_id=world.id,
            year=world.age,
            population=world.population,
            economy=world.economy,
            technology=world.technology,
            stability=world.stability,
            resources=world.resources,
            knowledge=world.knowledge,
        )
    )


def create_event(session: Session, world: World, kind: str, impact: str, payload: dict | None = None) -> Event:
    title, description = EVENT_CATALOG[kind]
    event = Event(
        world_id=world.id,
        year=world.age,
        kind=kind,
        title=title,
        description=description,
        impact=impact,
        payload_json=json.dumps(payload or {}, separators=(",", ":")),
    )
    session.add(event)
    return event


def _apply_event(world: World, kind: str, rng: random.Random) -> None:
    if kind == "innovation":
        world.technology = clamp(world.technology + rng.uniform(1.0, 3.2))
        world.knowledge = clamp(world.knowledge + rng.uniform(0.8, 2.2))
    elif kind == "market":
        world.economy = clamp(world.economy + rng.uniform(1.2, 3.0))
    elif kind == "social":
        world.stability = clamp(world.stability + rng.uniform(0.7, 2.2))
    elif kind == "resource":
        world.resources = clamp(world.resources - rng.uniform(1.0, 4.0))
        world.stability = clamp(world.stability - rng.uniform(0.2, 1.4))
    elif kind == "governance":
        world.stability = clamp(world.stability + rng.uniform(0.8, 2.5))
        world.economy = clamp(world.economy + rng.uniform(0.2, 1.2))
    elif kind == "crisis":
        world.stability = clamp(world.stability - rng.uniform(2.0, 6.0))
        world.economy = clamp(world.economy - rng.uniform(0.8, 3.2))


def tick_world(session: Session, world: World, steps: int = 1) -> World:
    for _ in range(steps):
        if world.status not in {"running", "created"}:
            break
        rng = random.Random(world.seed * 1_000_003 + (world.age + 1) * 97)
        world.age += 1

        knowledge_gain = 0.17 + world.technology * 0.004 + rng.uniform(-0.03, 0.10)
        world.knowledge = clamp(world.knowledge + knowledge_gain)
        tech_gain = 0.06 + world.knowledge * 0.003 + rng.uniform(-0.02, 0.08)
        world.technology = clamp(world.technology + tech_gain)

        resource_pressure = 0.05 + (world.population / 1_000_000) * 0.2
        regen = 0.035 + world.technology * 0.0008
        world.resources = clamp(world.resources + regen - resource_pressure + rng.uniform(-0.08, 0.08))

        growth = 0.0035 + (world.stability - 50) / 50_000 + rng.uniform(-0.0012, 0.0015)
        growth *= max(0.35, world.resources / 100)
        world.population = max(10, int(world.population * (1 + growth)))

        economic_gain = 0.08 + world.technology * 0.002 + world.stability * 0.001 + rng.uniform(-0.20, 0.24)
        world.economy = clamp(world.economy + economic_gain)
        stability_delta = (world.resources - 50) * 0.002 + (world.economy - 50) * 0.001 + rng.uniform(-0.22, 0.22)
        world.stability = clamp(world.stability + stability_delta)

        agents = session.scalars(select(Agent).where(Agent.world_id == world.id)).all()
        for agent in agents:
            agent.energy = clamp(agent.energy + rng.uniform(-2.5, 1.8))
            agent.knowledge = clamp(agent.knowledge + 0.05 + world.knowledge * 0.001 + rng.uniform(0, 0.15))
            agent.influence = clamp(agent.influence + rng.uniform(-0.15, 0.35))
            agent.wealth = clamp(agent.wealth + (world.economy - 45) * 0.006 + rng.uniform(-0.3, 0.5))
            agent.mood = clamp(agent.mood + (world.stability - 50) * 0.004 + rng.uniform(-0.5, 0.5))
            agent.x = max(0.02, min(0.98, agent.x + rng.uniform(-0.025, 0.025)))
            agent.y = max(0.02, min(0.98, agent.y + rng.uniform(-0.025, 0.025)))
            memory = json.loads(agent.memory_json or "[]")
            if rng.random() < 0.035:
                memory.append({"year": world.age, "note": f"Adapted as {agent.role}"})
                agent.memory_json = json.dumps(memory[-20:])

        event_probability = 0.24 + world.technology / 650
        if world.age % 5 == 0 or rng.random() < event_probability:
            kinds = ["innovation", "market", "social", "resource", "governance", "crisis"]
            weights = [1.3, 1.2, 1.0, 0.8, 0.9, 0.45]
            kind = rng.choices(kinds, weights=weights, k=1)[0]
            impact = "high" if rng.random() < 0.20 else "medium" if rng.random() < 0.65 else "low"
            _apply_event(world, kind, rng)
            create_event(session, world, kind, impact, {"economy": world.economy, "technology": world.technology})

        world.updated_at = utcnow()
        # Keep early history granular while preventing unbounded high-speed snapshot growth.
        keep_snapshot = world.age <= 500 or (world.age <= 10_000 and world.age % 5 == 0) or world.age % 25 == 0
        if keep_snapshot:
            snapshot(session, world)
    session.commit()
    session.refresh(world)
    return world


def world_analysis(world: World, events: list[Event]) -> dict:
    signals: list[str] = []
    risks: list[str] = []
    opportunities: list[str] = []

    if world.technology > 65:
        signals.append("The world has entered an advanced technology regime.")
        opportunities.append("Increase knowledge-intensive institutions and high-skill agent roles.")
    elif world.knowledge > 40:
        signals.append("Knowledge accumulation is outpacing technology conversion.")
        opportunities.append("Create research and commercialization loops to convert knowledge into technology.")
    else:
        signals.append("The civilization remains in an early capability-building phase.")

    if world.resources < 35:
        risks.append("Resource availability is approaching a constraint on population and economic growth.")
    if world.stability < 45:
        risks.append("Low social stability increases the probability of disruptive events.")
    if world.economy > 70 and world.resources < 50:
        risks.append("Economic growth is consuming resources faster than the system can replenish them.")
    if not risks:
        risks.append("No critical systemic risk is visible in the current state; continue scenario stress-testing.")

    if world.economy > 60:
        opportunities.append("The economy can support broader specialization and new organization formation.")
    if world.stability > 75:
        opportunities.append("High stability creates room for longer-horizon research and infrastructure investment.")

    recent = [e.kind for e in events[:12]]
    return {
        "summary": signals[0],
        "signals": signals,
        "risks": risks,
        "opportunities": opportunities[:4],
        "recent_event_mix": {kind: recent.count(kind) for kind in sorted(set(recent))},
        "confidence": "scenario-derived, not a real-world forecast",
    }
