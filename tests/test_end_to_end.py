import importlib
import os
from pathlib import Path

TEST_DB = Path(__file__).resolve().parents[1] / "data" / "pytest.db"
if TEST_DB.exists():
    TEST_DB.unlink()
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"
os.environ["GENESIS_SECRET_KEY"] = "pytest-secret-key"
os.environ["GENESIS_AUTORUN"] = "0"
os.environ["GENESIS_ADMIN_EMAIL"] = "admin@test.local"
os.environ["GENESIS_ADMIN_PASSWORD"] = "AdminPassword123!"

from fastapi.testclient import TestClient
from genesis.app import app


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def test_full_saas_cycle():
    with TestClient(app) as client:
        assert client.get("/api/v1/health").status_code == 200

        reg = client.post("/api/v1/auth/register", json={
            "email": "founder@example.com", "name": "Founder", "password": "StrongPassword123"
        })
        assert reg.status_code == 200, reg.text
        token = reg.json()["token"]

        me = client.get("/api/v1/me", headers=auth_header(token))
        assert me.status_code == 200
        assert me.json()["user"]["plan"] == "free"

        created = client.post("/api/v1/worlds", headers=auth_header(token), json={
            "name": "Genesis Earth", "template": "genesis-earth", "population": 1000,
            "agent_count": 24, "seed": 42
        })
        assert created.status_code == 201, created.text
        world_id = created.json()["world"]["id"]
        assert len(created.json()["agents"]) == 24

        started = client.post(f"/api/v1/worlds/{world_id}/start", headers=auth_header(token))
        assert started.status_code == 200
        assert started.json()["world"]["status"] == "running"

        ticked = client.post(f"/api/v1/worlds/{world_id}/tick", headers=auth_header(token), json={"steps": 12})
        assert ticked.status_code == 200, ticked.text
        body = ticked.json()
        assert body["world"]["age"] == 12
        assert len(body["series"]) >= 13
        assert "summary" in body["analysis"]
        assert len(body["events"]) >= 2

        deployed = client.post(
            f"/api/v1/worlds/{world_id}/agents",
            headers=auth_header(token),
            json={"name": "Ada", "role": "researcher", "goal": "Study emergent institutions", "skills": ["research", "analysis"]},
        )
        assert deployed.status_code == 201, deployed.text
        agent = deployed.json()["agent"]
        assert agent["goal"] == "Study emergent institutions"
        tasked = client.post(
            f"/api/v1/worlds/{world_id}/agents/{agent['id']}/task",
            headers=auth_header(token),
            json={"task": "Map institutional feedback loops", "difficulty": 4},
        )
        assert tasked.status_code == 200, tasked.text
        assert tasked.json()["agent"]["memory_count"] >= 1

        api_key = client.post("/api/v1/api-keys", headers=auth_header(token), json={"name": "Test key"})
        assert api_key.status_code == 201, api_key.text
        raw_key = api_key.json()["key"]
        via_key = client.get("/api/v1/worlds", headers={"X-API-Key": raw_key})
        assert via_key.status_code == 200
        assert len(via_key.json()["worlds"]) == 1

        export = client.get(f"/api/v1/worlds/{world_id}/export", headers=auth_header(token))
        assert export.status_code == 200
        assert export.json()["export"]["format"] == "genesis-world-v1"

        # Workspace collaboration: a registered teammate can be granted access.
        teammate_reg = client.post("/api/v1/auth/register", json={
            "email": "teammate@example.com", "name": "Teammate", "password": "StrongPassword123"
        })
        teammate_token = teammate_reg.json()["token"]
        workspace_id = me.json()["workspace"]["id"]
        member = client.post(
            f"/api/v1/workspace/members?workspace_id={workspace_id}",
            headers=auth_header(token),
            json={"email": "teammate@example.com", "role": "researcher"},
        )
        assert member.status_code == 201, member.text
        team_worlds = client.get(
            f"/api/v1/worlds?workspace_id={workspace_id}", headers=auth_header(teammate_token)
        )
        assert team_worlds.status_code == 200, team_worlds.text
        assert team_worlds.json()["worlds"][0]["id"] == world_id

        # A viewer can inspect but cannot mutate a team world.
        viewer_reg = client.post("/api/v1/auth/register", json={
            "email": "viewer@example.com", "name": "Viewer", "password": "StrongPassword123"
        })
        viewer_token = viewer_reg.json()["token"]
        add_viewer = client.post(
            f"/api/v1/workspace/members?workspace_id={workspace_id}",
            headers=auth_header(token),
            json={"email": "viewer@example.com", "role": "viewer"},
        )
        assert add_viewer.status_code == 201
        assert client.get(f"/api/v1/worlds/{world_id}", headers=auth_header(viewer_token)).status_code == 200
        assert client.post(f"/api/v1/worlds/{world_id}/pause", headers=auth_header(viewer_token)).status_code == 403

        billing = client.get("/api/v1/billing/status", headers=auth_header(token))
        assert billing.status_code == 200
        assert billing.json()["provider"] == "manual"

        changed = client.post(
            "/api/v1/me/password",
            headers=auth_header(token),
            json={"current_password": "StrongPassword123", "new_password": "NewStrongPassword456"},
        )
        assert changed.status_code == 200
        new_token = changed.json()["token"]
        assert client.get("/api/v1/me", headers=auth_header(token)).status_code == 401
        assert client.get("/api/v1/me", headers=auth_header(new_token)).status_code == 200

        admin_login = client.post("/api/v1/auth/login", json={
            "email": "admin@test.local", "password": "AdminPassword123!"
        })
        assert admin_login.status_code == 200, admin_login.text
        admin_token = admin_login.json()["token"]
        stats = client.get("/api/v1/admin/stats", headers=auth_header(admin_token))
        assert stats.status_code == 200
        assert stats.json()["users"] >= 2
        assert stats.json()["worlds"] >= 1
        founder_id = me.json()["user"]["id"]
        upgraded = client.patch(
            f"/api/v1/admin/users/{founder_id}",
            headers=auth_header(admin_token),
            json={"plan": "creator"},
        )
        assert upgraded.status_code == 200
        assert upgraded.json()["user"]["plan"] == "creator"


def test_free_plan_limits():
    with TestClient(app) as client:
        reg = client.post("/api/v1/auth/register", json={
            "email": "limit@example.com", "name": "Limit User", "password": "StrongPassword123"
        })
        token = reg.json()["token"]
        h = auth_header(token)
        for i in range(2):
            res = client.post("/api/v1/worlds", headers=h, json={
                "name": f"World {i}", "template": "genesis-earth", "population": 1000, "agent_count": 4, "seed": i+1
            })
            assert res.status_code == 201
        third = client.post("/api/v1/worlds", headers=h, json={
            "name": "World 3", "template": "genesis-earth", "population": 1000, "agent_count": 4, "seed": 3
        })
        assert third.status_code == 403
