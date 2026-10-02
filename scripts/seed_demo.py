#!/usr/bin/env python3
from __future__ import annotations

import argparse
import secrets
import string
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from sqlalchemy import select

from genesis.database import SessionLocal, User, World, init_db
from genesis.engine import tick_world
from genesis.schemas import WorldCreate
from genesis.security import hash_password
from genesis.services import create_world, ensure_workspace


def generated_password() -> str:
    alphabet = string.ascii_letters + string.digits + "-_!@"
    return "D!" + "".join(secrets.choice(alphabet) for _ in range(18)) + "7"


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an investor/demo Genesis world")
    parser.add_argument("--email", default="demo@genesis.local")
    parser.add_argument("--password", default="")
    parser.add_argument("--years", type=int, default=40)
    args = parser.parse_args()
    password = args.password or generated_password()

    init_db()
    with SessionLocal() as session:
        user = session.scalar(select(User).where(User.email == args.email.lower()))
        created_user = False
        if not user:
            user = User(
                email=args.email.lower(),
                name="Genesis Demo",
                password_hash=hash_password(password),
                role="user",
                plan="creator",
            )
            session.add(user)
            session.flush()
            ensure_workspace(session, user)
            created_user = True

        workspace = ensure_workspace(session, user)
        world = session.scalar(select(World).where(World.workspace_id == workspace.id, World.name == "Genesis Earth Demo"))
        if not world:
            world = create_world(
                session,
                user,
                WorldCreate(
                    workspace_id=workspace.id,
                    name="Genesis Earth Demo",
                    description="Pre-seeded autonomous civilization for product demonstrations.",
                    template="genesis-earth",
                    population=25_000,
                    agent_count=64,
                    seed=20261001,
                ),
            )
            world.status = "running"
            session.commit()
            tick_world(session, world, max(1, min(args.years, 200)))
            world.status = "paused"
            session.commit()

    print("Demo environment ready")
    print(f"Email: {args.email.lower()}")
    if created_user:
        print(f"Password: {password}")
    else:
        print("Existing demo account reused; password was not changed.")


if __name__ == "__main__":
    main()
