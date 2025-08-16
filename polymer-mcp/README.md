# Master Coder Protocol — Polymers

A full, production-grade module to accelerate polymer R&D with data schemas (BigSMILES-ready), physics guardrails, ML training and calibration, simulation stubs, inverse design, and HTML reporting. Typer CLI, Hydra configs, reproducibility logging, and CI included.

## Quickstart

```bash
# optional venv
python -m venv .venv && source .venv/bin/activate

pip install -e ".[all]"
polymerlab --help
```

## Common Commands

```bash
# Validate data against schema
polymerlab data validate --in data/raw/example_polymer.json

# Parse raw → interim (validated) and featurize → processed/features.csv
polymerlab data featurize --in data/interim --out data/processed

# Train Tg regressor and save run under runs/<name>
polymerlab train fit --config conf/ml/tg_regressor.yaml

# Conformal calibration on held-out or validation split
polymerlab train calibrate --run-dir runs/tg_regressor_default

# Physics rule checks on processed feature CSV
polymerlab rules check --in data/processed/features.csv --rules conf/rules/physics.yaml

# MD cooling simulation (stub) to estimate Tg and plots
polymerlab sim md --config conf/sim/md_tg.yaml

# Inverse design loop (stub) using trained model
polymerlab inverse bo --target Tg_C --run-dir runs/tg_regressor_default

# Generate an HTML report of a run
polymerlab eval report --run-dir runs/tg_regressor_default --out reports/html/run_default.html
```

## Layout

```
polymer-mcp/
  conf/                 # Hydra-style configs
  data/                 # raw → interim → processed
  reports/              # logs, figures, html
  runs/                 # training runs and artifacts
  src/polymerlab/       # package: CLI, IO, features, models, physics, UQ, sim, inverse, eval, logging
  tests/                # unit tests and smoke tests
```

## License

MIT
