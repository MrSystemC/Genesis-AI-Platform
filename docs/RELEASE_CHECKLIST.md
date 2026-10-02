# Release checklist

## Already covered by the release

- [x] Single production entrypoint.
- [x] Responsive web console.
- [x] Animated simulation visualization.
- [x] Accounts and signed sessions.
- [x] Workspaces and member roles.
- [x] World lifecycle and persistent simulation state.
- [x] Agent registry and live agent metrics.
- [x] Event history and state timeline.
- [x] Scenario-derived analytics.
- [x] API keys and OpenAPI docs.
- [x] Entitlement/plan limits.
- [x] Admin statistics, user plan control and audit log.
- [x] Docker, Linux and Termux launch paths.
- [x] End-to-end automated tests.
- [x] Legacy source lineage isolated from production.

## Operator-supplied items for a public commercial launch

These cannot be safely embedded in a distributable archive because they belong to the operator's external accounts/infrastructure:

- [ ] production domain and DNS;
- [ ] TLS certificate / managed HTTPS;
- [ ] strong production secrets;
- [ ] transactional email provider if public signup/password recovery is required;
- [ ] payment provider account and private API keys for automated card billing;
- [ ] legal documents applicable to the operator/jurisdiction (Terms, Privacy Policy, DPA as needed);
- [ ] production monitoring/error-reporting account if desired;
- [ ] backup destination and retention policy.

The platform can run before those integrations in self-hosted, demo, pilot or manually invoiced enterprise mode.
