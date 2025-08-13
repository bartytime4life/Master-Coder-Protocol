# Deployment Plan

- Use Docker containers for services.
- Deploy via Kubernetes manifests in `full-stack/k8s`.
- CI/CD pipeline builds images and runs tests.
- Configuration managed via environment variables.
- Monitor with Prometheus/Grafana; log with ELK stack.
- Database backups nightly.
- Model rollout via blue-green deployment.
- Known issues: scale testing pending.
