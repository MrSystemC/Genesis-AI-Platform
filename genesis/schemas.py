from __future__ import annotations

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    email: str = Field(min_length=5, max_length=320)
    name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=10, max_length=200)


class LoginRequest(BaseModel):
    email: str = Field(min_length=5, max_length=320)
    password: str


class WorldCreate(BaseModel):
    workspace_id: str | None = None
    name: str = Field(min_length=2, max_length=160)
    description: str = Field(default="", max_length=2000)
    template: str = Field(default="genesis-earth", max_length=64)
    population: int = Field(default=1000, ge=10, le=10_000_000)
    agent_count: int = Field(default=36, ge=4, le=250)
    seed: int = Field(default=1, ge=1, le=2_147_483_647)


class WorldPatch(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=160)
    speed: int | None = Field(default=None, ge=1, le=20)


class TickRequest(BaseModel):
    steps: int = Field(default=1, ge=1, le=100)


class ApiKeyCreate(BaseModel):
    name: str = Field(default="Default", min_length=2, max_length=120)


class ProfilePatch(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)

class WorkspaceMemberCreate(BaseModel):
    email: str = Field(min_length=5, max_length=320)
    role: str = Field(default="viewer", pattern="^(admin|developer|researcher|viewer)$")


class AdminUserPatch(BaseModel):
    plan: str | None = Field(default=None, pattern="^(free|creator|professional|enterprise)$")
    role: str | None = Field(default=None, pattern="^(user|admin)$")
    is_active: bool | None = None


class CheckoutRequest(BaseModel):
    plan: str = Field(pattern="^(creator|professional)$")

class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(min_length=10, max_length=200)


class AgentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    role: str = Field(default="researcher", min_length=2, max_length=64)
    goal: str = Field(default="Learn and contribute", min_length=3, max_length=240)
    skills: list[str] = Field(default_factory=list, max_length=12)


class AgentTaskRequest(BaseModel):
    task: str = Field(min_length=3, max_length=500)
    difficulty: int = Field(default=3, ge=1, le=10)
