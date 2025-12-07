# Migration from setuptools to uv

This project has been successfully migrated from setuptools to uv package manager.

## What Changed

### Files Added
- `pyproject.toml` - Modern Python project configuration
- `uv.lock` - Dependency lock file for reproducible builds
- `.venv/` - Virtual environment managed by uv

### Files Removed
- `setup.py` - Old setuptools configuration
- `MANIFEST.in` - No longer needed with modern build system

### Configuration Changes
- Updated minimum Python version from 3.7 to 3.9 (required by dev dependencies)
- Switched from setuptools-git-versioning to hatch-vcs for version management
- Converted to modern pyproject.toml format

## Common uv Commands

### Development Setup
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Install with dev dependencies
uv sync --extra dev
```

### Running Commands
```bash
# Run Python scripts
uv run python script.py

# Run tests
uv run pytest

# Run linting
uv run black .
uv run pylint marshy/

# Build package
uv build
```

### Dependency Management
```bash
# Add a new dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name

# Update dependencies
uv sync --upgrade

# Remove a dependency
uv remove package-name
```

## Benefits of uv

1. **Speed**: Much faster dependency resolution and installation
2. **Reproducibility**: Lock file ensures consistent environments
3. **Modern**: Uses pyproject.toml standard
4. **Simplicity**: Single tool for virtual environments, dependencies, and builds
5. **Compatibility**: Works with existing Python ecosystem

## Migration Verification

The migration has been tested and verified:
- ✅ All 64 tests pass
- ✅ Package builds successfully
- ✅ All dependencies install correctly
- ✅ Dev tools (black, pylint) work properly
- ✅ Both main packages (marshy, injecty_config_marshy) import correctly