.PHONY: install lint test format run-ci

install:
python -m pip install -e ".[all]"

format:
python -m pip install ruff black
ruff check --select I --fix .
black .

lint:
python -m pip install ruff
ruff check .

test:
pytest -q

run-ci: lint test
echo "CI checks complete."
