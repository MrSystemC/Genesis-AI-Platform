from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from .config import settings
from .database import User
from .services import audit


def _stripe():
    try:
        import stripe  # type: ignore
    except ImportError as exc:
        raise HTTPException(
            status_code=503,
            detail="Stripe support is not installed. Install requirements-billing.txt.",
        ) from exc
    if not settings.stripe_secret_key:
        raise HTTPException(status_code=503, detail="Stripe is not configured")
    stripe.api_key = settings.stripe_secret_key
    return stripe


def provider_status() -> dict:
    return {
        "provider": "stripe" if settings.stripe_secret_key else "manual",
        "checkout_enabled": bool(
            settings.stripe_secret_key
            and settings.stripe_price_creator
            and settings.stripe_price_professional
        ),
        "webhook_configured": bool(settings.stripe_webhook_secret),
    }


def create_checkout(user: User, plan: str) -> dict:
    stripe = _stripe()
    price_map = {
        "creator": settings.stripe_price_creator,
        "professional": settings.stripe_price_professional,
    }
    price_id = price_map.get(plan)
    if not price_id:
        raise HTTPException(status_code=503, detail=f"Stripe price for {plan} is not configured")
    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=f"{settings.public_url}/?billing=success",
        cancel_url=f"{settings.public_url}/?billing=cancelled",
        customer=user.billing_customer_id or None,
        customer_email=None if user.billing_customer_id else user.email,
        client_reference_id=user.id,
        metadata={"user_id": user.id, "plan": plan},
        subscription_data={"metadata": {"user_id": user.id, "plan": plan}},
        allow_promotion_codes=True,
    )
    return {"checkout_url": session.url, "provider": "stripe"}


def process_webhook(payload: bytes, signature: str, session: Session) -> dict:
    stripe = _stripe()
    if not settings.stripe_webhook_secret:
        raise HTTPException(status_code=503, detail="Stripe webhook is not configured")
    try:
        event = stripe.Webhook.construct_event(payload, signature, settings.stripe_webhook_secret)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="invalid Stripe webhook signature") from exc

    event_type = event.get("type")
    obj = event.get("data", {}).get("object", {})
    metadata = obj.get("metadata", {}) or {}
    user_id = metadata.get("user_id") or obj.get("client_reference_id")
    plan = metadata.get("plan")

    user = session.get(User, user_id) if user_id else None
    if event_type == "checkout.session.completed" and user:
        if plan in {"creator", "professional", "enterprise"}:
            user.plan = plan
        user.billing_customer_id = obj.get("customer") or user.billing_customer_id
        user.billing_subscription_id = obj.get("subscription") or user.billing_subscription_id
        audit(session, user.id, "billing.checkout.completed", str(obj.get("id", "")), {"plan": user.plan})
        session.commit()
    elif event_type in {"customer.subscription.updated", "customer.subscription.deleted"} and user:
        status = obj.get("status")
        if event_type.endswith("deleted") or status not in {"active", "trialing"}:
            user.plan = "free"
        elif plan in {"creator", "professional", "enterprise"}:
            user.plan = plan
        user.billing_subscription_id = obj.get("id") or user.billing_subscription_id
        audit(session, user.id, "billing.subscription.sync", str(obj.get("id", "")), {"status": status, "plan": user.plan})
        session.commit()

    return {"received": True, "type": event_type}
