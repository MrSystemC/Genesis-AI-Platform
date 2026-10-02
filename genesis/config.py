from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("GENESIS_APP_NAME", "Genesis AI Platform")
    environment: str = os.getenv("GENESIS_ENV", "development")
    secret_key: str = os.getenv("GENESIS_SECRET_KEY", "change-me-before-production")
    database_url: str = os.getenv(
        "DATABASE_URL", f"sqlite:///{ROOT / 'data' / 'genesis.db'}"
    )
    token_ttl_seconds: int = _int("GENESIS_TOKEN_TTL_SECONDS", 86400)
    autorun: bool = _bool("GENESIS_AUTORUN", True)
    tick_interval_seconds: float = float(os.getenv("GENESIS_TICK_INTERVAL_SECONDS", "2"))
    allow_registration: bool = _bool("GENESIS_ALLOW_REGISTRATION", True)
    demo_mode: bool = _bool("GENESIS_DEMO_MODE", True)
    admin_email: str = os.getenv("GENESIS_ADMIN_EMAIL", "")
    admin_password: str = os.getenv("GENESIS_ADMIN_PASSWORD", "")
    public_url: str = os.getenv("GENESIS_PUBLIC_URL", "http://127.0.0.1:8000").rstrip("/")
    stripe_secret_key: str = os.getenv("STRIPE_SECRET_KEY", "")
    stripe_webhook_secret: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    stripe_price_creator: str = os.getenv("STRIPE_PRICE_CREATOR", "")
    stripe_price_professional: str = os.getenv("STRIPE_PRICE_PROFESSIONAL", "")
    trusted_hosts: tuple[str, ...] = tuple(
        x.strip() for x in os.getenv("GENESIS_TRUSTED_HOSTS", "*").split(",") if x.strip()
    )


settings = Settings()
