# Billing integration

Genesis enforces plan entitlements independently of a payment provider. This allows self-hosted pilots and manually invoiced enterprise customers without Stripe.

## Manual mode

If `STRIPE_SECRET_KEY` is empty, `/api/v1/billing/status` reports `provider: manual`. Administrators can assign Free, Creator, Professional or Enterprise plans from the Admin console.

## Stripe mode

Install the optional dependency:

```bash
. .venv/bin/activate
pip install -r requirements-billing.txt
```

Configure:

```text
GENESIS_PUBLIC_URL=https://your-domain.example
STRIPE_SECRET_KEY=...
STRIPE_WEBHOOK_SECRET=...
STRIPE_PRICE_CREATOR=price_...
STRIPE_PRICE_PROFESSIONAL=price_...
```

Configure the Stripe webhook to send Checkout/Subscription events to:

```text
https://your-domain.example/api/v1/billing/webhook
```

The integration creates subscription Checkout Sessions with user/plan metadata. Completed checkout updates the Genesis plan. Subscription cancellation or an inactive subscription returns the account to the Free plan.

Never place real Stripe secrets in the distributable source archive or commit them to version control.
