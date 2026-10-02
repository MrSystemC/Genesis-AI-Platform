# Product definition

## Category

Genesis AI Platform is a **simulation infrastructure SaaS** for autonomous AI worlds and organizations. It combines an agent runtime, persistent scenario environments, civilization/economy dynamics, observability and a commercial control plane.

It is deliberately positioned above a game or one-off simulator: a user creates a workspace, instantiates worlds, runs autonomous processes, observes agent/system behavior, exports the result and can integrate the platform over API.

## Who it is for

### AI and agent developers
Use persistent multi-agent environments to test long-horizon behavior, memory, coordination and emergent system dynamics.

### Research teams and universities
Build repeatable experiments around agent societies, economics, governance, resource pressure and institutional behavior.

### Product and strategy teams
Run **scenario experiments** to explore assumptions before committing real resources. Genesis does not claim real-world predictive accuracy unless a customer supplies and validates an appropriate domain model and data.

### Game and simulation studios
Use the world/agent/event model as a foundation for living worlds and persistent non-player societies.

### Enterprise innovation teams
Create private workspaces, reusable scenario templates, API integrations and controlled access for teams.

## Core value created

1. **Cheaper experimentation** — test many internally consistent scenarios before running expensive real-world pilots.
2. **Observability for autonomous systems** — see world state, event history and agent-level signals instead of treating agent systems as black boxes.
3. **Reusable simulation infrastructure** — auth, tenancy, lifecycle, API keys, exports and admin controls are already part of the product.
4. **Persistent institutional memory** — events and snapshots create a history that can be analyzed across long-running experiments.
5. **A platform for extensions** — market templates, specialized engines and external models can be added without rebuilding the SaaS layer.

## Monetization model

The release contains enforceable product entitlements for four tiers:

| Plan | Intended user | Included worlds | Representative agents/world | API keys | Indicative monthly price |
| --- | --- | ---: | ---: | ---: | ---: |
| Free | evaluation | 2 | 48 | 1 | $0 |
| Creator | developers | 10 | 100 | 5 | $49 |
| Professional | teams/research | 50 | 250 | 20 | $499 |
| Enterprise | private deployments | 1000 | 1000 | 100 | custom |

These are product packaging defaults, not a revenue forecast. Actual pricing should be tested against compute cost, customer willingness to pay and support burden.

## Revenue paths

- recurring subscriptions;
- metered simulation compute in a later worker-based deployment;
- enterprise private deployment / SLA contracts;
- professional services for calibrated domain scenarios;
- marketplace commission on scenario and agent templates;
- API usage for external products built on Genesis.

## Commercial constraint to understand

The software can launch today as a self-hosted or manually billed SaaS. **Automated card collection is not enabled without a payment-provider account and secret credentials.** That is an external account dependency, not something that can be safely embedded in a source archive. The plan/entitlement layer is already separated so Stripe or another provider can be connected without redesigning the product.
