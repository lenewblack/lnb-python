# CLAUDE.md

## Release Workflow

1. **Update CHANGELOG.md** — move items from `[Unreleased]` into a new version section using [Keep a Changelog](https://keepachangelog.com) format. Update the comparison links at the bottom.

2. **Bump the version** in two places:
   - `src/lnb/_version.py` → `__version__ = "X.Y.Z"`
   - `pyproject.toml` → `version = "X.Y.Z"`

3. **Commit** the changes:
   ```bash
   git add CHANGELOG.md src/lnb/_version.py pyproject.toml
   git commit -m "chore: release vX.Y.Z"
   ```

4. **Tag and push**:
   ```bash
   git tag vX.Y.Z
   git push origin develop
   git push origin vX.Y.Z
   ```

5. The `release.yml` workflow triggers automatically on version tags, runs the test suite, and publishes a GitHub Release.

## Versioning

This project follows [Semantic Versioning](https://semver.org):

- **PATCH** (`0.1.x`) — bug fixes, no API changes
- **MINOR** (`0.x.0`) — new backwards-compatible features or new resource methods
- **MAJOR** (`x.0.0`) — breaking changes (renamed methods, removed parameters, changed model fields)

## CI

- `ci.yml` — runs on every push and pull request; executes the test suite on Python 3.9, 3.10, 3.11, and 3.12
- `release.yml` — triggers on `v*` tags; runs tests then publishes a GitHub Release

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Type check
mypy src/lnb

# Lint
ruff check src/lnb
```
